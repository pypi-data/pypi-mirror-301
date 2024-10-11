import os
import os.path as osp
import getpass
import re
import shlex
import shutil
from glob import glob
import hashlib
import pathlib
import platform
import importlib
import subprocess
import networkx as nx

from partis.utils import (
  ModelHint,
  join_attr_path,
  filter_traceback )

from partis.pyproj import (
  norm_dist_filename )

from partis.schema import (
  SchemaDetectionError,
  required,
  optional,
  derived,
  is_bool,
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
  PathValued,
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

from .base import (
  WorkflowError,
  ToolError,
  SerialGroup,
  ParallelGroup )

from .query import (
  NWLQueryProvider,
  NWLQueryEvaluated )

from .inputs import (
  WorkFileInput,
  RunFileInput,
  WorkDirInput,
  RunDirInput )

from .outputs import (
  PathOutput )

from .runtime import (
  EnabledInput,
  CheckedFile,
  QueryDep )

from partis.schema.serialize import (
  yaml,
  json )

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++#
def _get_environ(key, isfile = False, method = None, **kwargs):

  def _f():
    if key not in os.environ:
      return None

    val = os.environ[key]

    if isfile:
      with open(val, 'rb') as fp:
        val = fp.read().decode('utf-8', errors = 'replace')

    if method:
      return method(val, **kwargs)

    return val

  return _f

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++#
def get_environ(val, methods):
  if val is not None:
    return val

  for f in methods:
    val = f()

    if val is not None:
      return val

  return None

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++#
def get_dirs(tool_name, startdir, workdir, rundir):
  if osp.isfile( tool_name ):
    tool_name = osp.basename( tool_name ).rsplit('.', 1)[0]

  pwd = PathValued('.').resolve()

  if startdir is None:
    startdir = pwd

  if workdir is None:
    workdir = startdir

  if rundir is None:
    rundir = tool_name

  startdir = PathValued(startdir)
  workdir = PathValued(workdir)
  rundir = PathValued(rundir)

  if not rundir.is_absolute():
    rundir = workdir / rundir

  startdir = startdir.resolve()
  workdir = workdir.resolve()
  rundir = rundir.resolve()

  return pwd, startdir, workdir, rundir

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++#
def dump_file(*,
  obj,
  fname,
  num,
  log,
  add_hash = True,
  no_defaults = True ):

  fname_tmp = f"{fname}.tmp.{num}"

  with filter_traceback(
    suppress = True,
    filter = Exception,
    log = log,
    msg = f"Failed to write file",
    data = fname ):

    yaml.dump(
      fname_tmp,
      obj,
      add_hash = add_hash,
      no_defaults = no_defaults )

    os.replace(
      fname_tmp,
      fname )

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++#
def expand_environ( var ):
  e_var = osp.expandvars(var)

  while e_var != var:
    var = e_var
    e_var = osp.expandvars(var)

  return shlex.split( e_var )

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++#
def detect_run_with_mpi():

  try:
    from mpi4py import MPI
    return MPI.COMM_WORLD.size > 1

  except ImportError as e:
    pass

  for var in [
    'OMPI_COMM_WORLD_SIZE',
    'PMI_SIZE']:

    if var in os.environ:
      try:
        size = int(os.environ[var])
        return size > 1
      except:
        pass

      return True

  return False

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++#
def get_mpiexec( mpiexec_str = None ):
  if not ( mpiexec_str is None or isinstance(mpiexec_str, str) ):
    return mpiexec_str

  mpiexec = None

  if mpiexec_str is None and 'NWL_MPIEXEC' in os.environ:
    mpiexec_str = os.environ['NWL_MPIEXEC']

  if mpiexec_str is not None:
    mpiexec = expand_environ( mpiexec_str )

  if mpiexec is None:
    exe = shutil.which('mpiexec')

    if exe is not None:
      mpiexec = [
        'mpiexec',
        '-n', '{processes}',
        '-host', '{nodes}' ]

  return mpiexec

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++#
def get_processes( val = None ):

  if val is None:
    for var in [
      'NWL_PROCS',
      'SLURM_NTASKS',
      'PBS_NP' ]:

      if var in os.environ:
        val = os.environ[var]

        if val:
          break

  if val is not None:
    val = int(val)

  return val

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++#
def get_cpus_per_process( val = None ):

  if val is None:
    for var in [
      'NWL_CPUS_PER_PROC',
      'SLURM_CPUS_PER_TASK' ]:

      if var in os.environ:
        val = os.environ[var]

        if val:
          break

  if val is not None:
    val = int(val)

  return val

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++#
def get_threads_per_cpu( val = None ):

  if val is None:
    for var in [
      'NWL_THREADS_PER_CPU' ]:

      if var in os.environ:
        val = os.environ[var]

        if val:
          break

  if val is not None:
    val = int(val)

  return val

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++#
def get_gpus_per_process( val = None ):

  if val is None:
    for var in [
      'NWL_GPUS_PER_PROC',
      'SLURM_GPUS_PER_TASK' ]:

      if var in os.environ:
        val = os.environ[var]

        if val:
          break

  if val is not None:
    val = int(val)

  return val

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++#
def get_runhost( val = None ):

  if val is None:
    val = platform.node()

  return val

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++#
def get_jobhost( val = None ):

  if val is None:

    for var in [
      'NWL_JOBHOST',
      'SLURM_SUBMIT_HOST',
      'PBS_O_HOST']:

      if var in os.environ:
        val = os.environ[var]
        break

  if val is None:
    val = get_runhost()

  return val

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++#
def get_nodelist( val = None ):

  val = get_environ(
    val = val,
    methods = [
      _get_environ('NWL_NODELIST', isfile = False),
      _get_environ('NWL_NODEFILE', isfile = True),
      _get_environ('SLURM_JOB_NODELIST', isfile = False),
      _get_environ('PBS_NODEFILE', isfile = True) ])


  if isinstance(val, str):
    # parse list of node hostnames, handling "compressed" syntax
    # E.G. asdasd-0-[000-1,2,3]

    nodes = []

    for m in re.finditer(r"(?P<prefix>[\w-]+)(\[(?P<ranges>[\d,-]+)\])?", val):
      node = m.group('prefix')
      _ranges = m.group('ranges')

      if _ranges:
        for ab in _ranges.split(','):
          a, _, b = ab.partition('-')

          if b:
            # keep fixed width
            w = len(a)
            for i in range(int(a), int(b)+1):
              nodes.append(f"{node}{i:>0{w}}")

          else:
            nodes.append(f"{node}{a}")

    val = nodes

  if val is None or len(val) == 0:
    # fallback to the runtime host
    val = [get_runhost()]

  return val

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++#
def get_runuser( val = None ):

  if val is None:
    try:
      # Documentation mentions this preferrable to os.getlogin, since this
      # getpass.getuser checks environment variables in addition to the
      # system-level calls.
      # NOTE: There is a chance that this raises an exception if there is no login
      # username available.
      # TODO: document the exception classes that could be raised, and specialize
      # the except clause
      val = getpass.getuser()
    except:
      pass

  return val

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++#
def get_jobuser( val = None ):

  if val is None:

    for var in [
      'NWL_JOBUSER',
      'SLURM_JOB_USER',
      'PBS_O_LOGNAME' ]:

      if var in os.environ:
        val = os.environ[var]
        break

  if val is None:
    val = get_runuser()

  return val

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++#
def get_jobid( val = None ):
  if val is None:
    for var in [
      'NWL_JOBID',
      'SLURM_JOBID',
      'SLURM_JOB_ID',
      'PBS_JOBID' ]:

      if var in os.environ:
        val = os.environ[var]
        break

  return val

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++#
def get_jobname( val = None ):
  if val is None:
    for var in [
      'NWL_JOBNAME',
      'SLURM_JOB_NAME',
      'PBS_JOBNAME' ]:

      if var in os.environ:
        val = os.environ[var]
        break

  return val

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++#
def get_inputs_enabled( val ):
  """Evaluate the 'enabled' expression for given input values
  """
  tag_key = None
  enabled = True
  child = None

  if is_valued_type(val):
    schema = val._schema

    if hasattr(schema, 'tag_key'):
      tag_key = schema.tag_key

    if hasattr(schema, 'schema_origin') and hasattr(schema.schema_origin, 'enabled'):
      enabled = schema.schema_origin.enabled

  if is_sequence( val ):
    child = [
      get_inputs_enabled( v )
      for i, v in enumerate(val) ]

  elif is_mapping( val ):
    child = {
      k : get_inputs_enabled( v )
      for k, v in val.items()
      if k != tag_key }

  return EnabledInput(
    child = child,
    enabled = enabled )

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++#
# def eval_inputs_enabled(*,
#   val,
#   context ):
#   """Evaluate the 'enabled' expression for given input values
#   """
#   tag_key = None

#   if is_valued_type(val):
#     schema = val._schema

#     if hasattr(schema, 'tag_key'):
#       tag_key = schema.tag_key

#     if hasattr(schema, 'schema_origin') and hasattr(schema.schema_origin, 'enabled'):
#       if not schema.schema_origin.enabled._eval( context = context ):
#         return False

#   if is_sequence( val ):
#     return [
#       eval_inputs_enabled(
#         val = v,
#         context = context(
#           schema = schema,
#           parent = val,
#           key = i ) )
#       for i, v in enumerate(val) ]

#   elif is_mapping( val ):
#     return {
#       k : eval_inputs_enabled(
#         val = v,
#         context = context(
#           schema = schema,
#           parent = val,
#           key = k ) )
#       for k, v in val.items()
#       if k != tag_key }

#   else:
#     return True

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++#
def filter_inputs_enabled(*,
  val,
  inputs_enabled ):
  """Filters out all input values that ought to be ignored according after
  evaluating the corresponding 'enabled' expression in the tool inputs section
  """

  assert is_bool(inputs_enabled.enabled)

  if not inputs_enabled.enabled:
    return None


  if is_sequence(val):
    assert is_sequence(inputs_enabled.child)

    return [
      filter_inputs_enabled(
        val = v,
        inputs_enabled = inputs_enabled.child[i] )
      for i, v in enumerate(val) ]

  elif is_mapping(val):
    assert is_mapping(inputs_enabled.child)

    _enabled = {
      k : filter_inputs_enabled(
        val = v,
        inputs_enabled = inputs_enabled.child[k] )
      for k, v in val.items()
      if k in inputs_enabled.child }

    _enabled = {k:v for k,v in _enabled.items() if v}

    return _enabled

  else:
    return val

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++#
def resolve_input_files(
  workdir,
  rundir,
  val ):
  """Resolve input paths relative to the workflow/working directory, or the
  tools run directory, to absolute paths.

  ..note::

    These modifications are done in-place, and do/should *not* perform any operation
    that would require the paths actually exist.
  """

  if isinstance(val, PathValued):
    if val._explicit and not val.is_absolute():
      # NOTE: don't want to resolve RunFile(Dir)Input
      if isinstance(val._schema.schema_origin, (WorkFileInput, WorkDirInput)):
        val = workdir/val
      else:
        val = rundir/val

  elif is_sequence(val):
    for i, v in enumerate(val):
      val[i] = resolve_input_files(
        workdir = workdir,
        rundir = rundir,
        val = v )

  elif is_mapping(val):
    for k, v in val.items():
      val[k] = resolve_input_files(
        workdir = workdir,
        rundir = rundir,
        val = v )

  return val

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++#
def resolve_output_files(
  rundir,
  val ):
  """Resolves output paths relative to the tool's run directory to relative paths.
  Absolute paths that point outside the run directory are left un-changed.

  ..note::

    These modifications are done in-place
  """

  if isinstance( val, PathValued ):
    if (
      isinstance(val._schema.schema_origin, PathOutput)
      and val._explicit
      and val.is_absolute()
      and val.is_relative_to(rundir)):

      # only resolve non-empty paths that point to something within the run directory
      val = val.relative_to(rundir)

  elif is_sequence( val ):
    for i, v in enumerate(val):
      val[i] = resolve_output_files(
        rundir = rundir,
        val = v )

  elif is_mapping( val ):
    for k, v in val.items():
      val[k] = resolve_output_files(
        rundir = rundir,
        val = v )

  return val

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++#
def checked_inout_files(*,
  dir,
  name_path,
  val ):
  """Checks for the existance of input file/dir paths
  """

  files = list()

  if isinstance( val, PathValued ):

    if (
      isinstance(val._schema.schema_origin, (WorkFileInput, WorkDirInput, PathOutput))
      and val._explicit):

      files.append(CheckedFile(
        name = join_attr_path(name_path),
        path = val.resolve()))

  elif is_sequence(val):
    for i, v in enumerate(val):
      files.extend( checked_inout_files(
        dir = dir,
        name_path = name_path + [i],
        val = v ))

  elif is_mapping(val):
    for k, v in val.items():
      files.extend( checked_inout_files(
        dir = dir,
        name_path = name_path + [k],
        val = v ))

  return files

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++#
def get_input_query_deps(
  startdir,
  workdir,
  rundir,
  name_path,
  val ):
  """Checks for input file dependencies needed to evaluate input query expressions
  """

  deps = list()

  if is_valued_type(val) and isinstance(val._src, NWLQueryEvaluated):

    src = val._encode
    provider = val._src._provider

    assert isinstance(provider, NWLQueryProvider)

    _, uri = provider.check(src)

    base, path, var, cast_type = provider.parse_uri(
      uri = uri,
      startdir = startdir,
      rundir = rundir,
      workdir = workdir )

    deps.append(QueryDep(
      name = join_attr_path(name_path),
      base = base,
      path = path,
      var = var,
      cast_type = cast_type ))

  elif isinstance( val, PathValued ):
    # NOTE: It might be possible to check regular file dependencies, but due
    # to default values and ability to 'disable' inputs at runtime, these may
    # cause to insert "false" dependencies that will actually be ignored.
    # However, the method 'checked_inout_files' will account for this when the
    # tool runs
    pass

  elif is_sequence( val ):
    for i, v in enumerate(val):

      deps.extend( get_input_query_deps(
        startdir = startdir,
        workdir = workdir,
        rundir = rundir,
        name_path = name_path + [i],
        val = v ) )

  elif is_mapping( val ):
    for k, v in val.items():

      deps.extend( get_input_query_deps(
        startdir = startdir,
        workdir = workdir,
        rundir = rundir,
        name_path = name_path + [k],
        val = v ) )

  return deps

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++#
def _dep_resolve(order, pending, v, vdeps):
  vdeps = [d for d in vdeps if d not in order]

  if not vdeps:
    # resolved
    order.append(v)
    return True

  pending.append((v,vdeps))

  return False

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++#
def _dep_sort_stable(deps):
  """Simple stable sort of dependencies
  """
  order = SerialGroup()
  avail = [ (str(k), [str(u) for u in v]) for k,v in deps.items() ][::-1]
  pending = list()

  while avail or pending:

    if pending and _dep_resolve(order, pending, *pending.pop()):
      continue

    if not avail:

      pending = [(v, [d for d in vdeps if d not in order]) for v, vdeps in pending ]
      raise WorkflowError(
        "Workflow contains un-resolvable I/O dependencies",
        hints = [f"{v} -> {vdeps}" for v, vdeps in pending] )

    _dep_resolve(order, pending, *avail.pop())

  return order

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++#
def run_order(
  run_serial,
  deps ):
  """

  Parameters
  ----------
  run_serial : bool
    If true, does not assume stages may be run in parallel, even if they do not
    appear to be inter-dependent
  deps : dict[str, list[str]]

  Returns
  -------
  list[ tuple[ list[str], list[set[str]] ] ]
  """

  stages = set(deps.keys())

  for stage, _deps in deps.items():
    missing = [ d for d in _deps if d not in stages ]

    if missing:
      raise WorkflowError(
        f"Stage '{stage}' I/O dependencies must be another workflow stage",
        data = missing )

  if run_serial:
    return _dep_sort_stable(deps)

  graph = nx.DiGraph(deps).reverse()

  try:
    cycle = nx.find_cycle(graph)

    raise WorkflowError(
      "Workflow contains a cycle of I/O dependencies",
      hints = [f"{a} -> {b}" for a,b in cycle] )

  except nx.exception.NetworkXNoCycle as e:
    pass

  comps = list(nx.connected_components(graph.to_undirected()))

  order = ParallelGroup()

  for comp in comps:
    subg = graph.subgraph(comp)
    gens = list(nx.topological_generations(subg))

    order.append( SerialGroup( [ ParallelGroup(g) for g in gens ]) )

  return order

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++#
def run_order_hints(order):
  if isinstance(order, str):
    return order

  if len(order) == 1:
    return run_order_hints(order[0])

  if isinstance( order, ParallelGroup ):
    return ModelHint(
      "Parallel Group:",
      level = 'info',
      hints = [run_order_hints(c) for c in order] )

  return ModelHint(
    "Serial Group:",
    level = 'info',
    hints = [run_order_hints(c) for c in order] )

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++#
def load_results( rundir = None ):
  results_file = "nwl.results.yml"

  if rundir:
    results_file = osp.join( rundir, results_file )

  # ensure plugs reloaded with access to additional search paths
  from partis.schema.plugin import (
    schema_plugins )

  schema_plugins.load_plugins()

  results = yaml.load(
    results_file,
    loc = results_file,
    detect_schema = True )

  return results



#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
def diff_hint( loc, ref, val ):

  if is_sequence(ref):
    if not is_sequence( val ):
      return ModelHint(
        f"Expected a sequence",
        data = val,
        level = 'error',
        loc = loc )

    if len( val ) != len( ref ):
      return ModelHint(
        f"Expected a sequence of length {len(ref)}",
        data = len(val),
        level = 'error',
        loc = loc )

    hints = list()

    for i, v in enumerate(ref):
      _hint = diff_hint( loc(key = i), v, val[i] )

      if _hint is not None:
        hints.append( _hint )

    if len(hints) > 0:
      return ModelHint(
        f"In sequence",
        level = 'error',
        loc = loc,
        hints = hints )

  elif is_mapping( ref ):
    if not is_mapping( val ):
      return ModelHint(
        f"Expected mapping",
        data = val,
        level = 'error',
        loc = loc )

    # if len( val ) != len( ref ):
    #   return ModelHint(f"mapping at `{_path}` length {len(ref)} : {len(val)}")

    hints = list()

    for k, v in ref.items():
      _hint = None

      if k not in val:
        _hint = ModelHint(
          f"Expected key",
          level = 'error',
          data = k,
          loc = loc )

      else:
        _hint = diff_hint( loc(key = k), v, val[k] )

      if _hint is not None:
        hints.append( _hint )

    if len(hints) > 0:
      return ModelHint(
        f"In mapping",
        level = 'error',
        loc = loc,
        hints = hints )

  elif val != ref:
    return ModelHint(
      f"Expected value of `{ref}`",
      level = 'error',
      data = val,
      loc = loc )

  return None
