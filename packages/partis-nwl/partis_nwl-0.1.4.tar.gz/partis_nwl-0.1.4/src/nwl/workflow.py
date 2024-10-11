
import os
import os.path as osp
import re
import subprocess
import shutil
import base64
import difflib
import shlex
from timeit import default_timer as timer
import socket
import rich

import logging
log = logging.getLogger(__name__)

from partis.utils import (
  fmt_limit,
  hint_level_name,
  getLogger,
  branched_log,
  odict,
  adict,
  checksum,
  ModelHint,
  ModelError,
  Loc,
  LogListHandler,
  ProcessEnv,
  VirtualEnv )

from partis.utils.async_trio import (
  wait_all,
  ResourceLimiter )

from partis.utils.inspect import (
  filter_traceback )

from partis.schema import (
  required,
  optional,
  derived,
  is_string,
  is_sequence,
  is_mapping,
  is_evaluated,
  is_valued,
  is_valued_type,
  is_optional,
  PJCEvaluated,
  BoolPrim,
  IntPrim,
  FloatPrim,
  StrPrim,
  SeqPrim,
  MapPrim,
  UnionPrim,
  PassPrim,
  StructValued,
  MapValued,
  SchemaError,
  SeqValued,
  schema_declared,
  SchemaModule,
  SchemaError,
  SchemaValidationError,
  SchemaDetectionError )

from partis.schema.prim.any_prim import (
  any_prim_cases,
  AnyPrim )

from partis.schema.hint import (
  Hint,
  HintList )

from .base import (
  SerialGroup,
  ParallelGroup,
  workflow_declared,
  WorkflowError )

from .log import (
  LogContext,
  LogEvent )

from .allocation import RunAllocation

from partis.schema.serialize.yaml import (
  load,
  dump )

from .utils import (
  get_dirs,
  get_mpiexec,
  get_processes,
  get_nodelist,
  get_cpus_per_process,
  get_threads_per_cpu,
  get_gpus_per_process,
  get_runhost,
  get_jobhost,
  get_jobuser,
  get_jobid,
  get_jobname,
  load_results,
  run_order,
  run_order_hints,
  diff_hint )

from .inputs import (
  AnyInput,
  QueryContext,
  EnabledInputContext )

from .outputs import (
  AnyOutput,
  AnyMainOutput,
  OutputsContext )


