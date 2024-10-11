# -*- coding: UTF-8 -*-
"""NWL Tool runner

example usage:

  partis-nwl [tool_name] [inputs_file]

"""

import sys
import os
import os.path as osp
from pathlib import Path
import re
from pprint import pformat
from copy import copy
import time
import argparse
from argparse import RawTextHelpFormatter
import logging
import traceback
import zipfile
import shutil
import tempfile
import importlib
import subprocess

import datetime
from timeit import default_timer as timer

from partis.pyproj import (
  norm_dist_filename )

from partis.utils import (
  logging_parser_add,
  logging_parser_init,
  log_levels,
  getLogger,
  LogListHandler,
  ModelHint,
  VirtualEnv,
  MutexFile )

log = getLogger(__name__)

from .utils import (
  dump_file,
  detect_run_with_mpi,
  get_mpiexec,
  get_processes,
  get_cpus_per_process,
  get_threads_per_cpu,
  get_gpus_per_process )

from partis.schema import (
  is_mapping,
  SchemaHint,
  SchemaError,
  Loc,
  SeqPrim,
  SchemaModule )

from partis.schema.serialize.yaml import (
  load,
  dump,
  dumps )

from .results import (
  ToolResults )

from .utils import (
  get_dirs,
  get_mpiexec,
  get_processes,
  get_cpus_per_process,
  get_threads_per_cpu,
  get_gpus_per_process,
  get_runhost,
  get_jobhost,
  get_jobuser,
  get_jobid,
  get_jobname )

from .load_tool import load_tool_wait

from .tool import (
  Tool )

from .workflow import (
  Workflow )

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

