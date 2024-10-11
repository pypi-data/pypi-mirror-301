# -*- coding: UTF-8 -*-

import os
import os.path as osp
import subprocess
import shutil
from timeit import default_timer as timer

import logging
log = logging.getLogger(__name__)

from partis.utils import (
  odict,
  adict,
  ModelHint,
  ModelError,
  LogListHandler,
  tail )

from partis.schema import (
  required,
  optional,
  derived,
  is_sequence,
  is_mapping,
  is_evaluated,
  is_valued,
  is_valued_type,
  is_optional,
  PyEvaluated,
  BoolPrim,
  IntPrim,
  FloatPrim,
  StrPrim,
  SeqPrim,
  MapPrim,
  UnionPrim,
  StructValued,
  schema_declared,
  EvaluatedContext )

from ..base import (
  ToolError )

from ..log import (
  LogEvent )

from .base import (
  EvaluatedCommands,
  BaseCommandOutput,
  BaseCommand )

from ..context import (
  ArgumentContext )

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
EvaluatedArgument = PyEvaluated.subclass(
  context = ArgumentContext )

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
class StdFile( StructValued ):
  schema = dict(
    tag = 'std_file',
    default_val = derived,
    struct_proxy = 'path' )

  path = StrPrim(
    default_val = "",
    max_lines = 1 )

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
class StdInFile( StdFile ):
  """Standard input file
  """
  schema = dict(
    tag = 'stdin',
    default_val = derived )

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
class StdOutFile( StdFile ):
  """Standard output file
  """
  schema = dict(
    tag = 'stdout',
    default_val = derived )

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
class ProcessCommandOutput( BaseCommandOutput ):
  schema = dict(
    tag = 'process',
    default_val = derived )

  executable = StrPrim(
    doc = """The resolved absolute path to the executable
      Note that this value is computed from the first item in 'args', and
      is given only for reference to allow inspection of what program was run.
      The un-modified 'args' is what was passed directly to the system to create
      the sub-process.""",
    default_val = '',
    max_lines = 1 )

  args = SeqPrim(
    doc = "List of arguments used to execute command",
    item = StrPrim(
      max_lines = 1 ),
    default_val = list() )

  pid = IntPrim(
    doc = "Process id of executed command",
    default_val = 0 )

  stdin = StdInFile

  stdout = StdOutFile

  returncode = IntPrim(
    doc = "A numeric return value of command.",
    default_val = 0 )

  env = MapPrim(
    doc = "Additional environment variables that were set for this command.",
    item = StrPrim(),
    default_val = dict() )

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
class ProcessArgument( StructValued ):
  schema = dict(
    tag = 'process_arg',
    struct_proxy = 'value' )

  value = UnionPrim(
    cases = [
      StrPrim(
        evaluated = EvaluatedArgument,
        max_lines = 1 ),
      SeqPrim(
        item = StrPrim(
          evaluated = EvaluatedArgument,
          max_lines = 1 ) ) ],
    evaluated = EvaluatedArgument )

  label = StrPrim(
    default_val = '',
    max_lines = 1,
    max_cols = 80 )

  doc = StrPrim(
    default_val = '',
    max_lines = 100 )

  enabled = BoolPrim(
    doc = "Marks the argument as enabled if True, disabled if False",
    default_val = True,
    evaluated = EvaluatedCommands )

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
class ProcessCommand( BaseCommand ):
  """Runs a system process
  """

  schema = dict(
    tag = 'process' )

  cwd = StrPrim(
    default_val = '.')

  env = MapPrim(
    doc = "Additional environment variables to set for this command.",
    item = StrPrim(
      doc = "Environment variable",
      evaluated = EvaluatedCommands ),
    default_val = dict(),
    evaluated = EvaluatedCommands )

  args = SeqPrim(
    doc = "List of command arguments used to create process",
    item = ProcessArgument,
    evaluated = EvaluatedCommands,
    default_val = required )

  stdin = StrPrim(
    doc = "Path to standard input file",
    default_val = "",
    evaluated = EvaluatedCommands,
    max_lines = 1 )

  epilog = SeqPrim(
    doc = """List of possible logging after closing command.
      Logs with level 'ERROR' or 'CRITICAL' are used to establish whether a
      command has failed.
      """,
    item = LogEvent,
    default_val = [
      dict(
        msg = "Command failed from non-zero process exit code",
        level = "ERROR",
        enabled = "$expr:py _.command.returncode != 0" ) ] )

  #-----------------------------------------------------------------------------
  def __init__( self, *args, **kwargs ):
    super().__init__(*args, **kwargs)

    self._env = None
    self._args = None
    self._process = None
    self._killed = False

    self._stdin_file = None
    self._stdin_fp = None

    self._stdout_file = None
    self._stdout_fp = None

  #-----------------------------------------------------------------------------
  def _reset( self ):
    super()._reset()

    self._env = None
    self._args = None
    self._process = None
    self._killed = False

    self._stdin_file = None
    self._stdin_fp = None

    self._stdout_file = None
    self._stdout_fp = None

  #-----------------------------------------------------------------------------
  def value_schema( self, name, module = None ):
    return ProcessCommandOutput

  #-----------------------------------------------------------------------------
  def _config( self,
    tool,
    workdir,
    rundir,
    env,
    venv,
    id,
    tool_results,
    timeout = None,
    log = None ):

    super()._config(
      tool = tool,
      workdir = workdir,
      rundir = rundir,
      env = env,
      venv = venv,
      id = id,
      tool_results = tool_results,
      timeout = timeout,
      log = log )

    if self.stdin != "":
      self._stdin_file = f"nwl.cmd.{id}.stdin.txt"

    self._stdout_file = f"nwl.cmd.{id}.stdout.txt"

    self._results.stdin.path = self._stdin_file
    self._results.stdout.path = self._stdout_file

    self._results.env = self.env
    self._env = { **env, **self.env }

    args = list()

    arg_ctx = ArgumentContext(
      results = tool_results,
      static = self._tool.resources.static )

    arg_logger = self._log.getChild('args')

    for arg in self.args:
      if arg.enabled:

        try:

          val = arg.value._eval(
            context = arg_ctx,
            logger = arg_logger )

        except BaseException as e:
          self._log.error( ModelHint(
            msg = "Failed to evaluate argument",
            hints = e ) )

          return

        if is_sequence( val ):
          args.extend( val )
        else:
          args.append( val )

    if len(args) == 0:
      self._log.error(f"No process arguments")
      return

    self._results.args = args

    cmd_exec = args[0]
    cmd_exec_src = shutil.which(cmd_exec)

    if cmd_exec_src is None:
      # TODO: implement a utility function that can report more precisely if
      # the program exists, but maybe the permissions are not set such that
      # it can be executed.
      self._log.error(ModelHint(
        f"Executable does not exist or has in-sufficient permissions",
        data = cmd_exec ))

    else:
      # NOTE: stores the full path to the executable program, resolving symlinks,
      # to allow future inspection, but passes the un-modified argument as given
      # in the tool definition to ensure the command is not modified
      self._results.executable = osp.realpath(cmd_exec_src)


    self._update_result_logs()

    return self._results

  #-----------------------------------------------------------------------------
  def _open( self,
    tool_results ):

    super()._open(
      tool_results = tool_results )


    try:
      if self._stdin_file is not None:
        self._stdin_fp = open( self._stdin_file, "rb" )

      self._stdout_fp = open( self._stdout_file, "wb")

    except BaseException as e:
      self._log.error( ModelHint(
        msg = "Failed to open standard input/output/err files",
        hints = e ) )

    self._update_result_logs()
    if self._failed:
      return

    try:
      args = self._results.args._encode

      self._process = self._venv.Popen(
        args,
        shell = False,
        stdin = self._stdin_fp,
        stdout = self._stdout_fp,
        stderr = subprocess.STDOUT,
        env = self._env,
        cwd = osp.join(self._rundir, self.cwd) )

      self._results.pid = self._process.pid

    except BaseException as e:
      self._log.error( ModelHint(
        msg = "Failed to open process",
        hints = e ) )

  #-----------------------------------------------------------------------------
  def _poll( self,
    tool_results ):

    if self._process is None:
      return self._close(
        tool_results = tool_results )

    # self._log.debug(f"Command polling")

    time_cur = timer()

    try:
      res = self._process.poll()
    except BaseException as e:
      self._log.error( ModelHint(
        msg = f"Failed to poll running process",
        data = self._process.pid,
        hints = e ) )

      return self._close(
        tool_results = tool_results )

    if res is not None:
      self._results.returncode = self._process.returncode
      self._process = None

      return self._close(
        tool_results = tool_results )

    if (
      self._killed
      or self._time_limit is None
      or time_cur <= self._time_limit ):
      return None

    self._log.error( ModelHint(
      f"Killing process, time limit exceeded: {self._timeout} sec",
      data = self._process.pid ) )

    self._process.kill()
    self._killed = True

    return None

  #-----------------------------------------------------------------------------
  def _close( self,
    tool_results ):

    if self._process is not None:
      try:
        self._process.kill()
      except:
        pass

      self._process = None

    if self._stdin_fp is not None:
      try:
        self._stdin_fp.close()
      except:
        pass

      self._stdin_fp = None

    if self._stdout_fp is not None:
      try:
        self._stdout_fp.close()
      except:
        pass

      self._stdout_fp = None

    nlines = 50

    if os.path.exists( self._stdout_file ):

      lines = tail( self._stdout_file, nlines )

      if len( lines ) > 0:
        txt = "\n".join(lines)
        filename = os.path.split( self._stdout_file )[1]

        self._log.info( ModelHint(
          f"last {len( lines )} lines of output",
          data = txt,
          format = 'block',
          loc = filename ) )

    return super()._close(
      tool_results = tool_results )

  #-----------------------------------------------------------------------------
  def lint( self, tool, cmd_id, results ):
    hints = super().lint( tool, cmd_id, results )

    hints.extend( self.args._lint(
      context = ArgumentContext(
        results = results,
        static = tool.resources.static ) ) )


    return hints
