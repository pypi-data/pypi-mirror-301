
import os
import os.path as osp
import re
import subprocess
import shutil
import shlex
from timeit import default_timer as timer

import logging
log = logging.getLogger(__name__)

from partis.utils import (
  odict,
  adict,
  ModelHint,
  ModelError,
  LogListHandler )

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
  PJCEvaluated,
  BoolPrim,
  IntPrim,
  FloatPrim,
  StrPrim,
  PathPrim,
  SeqPrim,
  MapPrim,
  UnionPrim,
  PassPrim,
  StructValued,
  MapValued,
  SchemaError,
  SeqValued,
  schema_declared,
  SchemaModule )

from .query import (
  nwl_query_type_casters,
  nwl_query_bases )

from .allocation import RunAllocation
from .inputs import EvaluatedInputEnabled

Env = MapPrim(
  doc = """Environment variables set for tool run

    .. note::

      All environment variable names are first sanitized to contain only
      alpha|digit|underscore, with runs of other characters replaced by a
      single underscore '_'.""",
  item = StrPrim(),
  default_val = dict() )


#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
enabled_declared = schema_declared( tag = 'enabled_input' )

class EnabledInput( StructValued ):
  """Tool enabled input
  """

  schema = dict(
    declared = enabled_declared,
    default_val = optional )

  enabled = BoolPrim(
    doc = "Marks the input as enabled if True, disabled if False",
    default_val = optional,
    evaluated = EvaluatedInputEnabled )

  child = UnionPrim(
    default_val = optional,
    cases = [
      SeqPrim(item = enabled_declared),
      MapPrim(item = enabled_declared) ])

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
class CheckedFile( StructValued ):
  schema = dict(
    tag = 'checked_file',
    doc = "File that is checked for existing",
    default_val = derived )

  name = StrPrim(
    doc = "Name of the file in the tool results",
    default_val = "",
    max_lines = 1 )

  path = PathPrim(
    default_val = "" )

  checked = StrPrim(
    restricted = [ "no", "found", "missing" ],
    default_val = "no" )

  #+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
  def missing(self):
    if self.path._explicit:
      self.checked = "found" if self.path.exists() else "missing"

    return self.checked == "missing"

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
class QueryDep( CheckedFile ):
  schema = dict(
    tag = 'file_dep',
    doc = "Tool input file dependency",
    default_val = derived )

  base = StrPrim(
    default_val = "",
    restricted = [ "", *nwl_query_bases ] )

  path = PathPrim(
    default_val = "" )

  var = StrPrim(
    default_val = "",
    pattern = r"[\w\-]+(\.[\w\-]+)*",
    max_lines = 1 )

  cast_type = StrPrim(
    restricted = [ "", *nwl_query_type_casters.keys() ],
    default_val = "" )

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
class ToolRuntime( RunAllocation ):
  schema = dict(
    tag = 'runtime',
    doc = "Tool runtime information",
    default_val = derived )

  success = BoolPrim(
    doc = "Flag for whether the tool ran and closed successfully",
    default_val = False )

  startdir = PathPrim(
    doc = "Directory from which the tool resolves input file paths relative to starting directory.",
    default_val = "" )

  workdir = PathPrim(
    doc = "Directory from which the tool resolves input file paths relative to workflow directory.",
    default_val = "" )

  host = StrPrim(
    doc = """The local `hostname` or fully qualified domain name
    of the machine where the tool was run.

    .. note::

      If the tool was run with more than one allocated node, this will
      be the hostname of only the node on which the run script was executed.""",
    default_val = "",
    max_lines = 1 )

  nodes = SeqPrim(
    doc = """List of hostnames that are allocated for running multiple processes
      """,
    item = StrPrim(
      max_lines = 1 ),
    default_val = list() )

  threads_per_process = IntPrim(
    doc = """Maximum number of logical threads.

    Computed from allocated ``threads_per_cpu * cpus_per_process``""",
    min = 1,
    default_val = 1 )

  pid = IntPrim(
    doc = "The process id of the primary process running the tool on the `runhost`",
    default_val = 0 )

  cmd_index = IntPrim(
    doc = "Index of last attempted command",
    default_val = -1 )

  cmd_id = StrPrim(
    doc = "ID (key) of last attempted command",
    default_val = optional,
    max_lines = 1 )

  mpiexec = SeqPrim(
    doc = """List of arguments to execute a program within MPI, if available.

      This will be set, and the `{np}` variable in the original format strings
      will be replaced with the current value of `processes`, only if
      `processes > 1`.
      The arguments may be taken from the environment variable `NWL_MPIEXEC`,
      for example:

      .. code-block:: bash

        export NWL_MPIEXEC='mpirun -np {np:d} -host {nodes:s}'""",
    item = StrPrim(
      max_lines = 1 ),
    default_val = list() )

  query_deps = SeqPrim(
    item = QueryDep,
    default_val = list() )

  inputs_enabled = EnabledInput

  input_files = SeqPrim(
    item = CheckedFile,
    default_val = list() )

  output_files = SeqPrim(
    item = CheckedFile,
    default_val = list() )

  signals = MapPrim(
    doc = """Signals received by tool runtime

      The value is the number of times the given signal was received.
      """,
    item = IntPrim(
      default_val = 0 ),
    default_val = dict() )