#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
class CheckFile( StructValued ):

  schema = dict(
    tag = 'checkfile' )

  path = StrPrim(
    doc = "Path relative to run directory",
    max_lines = 1 )

  size = IntPrim(
    doc = "Expected size of file in bytes",
    default_val = optional )

  checksum = StrPrim(
    doc = """Expected checksum of file, in hexadecimal format

      The hash is refixed with the algorithm used to compute the hash.
      For example, the SHA-1 hash would be given as:

        sha1$00ea1da4192a2030f9ae023de3b3143ed647bbab
      """,
    # pattern = r"(\w+)\$([0-9a-fA-F]+)",
    default_val = optional )

  content_mode = StrPrim(
    doc = """Mode used for contents of file

      In `binary` mode, the contents are assumed to be in standard
      Base64 format ( RFC 3548 ).
      """,
    restricted = [ 'text', 'binary' ],
    default_val = 'text' )

  contents = StrPrim(
    doc = """Contents of file""",
    default_val = optional )

  #-----------------------------------------------------------------------------
  def check_file( self, dir ):
    path = os.path.join( dir, self.path )

    if not os.path.exists( path ):
      raise ModelError(f"Expected file does not exist: {path}")

    if self.size is not None:
      size = os.stat( path ).st_size

      if self.size != size:
        raise ModelError(f"Expected file size {self.size}: {size}")

    if self.checksum is not None:
      _alg, _hash = self.checksum.split("$")

      hash = checksum( path, algorithm = _alg )

      if hash != _hash:
        raise ModelError(
          f"File checksum failed",
          hints = [
            f"file: {path}",
            f"hash: {_alg}",
            f"expected: {_hash}",
            f"actual: {hash}" ])

    if self.contents is not None:
      if self.content_mode == 'text':
        lines_from = self.contents.strip().splitlines()

        with open( path, 'r' ) as fp:
          lines_to = fp.read().strip().splitlines()

        ndiff = (
          sum( a != b for a, b in zip(lines_from, lines_to ) )
          + abs( len(lines_from) - len(lines_to) ) )

        if ndiff > 0:
          dlines = difflib.unified_diff(
            lines_from,
            lines_to,
            fromfile = 'expected',
            tofile = path,
            lineterm = '' )

          # diff = "\n  ".join(dlines)

          raise ModelError(
            f"File contents failed",
            hints = [
              f"file: {path}",
              ModelHint(
                "lines",
                hints = dlines ) ])

      elif self.content_mode == 'binary':

        bytes_from = base64.standard_b64decode( self.contents.strip() )

        with open( path, 'rb' ) as fp:
          bytes_to = fp.write( )

        if bytes_from != bytes_to:
          raise ModelError(f"Expected file binary differs: {path}")

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
class Check( StructValued ):
  schema = dict(
    tag = 'check',
    default_val = derived )

  commands = MapPrim(
    doc = "Expected command results",
    item = AnyPrim,
    default_val = optional )

  outputs = MapPrim(
    doc = "Expected outputs",
    item = AnyPrim,
    default_val = optional )

  files = SeqPrim(
    doc = """List of expected output files in run directory""",
    item = CheckFile,
    default_val = list() )

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
class Stage( RunAllocation ):
  schema = dict(
    tag = 'stage',
    doc = "Workflow stage",
    default_val = derived )

  doc = StrPrim(
    doc = "Documentation string for more information about this workflow stage",
    default_val = '',
    max_lines = 100 )

  afterok = UnionPrim(
    doc = """Names of workflow stages that must complete with no errors
      before running this stage.

      .. note::

        It is *not* necessary to specify this explicitly if queries in the stage
        inputs already imply the order""",
    default_case = 0,
    cases = [
      StrPrim(
        default_val = '' ),
      SeqPrim(
        item = StrPrim(
          default_val = '' ),
        default_val = list() )])

  tool = StrPrim(
    doc = "Name of tool to run",
    default_val = '' )

  inputs = UnionPrim(
    default_case = 0,
    cases = [
      StrPrim(
        doc = "Input file",
        default_val = '' ),
      MapPrim(
        doc = "Input values",
        item = AnyPrim,
        default_val = dict() ) ] )

  check = Check

  epilog = SeqPrim(
    doc = """List of possible logging events after tool runs.
      Logs with level 'ERROR' or 'CRITICAL' are used to establish whether a
      something has failed.
      """,
    item = LogEvent,
    default_val = list() )

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
class WorkflowStatus( StructValued ):
  schema = dict(
    tag = 'status',
    doc = "Status",
    default_val = derived )

  success = BoolPrim(
    doc = "Flag for whether all checks were successful",
    default_val = True )

  startdir = StrPrim(
    doc = "Directory from which the tool was initially started",
    default_val = "" )

  workdir = StrPrim(
    doc = "Directory where tool was told to run",
    default_val = "" )

  stages = MapPrim(
    item = StrPrim(),
    default_val = dict() )

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
class Workflow( StructValued ):
  schema = dict(
    doc = "Workflow definition",
    declared = workflow_declared,
    default_val = derived )

  nwl = IntPrim(
    doc = "Version of Nano Workflow Language (NWL)",
    restricted = [ 1, ],
    default_val = 1 )

  stages = MapPrim(
    item = Stage,
    default_val = dict() )

  #-----------------------------------------------------------------------------
  def __init__( self, *args, **kwargs ):
    super().__init__(*args, **kwargs)

    self._configured = False
    self._opened = False
    self._closed = False
    self._failed = False
    self._save_num = 0

    self._log_handler = None
    self._results_log = None

  #-----------------------------------------------------------------------------
  def _update_result_logs( self ):
    if self._log_handler is None:
      return

    self._results_log.extend(self._log_handler.logs)
    self._log_handler.clear()

    # command fails if any prolog event of 'ERROR' or 'CRITICAL'
    self._failed = self._failed or any(
      l['level'] in [ 'ERROR', 'CRITICAL' ]
      for l in self._results_log )

  #-----------------------------------------------------------------------------
  async def _config( self, *,
    startdir = None,
    workdir = None,
    rundir = None,
    workflow_file = None,
    aux = None,
    truncate = None,
    log = None,
    venv = None,
    initlogs = None,
    run_stages = None,
    find_links = None,
    processes = None,
    cpus_per_process = None,
    threads_per_cpu = None,
    gpus_per_process = None,
    run_serial = None ):
    """Configure tool execution

    Parameters
    ----------
    workflow_file : None | str
      File read to create this workflow
    aux : None | dict
      Auxiliary variables that may be used for input query substitution.
    timeout : int | None
      Timeout to terminate command in seconds
    truncate : None | bool
      If true, and rundir already exists, will completely remove directory and
      all contents before starting command. (default: False)
    log : None | logging.Logger
      Parent logger to issue logging events
    venv : :class:`ProcessEnv <partis.utils.venv.ProcessEnv`
      Virtual process environment to run any subprocesses.
      If not given, the current environment will be used.
    initlogs : list
      Logs to add to results that occurred before running tool

    Returns
    -------
    None
    """
    from .load_tool import load_tool, install_tool_deps

    if self._configured:
      raise ValueError("Workflow already configured")

    self._configured = True

    if log is not None:
      self._log = log
    else:
      self._log = getLogger(f"workflow")

    if run_stages is None:
      run_stages = list(self.stages.keys())

    self._log_handler = LogListHandler()
    self._log.addHandler( self._log_handler )

    self._results_log = HintList()

    self._pwd, self._startdir, self._workdir, self._rundir = get_dirs(
      tool_name = "",
      startdir = startdir,
      workdir = workdir,
      rundir = rundir )

    self._log.info(f'Starting dir: {self._startdir}')
    self._log.info(f'Working dir: {self._workdir}')
    self._log.info(f'Run dir: {self._rundir}')

    if workflow_file:
      self._workflow_file = osp.realpath(workflow_file)
      self._workflow_file_dir = osp.dirname(self._workflow_file)
    else:
      self._workflow_file = None
      self._workflow_file_dir = self._startdir

    if venv is None:
      # TODO
      assert False

    self._venv = venv
    self._venv_log_handler = LogListHandler()
    self._venv.logger.addHandler( self._venv_log_handler )

    processes = get_processes( processes ) or 1
    cpus_per_process = get_cpus_per_process( cpus_per_process ) or 1
    threads_per_cpu = get_threads_per_cpu( threads_per_cpu ) or 1
    gpus_per_process = get_gpus_per_process( gpus_per_process ) or 0

    self._resource_limiter = ResourceLimiter(
      cpus = processes*cpus_per_process,
      gpus = processes*gpus_per_process )

    stage_args = [
      'processes',
      'cpus_per_process',
      'gpus_per_process' ]

    self._stage_tools = dict()
    self._stage_deps = dict()
    self._stage_reqs = dict()

    for dir, stage in self.stages.items():
      with branched_log(
        log = self._log,
        name = f"stages.{dir}",
        msg = f"Stage init `{dir}`" ) as log:

        rundir = osp.join(self._rundir, dir)
        prev_results = None

        self._stage_tools[dir] = None
        self._stage_deps[dir] = list()
        self._stage_reqs[dir] = dict()

        if dir not in run_stages:
          continue

        #.......................................................................
        # load/install tool (without dependencies)
        self._venv_log_handler.clear()

        tool, results_schema = await load_tool(
          name = stage.tool,
          venv = self._venv,
          find_links = find_links,
          no_deps = True )

        if tool is None:
          log.error( ModelHint(
            f"Failed to load tool",
            hints = self._venv_log_handler.hints ) )

          break

        log.success(f'Loaded tool: {stage.tool}')

        #.......................................................................
        # check that any 'checks' are valid
        if stage.check.commands is not None:
          with filter_traceback(
            suppress = True,
            log = log.error,
            msg = f"Validation failed" ):

            results_schema.data.commands.schema.decode(stage.check.commands)

        if stage.check.outputs is not None:
          with filter_traceback(
            suppress = True,
            log = log.error,
            msg = f"'check' validation failed" ):

            results_schema.data.outputs.schema.decode(stage.check.outputs)

        #.......................................................................
        # check resource requested for tool to that allocated for workflow
        if (
          stage.processes > processes
          or stage.cpus_per_process > cpus_per_process
          or stage.gpus_per_process > gpus_per_process ):

          _processes = min(processes, stage.processes)
          _cpus_per_process = min(cpus_per_process, stage.cpus_per_process)
          _gpus_per_process = min(gpus_per_process, stage.gpus_per_process)

          log.warning(ModelHint(
            f'Limited resource allocation',
            level = 'warning',
            hints = [
              ModelHint(f"processes", data = f"{stage.processes} -> {_processes}"),
              ModelHint(f"cpus_per_process", data = f"{stage.cpus_per_process} -> {_cpus_per_process}"),
              ModelHint(f"gpus_per_process", data = f"{stage.gpus_per_process} -> {_gpus_per_process}") ]))

          stage.processes = _processes
          stage.cpus_per_process = _cpus_per_process
          stage.gpus_per_process = _gpus_per_process

        self._stage_reqs[dir] = self._resource_limiter.require(
          cpus = stage.processes * stage.cpus_per_process,
          gpus = stage.processes * stage.gpus_per_process )

        #.......................................................................
        # get inputs from stage, or from file specified in stage
        inputs = None
        inputs_file = None

        if is_string(stage.inputs) and len(stage.inputs) > 0:
          inputs_file = stage.inputs

          if not osp.isabs(inputs_file):
            inputs_file = osp.join( self._workflow_file_dir, inputs_file )

        elif is_mapping(stage.inputs):
          inputs = stage.inputs

        #.......................................................................
        # perform configuration of tool (but not run it) so that input/output
        # inter-dependencies can be determined and checked
        tool._config(
          log = log,
          workdir = self._rundir,
          rundir = rundir,
          results_schema = results_schema,
          inputs = inputs,
          inputs_file = inputs_file,
          **{k: stage.get(k) for k in stage_args } )

        # TODO: check for previous run attempts?

        for query_dep in tool._results.runtime.query_deps:

          if query_dep.base in ['workflow', 'workdir']:
            _dir = query_dep.path

            if query_dep.base == 'workflow':
              # For workflow queries, the path points to 'nwl.results.yml',
              # need to get just the directory name
              _dir = osp.dirname(_dir)

            # TODO: still some ambiguity between the path to the tool run-directory
            # versus how it's referenced in the workflow
            _dir = osp.relpath( _dir,  start = self._rundir )

            if _dir in run_stages and _dir not in self._stage_deps[dir]:
              self._stage_deps[dir].append(_dir)

        if stage.afterok:

          if is_string(stage.afterok):
            _deps = [stage.afterok]
          else:
            _deps = [_dep for _dep in stage.afterok if _dep]

          self._stage_deps[dir].extend([
            _dep
            for _dep in _deps
            if _dep not in self._stage_deps[dir]])


      #.........................................................................
      # quite early if any tool causes failure
      self._update_result_logs()
      self._failed = self._failed or tool._failed

      if self._failed:
        break

      self._stage_tools[dir] = tool

    #...........................................................................
    self._update_result_logs()

    if self._failed:
      return

    #...........................................................................
    # determine the order in which the tools have to be run according to the
    # input/output inter-dependencies
    self._log.info(ModelHint(
      f'Workflow run inter-dependencies',
      hints = [
        ModelHint(
          f"{k}",
          data = 'None' if not deps else None,
          level = 'info',
          hints = ModelHint.cast(deps).hints if deps else None )
        for k,deps in self._stage_deps.items() ] ))

    self._run_order = run_order(run_serial, self._stage_deps)

    self._log.info(ModelHint(
      f'Workflow run order',
      hints = run_order_hints(self._run_order) ))

    #...........................................................................
    # install all dependencies at the same time to save time,
    # and reduce chances of conflicts between dependencies that might be arise
    # if they were installed individually
    self._venv_log_handler.clear()

    self._log.info(f"Installing tool dependencies")

    deps = await install_tool_deps(
      tools = list(self._stage_tools.values()),
      venv = self._venv,
      find_links = find_links )

    if deps is None:

      self._log.error( ModelHint(
        f"Failed to install dependencies",
        hints = self._venv_log_handler.hints ) )

    else:
      self._log.debug( ModelHint(
        f"Installed dependencies",
        hints = deps ) )

    self._update_result_logs()

    if self._failed:
      return

  #-----------------------------------------------------------------------------
  async def _run_stage( self, dir ):
    if self._failed:
      return

    tool = self._stage_tools[dir]
    stage = self.stages[dir]
    resource_reqs = self._stage_reqs[dir]

    rundir = osp.join(self._rundir, dir)
    tool_results_file = os.path.join( rundir, "nwl.results.yml" )

    if is_string(stage.inputs) and len(stage.inputs) > 0:
      inputs_file = stage.inputs

      if not osp.isabs(inputs_file):
        inputs_file = osp.join( self._workflow_file_dir, inputs_file )

    elif is_mapping(stage.inputs) and len(stage.inputs) > 0:
      inputs_file = osp.join(self._rundir, f"{dir}.yml")
      dump( inputs_file, stage.inputs )

    else:
      inputs_file = ""

    level = hint_level_name(self._log.getEffectiveLevel())

    _startdir = self._startdir

    args = [
      'python3',
      '-m',
      'partis.nwl.__main__',
      '-v', level,
      '--no-color',
      '--np', str(stage.processes),
      '--ncp', str(stage.cpus_per_process),
      '--ngp', str(stage.gpus_per_process),
      '--startdir', self._startdir,
      '--workdir', self._rundir,
      '--rundir', rundir,
      tool.qualname._encode,
      inputs_file ]

    # NOTE: this context manager will block until the required resources
    # become available (i.e. when other tools exit, freeing up CPUs)
    async with resource_reqs:

      self._log.info(ModelHint(
        f'Stage run `{dir}`: {tool.qualname}',
        hints = [
          ModelHint(
            'Config',
            level = 'info',
            hints = {
              'tool' : tool.qualname,
              'rundir': rundir,
              'inputs_file': inputs_file,
              **resource_reqs.resources } ),
          ModelHint(
            'Run Arguments',
            level = 'debug',
            hints = args ) ] ))

      res = await self._venv.trio_run(
        args,
        capture_stdout = True,
        stderr = subprocess.STDOUT,
        check = False )

    #...........................................................................
    # perform checks on the tool results after it exits

    out = res.stdout.decode('utf-8', errors = 'replace')

    with branched_log(
      log = self._log,
      name = f"stage",
      msg = f"Stage exit `{dir}`: {tool.qualname}" ) as log:

      if res.returncode == 0:
        log.success(f'Tool returned success')

      else:
        lines = out.splitlines()[-50:]
        err_hint = None

        if len( lines ) > 0:
          txt = "\n".join(lines)

          err_hint = ModelHint(
            f"last {len( lines )} lines of output",
            level = 'warning',
            data = txt,
            format = 'block' )

        log.error(ModelHint(
          f'Tool error return code: {dir}, {tool.qualname} -> {res.returncode}',
          hints = err_hint ))

        raise subprocess.CalledProcessError(
          res.returncode,
          res.args,
          output = res.stdout )


      with open( tool_results_file, "r" ) as fp:
        doc = fp.read()

      # read in tool results
      tool_results = load(
        tool_results_file,
        schema = tool.results_schema() )

      check = stage.check
      check_hints = list()

      # check that commands have correct values
      if check.commands is not None:
        hint = diff_hint(
          loc = Loc(path = [ 'data', 'commands' ]),
          ref = self.commands,
          val = tool_results.data.commands )

        if hint is not None:
          check_hints.append( hint )

      # check that outputs have correct values
      if check.outputs is not None:
        hint = diff_hint(
          loc = Loc(path = [ 'data', 'outputs' ]),
          ref = check.outputs,
          val = tool_results.data.outputs )

        if hint is not None:
          check_hints.append( hint )

      if len(check_hints) > 0:
        log.error(ModelHint(
          "Check failed",
          hints = check_hints ))

      # check that output files have correct values
      for file in check.files:
        with filter_traceback(
          suppress = True,
          log = log.error,
          msg = f"Check of output file failed" ):

          file.check_file( dir = rundir )

      # check logs
      with filter_traceback(
        suppress = True,
        log = log.error,
        msg = f"Check log evaluation failed" ):

        logs = stage.epilog._eval(
          context = LogContext(
            results = tool_results,
            static = None ),
          logger = log )

        # filter for only enabled log events
        for l in logs:
          if l.enabled:
            log.log( logging.getLevelName(l.level), l.msg )

  #-----------------------------------------------------------------------------
  async def _run_parallel_group( self, group ):
    if self._failed:
      return

    group_comps = list()

    for comp in group:
      group_comps.append( self._run_group(comp) )

    await wait_all(group_comps)

    self._update_result_logs()

  #-----------------------------------------------------------------------------
  async def _run_serial_group( self, group ):
    if self._failed:
      return

    for i, comp in enumerate(group):
      await self._run_group(comp)
      self._update_result_logs()


  #-----------------------------------------------------------------------------
  async def _run_group( self, group ):
    if self._failed:
      return

    if isinstance(group, str):
      await self._run_stage( group )

    elif isinstance(group, ParallelGroup):
      await self._run_parallel_group(group)

    else:
      await self._run_serial_group(group)

  #-----------------------------------------------------------------------------
  async def _run( self ):
    """Begin workflow execution

    Returns
    -------
    None
    """

    if not self._configured:
      raise ValueError("Workflow never configured")

    if self._opened:
      raise ValueError("Workflow already opened")

    self._opened = True

    if self._failed:
      return

    if not osp.exists(self._workdir):
      os.makedirs(self._workdir)

    if not osp.exists(self._rundir):
      os.makedirs(self._rundir)

    await self._run_group(self._run_order)

  #-----------------------------------------------------------------------------
  def _run_wait( self ):
    import trio

    results = trio.run( self._run )

    return results

  #+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
  async def run( self, **kwargs ):

    await self._config( **kwargs )

    return await self._run()


  #-----------------------------------------------------------------------------
  def run_wait( self, **kwargs ):
    import trio
    from functools import partial

    with filter_traceback():

      results = trio.run( partial( self.run, **kwargs ) )

    return results