def argument_parser( ):

  """Parse for commandline arguments.
  """

  parser = argparse.ArgumentParser(
    description = __doc__,
    formatter_class = RawTextHelpFormatter )

  parser.add_argument( "tool_name",
    type = str,
    nargs = '?',
    default = None,
    help = "Tool file or qualified name" )

  parser.add_argument( "inputs_file",
    type = str,
    default = None,
    nargs = '?',
    help = "Tool inputs. An empty string will result in using tool default input values" )

  parser.add_argument( "--tool",
    type = str,
    default = None,
    # dest = 'tool_name',
    help = "Alias for tool_name" )

  parser.add_argument( "--inputs",
    type = str,
    default = None,
    # dest = 'inputs_file',
    help = "Alias for inputs_file" )

  parser.add_argument( "--template",
    action='store_true',
    help = "Generate template tool inputs file using default values instead of running tool." )

  parser.add_argument( "-s", "--startdir",
    type = Path,
    default = None,
    help = "Starting directory, relative path for input files" )

  parser.add_argument( "-c", "--workdir",
    type = Path,
    default = None,
    help = "Workflow directory, relative path for input files" )

  parser.add_argument( "-d", "--rundir",
    type = Path,
    default = None,
    help = "Run directory, relative path for output files" )

  parser.add_argument( "-e", "--environ",
    type = str,
    default = None,
    help = """Specify alternate environment variables.
      If not specified, the processes will inherit the current environment.
      If an empty string, the current environment will be discarded.
      If a file path, the file should be a YAML file with key-value pairs to use
      for the environment dictionary.""" )

  parser.add_argument( "--aux",
    type = str,
    default = list(),
    metavar="KEY=VALUE",
    nargs='+',
    help = "Auxiliary variables that may be used for input query substitution" )

  parser.add_argument( "-t", "--timelimit",
    type = int,
    default = None,
    help = "Time limit before killing process (seconds)" )

  parser.add_argument( "--np",
    type = int,
    default = None,
    help = "Number of processes" )

  parser.add_argument( "--ncp",
    type = int,
    default = None,
    help = "Number of cpus per process" )

  parser.add_argument( "--ntc",
    type = int,
    default = None,
    help = "Number of logical threads per cpu (usually 1 or 2)" )

  parser.add_argument( "--ngp",
    type = int,
    default = None,
    help = "Number of gpus per process" )

  parser.add_argument( "--doc",
    action='store_true',
    help = "Print extra tool documentation" )


  # parser.add_argument( "--test",
  #   type = str,
  #   default = list(),
  #   action = 'append',
  #   help = "Tool test files" )

  parser.add_argument( "--mpiexec",
    type = str,
    default = None,
    help = "List of commands to execute a program within MPI, if available" )

  parser.add_argument( "--truncate",
    default = False,
    action='store_true',
    help = "Clears run directory before starting job" )

  parser.add_argument( "--venv",
    type = Path,
    default = None,
    help = """Specified path to create, or re-use, a virtual environment
      for installing tool packages.
      If not given, one will be created in the tool run directory.""" )

  parser.add_argument( "--venv-force",
    default = False,
    action='store_true',
    help = """Forces the creation of a new virtual environment, even if an existing
      one with the same name is found.""" )

  parser.add_argument( "--venv-in",
    type = Path,
    default = list(),
    action = 'append',
    help = """Inherit the 'site-packages' from one or more existing virtual environment(s).""" )

  parser.add_argument( "-f", "--find-links",
    type = str,
    default = list(),
    action = 'append',
    help = """Search location to find installable tool packages. The current
      directory is automatically added.""" )

  parser.add_argument( "--serial",
    action = 'store_true',
    help = """Preserves the initial order of workflow stages unless a dependency
      between two stages (I/O query, or an explicit 'afterok') would be violated.
      All stages are run sequentially (no parallel execution).""" )

  logging_parser_add(parser)

  return parser

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
def parse_key_values( raw_vars ):
  vars = dict()

  for kv in raw_vars:
    parts = kv.split('=', 1)

    if len(parts) > 1:

      k = parts[0].strip()
      v = parts[1].strip()

      vars[k] = v

  return vars

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++#
def dump_error_results(
  log,
  log_handler,
  startdir,
  workdir,
  rundir,
  aux ):

  rundir.mkdir(parents = True, exist_ok = True)

  results_file = rundir/'nwl.results.yml'
  log_file = rundir/'nwl.log.yml'
  env_file = rundir/'nwl.env.yml'

  results = ToolResults()

  results.job.args = sys.argv

  results.job.id = get_jobid()
  results.job.name = get_jobname()

  results.job.host = get_jobhost()
  results.job.user = get_jobuser()

  results.runtime.startdir = startdir
  results.runtime.workdir = workdir
  results.runtime.rundir = rundir
  results.runtime.aux = aux

  env = os.environ

  env = {
    re.sub( r'[^A-Za-z0-9\_]+', "_", k ) : v
    for k,v in env.items() }

  try:

    try:

      dump_file(
        obj = env,
        fname = env_file,
        num = 0,
        log = log.error )

      dump_file(
        obj = log_handler.logs,
        fname = log_file,
        num = 0,
        log = log.error )

      dump_file(
        obj = results,
        fname = results_file,
        num = 0,
        log = log.error )


    except Exception as e:
      log.error( ModelHint(
        msg = f"Failed to write tool result file",
        hints = e ) )

  except Exception as e:
    log.error( ModelHint(
      msg = f"Failed to encode tool result document",
      hints = e ) )

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
def positional_defaults(*args, **kwargs):

  # filter out positional arguments that are None
  pos_args = [ v for v in args if v is not None ]

  for k,v in kwargs.items():

    if v is None and len(pos_args):
      kwargs[k] = pos_args.pop(0)

  return kwargs

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
def run_tool( log, nwl_log, args ):

  if os.getcwd() not in sys.path:
    sys.path.append(os.getcwd())

  pwd = Path().resolve()

  # keep complete record of runner log in case tool fails
  log_handler = LogListHandler()
  log.addHandler( log_handler )

  venv_log = nwl_log.getChild("venv")
  venv_log.propagate = False
  venv_log_handler = LogListHandler()
  venv_log.addHandler( venv_log_handler )

  # extract from either positional or named arguments
  tool_name, inputs_file = positional_defaults(
    args.tool_name,
    args.inputs_file,
    tool_name = args.tool,
    inputs_file = args.inputs ).values()

  #.............................................................................
  # If given a previous result file, instead of tool name, use the result file
  # to fill in all arguments as a re-run
  if osp.basename(tool_name).startswith("nwl.results.yml"):

    if not osp.exists(tool_name):
      log.error(
        f"File not found: {tool_name}")

      return 1

    tool_name = osp.realpath(tool_name)

    if not ( args.truncate or (hasattr(sys.stdout, 'isatty') and sys.stdout.isatty()) ):
      log.error(
        f"Set ``--truncate`` to over-write previous result: {tool_name}")

      return 1

    elif not args.truncate:
      args.truncate = input(f"Overwrite (--truncate) previous results [yes/no]? ").lower().startswith('y')

    if not args.truncate:
      log.error(
        f"Run cancelled by user.")

      return 1

    dir = args.rundir or osp.dirname(tool_name)

    results_file = osp.join(dir, "nwl.results.yml")

    if osp.exists(results_file):

      results_file_bak = osp.join(
        dir,
        f"nwl.results.yml.bak_{int(time.time())}" )

      log.info(f"Saving backup: {results_file_bak}")
      shutil.copy2(results_file, results_file_bak)

    log.info(f'Loading from previous run result: {tool_name}')

    prev_results = load(
      tool_name,
      schema = ToolResults )

    tool_name = prev_results.job.tool_qualname

    if inputs_file is None:
      inputs_file = prev_results.job.inputs_file

      if not osp.abspath(inputs_file) and pwd != prev_results.job.curdir:
        inputs_file = osp.join( prev_results.job.curdir, inputs_file )

    args.startdir = args.startdir or prev_results.runtime.startdir
    args.workdir = args.workdir or prev_results.runtime.workdir
    args.rundir = args.rundir or prev_results.runtime.rundir
    args.mpiexec = args.mpiexec or prev_results.runtime.mpiexec
    args.np = args.np or prev_results.runtime.processes
    args.ncp = args.ncp or prev_results.runtime.cpus_per_process
    args.ntc = args.ntc or prev_results.runtime.threads_per_cpu
    args.ngp = args.ngp or prev_results.runtime.gpus_per_process

  pwd, startdir, workdir, rundir = get_dirs(
    tool_name = tool_name,
    startdir = args.startdir,
    workdir = args.workdir,
    rundir = args.rundir )


  #.............................................................................
  venv_dir = args.venv

  if not venv_dir:
    venv_dir = rundir/'venv_nwlrun'

  venv_dir = osp.abspath( venv_dir )

  find_links = [
    osp.abspath(p) for p in args.find_links ]

  # extract any auxiliary variables
  aux = parse_key_values( args.aux )

  venv = None
  returncode = 0
  tool_closed = False

  if tool_name is None:
    log.error(
      f"tool_name is required")

    dump_error_results(
      log = log,
      log_handler = log_handler,
      startdir = startdir,
      workdir = workdir,
      rundir = rundir,
      aux = aux )

    return 1

  log.info(f'Run: {tool_name}')
  log.info(f'Venv dir: {venv_dir}')

  try:
    # determine environment variables
    if args.environ is None:
      # inherit
      env = os.environ

    elif args.environ == '':
      # scrub
      env = dict()

    else:
      # load from YAML file
      env = load(
        file = args.environ,
        loc = Loc(
          filename = args.environ ) )

      if not (
        is_mapping( env )
        and all(
          isinstance(k, str) and isinstance(v, str)
          for k,v in env.items() ) ):

        returncode = 1
        log.error(
          f"`environ` file must be a single-level mapping: {args.environ}\n{env}" )



    # create/re-use virtual environment to install any packages

    venv_in = args.venv_in

    venv_mutex = MutexFile(
      prefix = osp.basename(venv_dir),
      dir = osp.dirname(venv_dir),
      # 10 min
      timeout = 600.0 )

    venv = VirtualEnv(
      path = venv_dir,
      inherit_site_packages = venv_in,
      reuse_existing = not args.venv_force,
      args = ['--without-pip'],
      logger = venv_log,
      mutex = venv_mutex )

    tool, results_schema = load_tool_wait(
      name = tool_name,
      venv = venv,
      find_links = find_links )

    if tool is None and ( args.venv_in or not args.venv_force ):
      # install failed. Attempt again, but with no re-use or inheritance
      # from other environments
      # NOTE: non-install errors will have raised an exception instead of
      # returning None
      # NOTE: existing install(s) may lead to incompatible dependencies
      log.warning(ModelHint(
        f"Failed to load tool, re-attempting without inherited site-packages",
        hints = venv_log_handler.hints ))

      venv_log_handler.clear()

      venv_in = list()

      venv = VirtualEnv(
        path = venv_dir,
        inherit_site_packages = venv_in,
        reuse_existing = False,
        args = ['--without-pip'],
        logger = venv_log,
        mutex = venv_mutex )

      tool, results_schema = load_tool_wait(
        name = tool_name,
        venv = venv,
        find_links = find_links )

    if tool is None:
      # still could not load tool
      returncode = 1

      log.error(ModelHint(
        f"Failed to load tool",
        hints = [ModelHint.from_dict(kw) for kw in venv_log_handler.logs] ))

      venv_log_handler.clear()

    if returncode == 0 and tool.type == 'workflow':
      with venv:
        # NOTE: using venv as context will update 'os.environ['PATH'] and sys.path
        # to approximate the environment seen by an interpreter run in the venv

        # ensure plugs reloaded with access to additional search paths
        from partis.schema.plugin import (
          schema_plugins )

        schema_plugins.load_plugins()

        log.success(f'Loaded workflow: {tool_name}')

        result = tool.run_wait(
          startdir = startdir,
          workdir = workdir,
          rundir = rundir,
          workflow_file = tool_name,
          venv = venv,
          log = nwl_log.getChild("workflow"),
          initlogs = log_handler.logs,
          find_links = find_links,
          processes = args.np,
          cpus_per_process = args.ncp,
          threads_per_cpu = args.ntc,
          gpus_per_process = args.ngp,
          run_serial = args.serial )

        tool_closed = True
        returncode = 1 if tool._failed else 0

    if returncode == 0 and tool.type == 'tool':
      with venv:
        # NOTE: using venv as context will update 'os.environ['PATH'] and sys.path
        # to approximate the environment seen by an interpreter run in the venv

        # ensure plugs reloaded with access to additional search paths
        from partis.schema.plugin import (
          schema_plugins )

        schema_plugins.load_plugins()

        log.success(f'Loaded tool: {tool_name}')

        if args.doc:
          log.info( "Input Schema" )
          log.info( results_schema.data.inputs.__doc__)
          log.info( "Output Schema" )
          log.info( results_schema.data.outputs.__doc__)
          log.info( "Commands Output Schema" )
          log.info( results_schema.data.commands.__doc__)

        if args.template:
          init_val = results_schema.data.inputs.schema.init_val

          if inputs_file:
            dump( inputs_file, init_val )

            log.info(f"Tool inputs template generated: {inputs_file}")

          else:
            log.info( ModelHint(
              "Tool inputs template",
              data = dumps(init_val) ))

        elif inputs_file is not None:
          # run tool
          result = tool.run_wait(
            startdir = startdir,
            workdir = workdir,
            rundir = rundir,
            env = env,
            venv = venv,
            aux = aux,
            timeout = args.timelimit,
            truncate = args.truncate,
            mpiexec = args.mpiexec,
            processes = args.np,
            cpus_per_process = args.ncp,
            threads_per_cpu = args.ntc,
            gpus_per_process = args.ngp,
            inputs_file = inputs_file,
            jobargs = list(sys.argv),
            results_schema = results_schema,
            log = nwl_log.getChild("tool"),
            initlogs = log_handler.logs )

          tool_closed = True
          returncode = 0 if result.runtime.success else 1

  except Exception as e:
    # catch any errors not caught by the tool

    returncode = 1
    log.error( ModelHint(
      "Runtime failure",
      hints = e ) )

  if inputs_file is not None and not ( args.template or tool_closed ):

    dump_error_results(
      log = log,
      log_handler = log_handler,
      startdir = startdir,
      workdir = workdir,
      rundir = rundir,
      aux = aux )

  return returncode

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
def feat_enabled(enabled, disabled):
  if not ( enabled or disabled ):
    return None

  if enabled:
    return True

  return False

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
def main():

  parser = argument_parser( )
  args = parser.parse_args( )

  logging_parser_init(args)

  # TODO: find better way to disable logging from other packages.
  # Maybe instead setLevel to individual packages/loggers in init_logging
  # instead of setting it on the 'root' logger for all packages
  for l in ['matplotlib', 'numba', 'trio', 'trimesh']:
    getLogger(l).setLevel(logging.ERROR)

  nwl_log = getLogger(f"nwl")
  log = nwl_log.getChild("run")

  if detect_run_with_mpi():
    log.error(
      f"NWL tool should not be launched directly by an MPI startup program."
      " Set '--mpiexec', or 'NWL_MPIEXEC', with needed MPI launch command and argument template string.")
    return 1

  time_start = timer()

  returncode = run_tool( log, nwl_log, args )

  time_end = timer()
  walltime = time_end - time_start

  if returncode != 0:
    log.error(f"Job exited with errors: wall-time {datetime.timedelta(seconds = walltime)} (H:M:S)")
  else:
    log.success(f"Job completed successfully: wall-time {datetime.timedelta(seconds = walltime)} (H:M:S)")

  return returncode

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
if __name__ == "__main__":
  exit( main() )
