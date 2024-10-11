import os
import os.path as osp

import logging
log = logging.getLogger(__name__)

from urllib.parse import (
  urlparse,
  parse_qs )

from partis.schema import (
  SchemaEvaluationError,
  ProviderSupport,
  Provider,
  Evaluated,
  SchemaHint,
  SchemaError,
  SchemaDetectionError,
  Loc,
  PathValued,
  is_bool,
  is_numeric,
  is_string,
  is_sequence,
  is_mapping,
  is_schema_prim,
  UnionPrim )

from partis.schema.serialize import (
  yaml,
  json )

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
nwl_query_type_casters = {
  'bool' : bool,
  'int' : int,
  'float' : float,
  'string' : str,
  'file' : PathValued,
  'dir' : PathValued,
  'struct' : lambda v: v,
  'list' : lambda v: v }

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
nwl_query_bases = [ 'startdir', 'workdir', 'workflow', 'rundir', 'tool' ]

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
class QueryEvaluationError( SchemaEvaluationError ):
  pass

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
class NWLQueryProvider( Provider ):
  """Evaluates NWL query scheme

  The query scheme may be one of three types:

  * ``nwl`` - Values stored in a tool result (including the current tool).
  * ``nwl+yaml`` - Values stored in any YAML file.
  * ``nwl+json`` - Values stored in any JSON file.
  * ``nwl+path`` - Resolve a file/directory path relative to one of the 'base' paths.

  The path is relative to a specified 'base', which may be one of the following:

  * ``startdir`` - Relative to the original starting directory.
  * ``workdir`` - Relative to the current working directory.
  * ``rundir`` - Relative to the current run directory.
  * ``workflow`` - Relative to the current workflow.
  * ``tool`` - Relative to the current tool.

  The query must specify a variable name to be extracted from the data at
  the given path.
  The variable name supports dot '.' notation, denoting a value nested in
  hierarchical structure separating the mapping keys or sequence indices.

  Example
  -------

  For a file in the working directory.

  .. code-block:: yaml
    :caption: some_file.yml

    a:
      - x: 1
        y: 2
      - z: 3
    b: Some Text


  * ``$nwl+yaml:workdir/some_file.yml?var=a.0.x`` -> ``1``
  * ``$nwl+yaml:workdir/some_file.yml?var=a.0.y`` -> ``1``
  * ``$nwl+yaml:workdir/some_file.yml?var=a.1.z`` -> ``3``
  * ``$nwl+yaml:workdir/some_file.yml?var=b`` -> ``'Some Text'``

  """

  TAG_NWL_RES = '$nwl:'
  TAG_NWL_YAML = '$nwl+yaml:'
  TAG_NWL_JSON = '$nwl+json:'
  TAG_NWL_PATH = '$nwl+path:'

  #-----------------------------------------------------------------------------
  def __init__( self ):
    super().__init__()

    self._result_files = dict()
    self._yaml_files = dict()
    self._json_files = dict()

    self._p_supported = dict(
      nwl_res = ProviderSupport(
        name = "Queries value from NWL result file",
        lexer = 'text',
        doc = f"escaped string: `{self.TAG_NWL_RES} ...`" ),
      nwl_yaml = ProviderSupport(
        name = "Queries value from generic YAML file",
        lexer = 'text',
        doc = f"escaped string: `{self.TAG_NWL_YAML} ...`" ),
      nwl_json = ProviderSupport(
        name = "Queries value from generic JSON file",
        lexer = 'text',
        doc = f"escaped string: `{self.TAG_NWL_JSON} ...`" ),
      nwl_path = ProviderSupport(
        name = "Resolve a file/directory path",
        lexer = 'text',
        doc = f"escaped string: `{self.TAG_NWL_PATH} ...`" ) )

  #-----------------------------------------------------------------------------
  @property
  def supported( self ):
    return self._p_supported

  #-----------------------------------------------------------------------------
  def check( self, src ):

    if isinstance( src, str ):

      if src.startswith(self.TAG_NWL_RES):
        return self.supported['nwl_res'], src[len(self.TAG_NWL_RES):]

      elif src.startswith(self.TAG_NWL_YAML):
        return self.supported['nwl_yaml'], src[len(self.TAG_NWL_YAML):]

      elif src.startswith(self.TAG_NWL_JSON):
        return self.supported['nwl_json'], src[len(self.TAG_NWL_JSON):]

      elif src.startswith(self.TAG_NWL_PATH):
        return self.supported['nwl_path'], src[len(self.TAG_NWL_PATH):]

    return None


  #-----------------------------------------------------------------------------
  def escaped( self, support, src ):
    if support is self.supported['nwl_res']:
      return self.TAG_NWL_RES + src

    elif support is self.supported['nwl_yaml']:
      return self.TAG_NWL_YAML + src

    elif support is self.supported['nwl_json']:
      return self.TAG_NWL_JSON + src

    elif support is self.supported['nwl_path']:
      return self.TAG_NWL_PATH + src

    raise ValueError(
      f"`support` must be one of {self.supported.values()}: {support}")

  #-----------------------------------------------------------------------------
  def parse_uri(self, *,
    uri,
    rundir,
    workdir,
    startdir ):

    res = urlparse( uri )

    authority = res.netloc
    path = res.path.split('/')
    query = parse_qs(res.query)

    if authority:
      raise QueryEvaluationError(
        f"NWL query does not support specifying an authority, '{authority}'"
        ". Leading '//' should not be added before path"
        f": {uri}")

    if len(path) == 0:
      raise QueryEvaluationError(
        f"NWL query must have a non-empty path: {uri}")

    base = path[0]
    path = path[1:]

    file = None
    var = None
    cast_type = None

    if not base:
      raise QueryEvaluationError(
        f"NWL query does not support absolute paths"
        f". Leading '/' should not be added before path"
        f": {uri}" )

    if 'var' in query:
      if len(query['var']) != 1:
        raise QueryEvaluationError(
          f"NWL query must specify '?var=name': {uri}")

      var = query['var'][0]

    if 'type' in query:
      if len(query['type']) != 1:
        raise QueryEvaluationError(
          f"NWL query must specify '?type=name': {uri}")

      cast_type = query['type'][0]

      if cast_type not in nwl_query_type_casters:
        types = list(nwl_query_type_casters.keys())

        raise QueryEvaluationError(
          f"NWL query 'type' must be one of {types}: {uri}")

    if base not in nwl_query_bases:
      raise QueryEvaluationError(
        f"NWL query base path must be one of {nwl_query_bases}: {base}")

    if base in [ 'rundir', 'tool' ]:

      file = rundir.joinpath(*path)

    elif base in [ 'startdir' ]:
      file = startdir.joinpath(*path)

    elif base in [ 'workdir', 'workflow' ]:

      file = workdir.joinpath(*path)

    assert file is not None

    if base in ['tool', 'workflow']:
      if osp.basename(file) != 'nwl.results.yml':
        file = osp.join( file, 'nwl.results.yml' )

    return base, file, var, cast_type

  #-----------------------------------------------------------------------------
  def eval( self,
    schema,
    src,
    loc = None,
    locals = None,
    module = None,
    logger = None ):

    res = self.check( src )

    if res is None:
      raise QueryEvaluationError(f"Not a valid NWL query: {src}")

    if locals is None:
      raise QueryEvaluationError(f"'locals' required to evaluate: {src}")

    obj = locals._
    rundir = locals._.runtime.rundir
    workdir = locals._.runtime.workdir
    startdir = locals._.runtime.startdir

    support, uri = res

    base, file, var, cast_type = self.parse_uri(
      uri = uri,
      rundir = rundir,
      workdir = workdir,
      startdir = startdir )

    if not osp.exists(file):
      raise QueryEvaluationError(f"NWL query source file/directory not found: {uri} -> {file}")

    if var is None and support is not self.supported['nwl_path']:
      _scheme = self.escaped(support, '')

      raise QueryEvaluationError(
        f"NWL query must specify '?var=name' for scheme '{_scheme}': {uri}")

    if support is self.supported['nwl_path']:
      return file

    if not osp.isfile(file):
      # NOTE: the remaining query types need to actually read in the file
      raise QueryEvaluationError(f"NWL query source is not a file: {uri} -> {file}")

    if support is self.supported['nwl_res']:

      if base in [ 'rundir', 'tool' ]:
        # simply use the current result state instead of reading from file
        return self.get_var(
          schema = schema,
          loc = 'tool',
          obj = obj,
          var = var,
          dir = rundir,
          cast_type = cast_type )

      return self.get_result_variable(
        schema = schema,
        file = file,
        var = var,
        dir = osp.dirname(file),
        cast_type = cast_type )

    elif support is self.supported['nwl_yaml']:

      return self.get_yaml_variable(
        schema = schema,
        file = file,
        var = var,
        dir = workdir,
        cast_type = cast_type )

    elif support is self.supported['nwl_json']:

      return self.get_json_variable(
        schema = schema,
        file = file,
        var = var,
        dir = workdir,
        cast_type = cast_type )

    raise QueryEvaluationError(f"Missing NWL query support case: {support}")


  #-----------------------------------------------------------------------------
  def get_result_variable( self, *,
    schema,
    file,
    var,
    dir,
    cast_type ):
    """Queries value from NWL result file
    """

    if file in self._result_files:
      results = self._result_files[ file ]

    else:

      try:
        results = yaml.load(
          file,
          loc = file,
          detect_schema = True )

      except SchemaDetectionError as e:
        results = yaml.load(
          file,
          loc = file )

      self._result_files[ file ] = results

    return self.get_var(
      schema = schema,
      loc = file,
      obj = results,
      var = var,
      dir = dir,
      cast_type = cast_type )

  #-----------------------------------------------------------------------------
  def get_yaml_variable( self, *,
    schema,
    file,
    var,
    dir,
    cast_type ):
    """Queries value from YAML file
    """

    if file in self._yaml_files:
      results = self._yaml_files[ file ]

    else:

      results = yaml.load(
        file,
        loc = file )

      self._yaml_files[ file ] = results

    return self.get_var(
      schema = schema,
      loc = file,
      obj = results,
      var = var,
      dir = dir,
      cast_type = cast_type )

  #-----------------------------------------------------------------------------
  def get_json_variable( self, *,
    schema,
    file,
    var,
    dir,
    cast_type ):
    """Queries value from JSON file
    """

    if file in self._json_files:
      results = self._json_files[file]

    else:

      results = json.load(
        file,
        loc = file  )

    return self.get_var(
      schema = schema,
      loc = file,
      obj = results,
      var = var,
      dir = dir,
      cast_type = cast_type )

  #-----------------------------------------------------------------------------
  def get_var( self, *,
    schema,
    loc,
    obj,
    var,
    dir,
    cast_type ):

    value = obj
    parts = var.split( '.' )

    for i, part in enumerate(parts):
      p = '.'.join( parts[:(i+1)] )

      if is_mapping( value ):
        if part not in value:
          raise QueryEvaluationError(f"Result value `{var}` not found: {loc}")

        value = value[ part ]

      elif is_sequence( value ):
        part = int( part )

        if part >= len( value ):
          raise QueryEvaluationError(f"Result value `{var}` not found: {loc}")

        value = value[ part ]

      else:
        raise QueryEvaluationError(f"Result value `{var}` not found: {loc}")


    if cast_type is None and isinstance( value, PathValued ):
      cast_type = 'file'

    if cast_type in ['dir', 'file', 'string'] and is_mapping( value ):

      # NOTE: for string, this makes the assumption that the source value, if it
      # contains a 'path' key, is the desired value as a file path.

      # NOTE: for file or dir, only the `path` string is stored, which will be
      # assigned to the struct_proxy

      if 'path' in value:
        value = value['path']

        # TODO: there really needs to be a better way of differentiating paths
        # from strings, and handling whether they need to be resolved relative
        # to particular directories
        if isinstance(value, (str, bytes, os.PathLike)):
          value = os.fspath(value)

          if len(value) > 0 and not osp.isabs( value ):
            rundir = obj.get('runtime', {}).get('rundir', dir)

            log.debug(SchemaHint(
              f"Resolved relative path: {rundir} -> {value}",
              hints = [
                SchemaHint("rundir", data = rundir),
                SchemaHint("path", data = value) ]))

            value = osp.join( rundir, value )

    value = self.cast_type(
      schema = schema,
      value = value,
      cast_type = cast_type )

    if cast_type in ['dir', 'file']:

      # if not isinstance(value, (str, bytes, os.PathLike)):
      #   raise QueryEvaluationError(
      #     f"Result value for `{var}` is not path-like: {value}, {loc}")

      if value._explicit and not value.is_absolute():
        rundir = PathValued(obj.get('runtime', {}).get('rundir', dir))

        log.debug(SchemaHint(
          f"Resolved relative path: {rundir} -> {value}",
          hints = [
            SchemaHint("rundir", data = rundir),
            SchemaHint("path", data = value) ]))

        value = rundir/value

    return value

  #-----------------------------------------------------------------------------
  def cast_type( self,
    schema,
    value,
    cast_type ):

    if cast_type:
      # use the type given in the query to cast the value before validating
      # with the schema
      if cast_type not in nwl_query_type_casters:
        raise QueryEvaluationError(
          f"Query result `type=` must be one of {nwl_query_type_casters.keys()}: {type}" )

      return nwl_query_type_casters[cast_type]( value )


    if not isinstance( schema, UnionPrim ):
      # use the target schema decoded type to attempt to cast to the correct type
      valued_type = schema.schema.valued_type

      return valued_type(value)._encode


    return value


#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
nwl_query_provider = NWLQueryProvider()

class NWLQueryEvaluated( Evaluated, provider = nwl_query_provider ):
  pass
