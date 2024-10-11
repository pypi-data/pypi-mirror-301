
import re
import sys
import os
import os.path as osp
import tempfile
import shutil
import subprocess
import zipfile

import pprint
import atexit


import trio

from partis.utils.async_trio import (
  aval )

from partis.utils import (
  getLogger,
  ModelError,
  ModelHint,
  VirtualEnv,
  hint_level_num,
  hint_level_name )

log = getLogger(__name__)

from partis.pyproj import (
  dist_targz,
  norm_dist_name,
  norm_dist_filename,
  join_dist_filename )

from partis.schema.serialize.yaml import (
  load,
  dump )

from partis.schema import (
  SchemaHint,
  SchemaError,
  Loc )

from partis.nwl import (
  Tool,
  NWLToolPkg )

class ToolPkgError( ModelError ):
  pass

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
module_dir =  osp.dirname( osp.abspath(__file__) )
tmpl_dir = osp.join( module_dir, "pkg_tmpl" )

mod_name_exclude = [
  'inputs',
  'outputs',
  'commands',
  'results',
  'load_tool',
  'source',
  'tool',
  'sys',
  'AliasMetaFinder' ]

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
async def run_cmd( args, logger, **kwargs ):

  build_ret = await trio.run_process(
    command = args,
    capture_stdout = True,
    capture_stderr = True,
    check = False,
    **kwargs )

  out = build_ret.stdout.decode('ascii', errors = 'replace')
  err = build_ret.stderr.decode('ascii', errors = 'replace')

  if out:
    logger.info( out )

  if err:
    logger.error( err )

  if build_ret.returncode != 0:

    raise subprocess.CalledProcessError(
      build_ret.returncode,
      build_ret.args,
      output = build_ret.stdout,
      stderr = build_ret.stderr )

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
async def build( *,
  pkg_file = None,
  tool_file = None,
  outdir = None,
  docdir = None,
  logger = None,
  tmpdir = None,
  cleanup = True,
  build_docs = True ):

  if logger is None:
    logger = log

  if outdir is None:
    outdir = os.getcwd()

  if docdir is None:
    docdir = outdir

  outdir = osp.realpath(outdir)
  docdir = osp.realpath(docdir)

  if not osp.exists(outdir):
    os.makedirs( outdir )

  if bool(pkg_file) == bool(tool_file):
    raise ToolPkgError(f"Must specify only one of `pkg_file` or `tool_file`")

  if pkg_file:

    pkg_file = osp.abspath( pkg_file )
    pkg_dir = osp.dirname( pkg_file )

    tool_pkg = load(
      file = pkg_file,
      schema = NWLToolPkg )

  else:

    tool_file = osp.abspath( tool_file )
    pkg_dir = osp.dirname( tool_file )

    tool_pkg = NWLToolPkg()
    tool_pkg.info.name = norm_dist_filename( 'nwlpkg_' + osp.basename( tool_file ).rsplit('.', 1)[0] )
    tool_pkg.tools.append( tool_file )

  pkg_name = norm_dist_name( tool_pkg.info.name )
  pkg_version = '.'.join([str(v) for v in tool_pkg.info.version ])
  pkg_file_name = norm_dist_filename( pkg_name )

  tools = list()
  tool_names = list()
  py_deps = list()
  include_files = list()

  build_dir = tempfile.mkdtemp( dir = tmpdir )

  data_dir = osp.join( build_dir, 'data' )
  mods_dir = osp.join( build_dir, 'mods' )

  os.makedirs(data_dir)
  os.makedirs(mods_dir)

  with open(osp.join(mods_dir, '__init__.py'), 'w') as fp:
    pass

  mods_src = dict()
  data_src = dict()

  try:
    build_dir = osp.abspath(build_dir)

    logger.debug( f'Temporary staging directory: {build_dir}' )

    for tool_file in tool_pkg.tools:
      file = tool_file.path
      tool_name = norm_dist_filename( osp.basename( file ).rsplit('.', 1)[0] )

      tool_names.append( tool_name )

      if not osp.isabs( file ):
        file = osp.join( pkg_dir, file )

      file_dir = osp.dirname( file )

      loc = Loc( filename = file )

      # output tool directory
      tool_dir = osp.join( build_dir, tool_name )


      ofile = osp.join( tool_dir, 'tool.yml' )

      # copy base package template
      shutil.copytree(
        osp.join( tmpl_dir, 'tool' ),
        tool_dir )

      shutil.copyfile(
        osp.join( tmpl_dir, 'partis_nwl_ext.py' ),
        osp.join( build_dir, 'partis_nwl_ext.py' ) )


      # NOTE: validates and restructures the data, filling in default values and
      # struct proxies, taking the load off of the less-capable down line parsers
      tool = load(
        file = file,
        schema = Tool )

      # validates the schemas generated from the tool definition
      results_schema = tool.results_schema()

      # update the qualified tool name to the module in this package
      tool.qualname = '.'.join([pkg_file_name, tool_name])

      hints = tool.lint( results_schema() )

      if hints:
        error_num = hint_level_num('error')
        hint_errors = [ hint for hint in hints if hint.level_num >= error_num ]
        hint_warns = [ hint for hint in hints if hint.level_num < error_num ]

        if hint_warns:
          max_num = max([hint.level_num for hint in hint_warns])

          logger.log( max_num, ModelHint(
            f"Tool expression linting {hint_level_name(max_num)}",
            loc = loc,
            hints = hint_warns ) )

        if hint_errors:
          raise ToolPkgError(
            f"Tool expression linting ERROR",
            loc = loc,
            hints = hint_errors )

      tools.append(tool)

      mod_name = None
      mod_path = tool.resources.python.module.path

      py_deps.extend( tool.resources.python.dependencies )

      if mod_path:

        if not osp.isabs( mod_path ):
          # module relative to original tool directory
          mod_path = osp.join( file_dir, mod_path )

        if osp.exists( mod_path + '.py' ):
          # module is a single python file
          # NOTE: if mod_path already ended with .py, it will be handled without
          # adding the extension
          mod_path = mod_path + '.py'

        if not osp.exists( mod_path ):
          raise ToolPkgError(
            f"Module path not found: {mod_path}",
            loc = loc )


        fname = osp.basename(mod_path)
        mod_name = fname

        if mod_name.endswith('.py'):
          mod_name = mod_name[:-3]

        if mod_name in mod_name_exclude:
          raise ToolPkgError(
            f"Module name cannot be any of {mod_name_exclude}: {mod_name}",
            loc = loc )

        if mod_name in mods_src:
          # module with same name already defined by another tool in the package
          _mod_path = mods_src[mod_name]

          if _mod_path != mod_path:
            # check if it is the same file. If not, there is a name conflict
            raise ToolPkgError(
              f"Modules with the same qualified name `{mod_name}` included by two tools: {_mod_path} != {mod_path}",
              loc = loc )

        mods_src[mod_name] = mod_path

        # store only path relative to the tool directory
        tool.resources.python.module = fname

      for name, data in tool.resources.static.items():
        data_path = data.path

        if not osp.isabs( data_path ):
          # data relative to original tool directory
          data_path = osp.join( file_dir, data_path )

        if not osp.exists( data_path ):
          raise ToolPkgError(
            f"Static data path not found: {data_path}",
            loc = loc )

        if name in data_src:
          _data_path = data_src[name]

          if _data_path != data_path:
            raise ToolPkgError(
              f"Static data with the same qualified name `{name}` included by two tools: {_data_path} != {data_path}",
              loc = loc )

        data_src[name] = data_path


        if osp.isfile( data_path ):

          # store only path relative to the tool's data directory
          fname = osp.basename(data_path)
          tool.resources.static[name] = '/'.join([name, fname])

        elif osp.isdir( data_path ):

          # store only path relative to the tool's data directory
          tool.resources.static[name] = name

        else:
          raise ToolPkgError(
            f"Data path not a file or directory: {data_path}",
            loc = loc )


      if mod_name:
        with open( osp.join(tool_dir, '__init__.py'), 'a') as fp:
          # NOTE: the module should not be directly imported into the tool
          # sub-module, since it will immediatly execute the module and all
          # dependencies, and does not obey the relative import symantics.
          # fp.write(f"\nfrom ..mods import {mod_name}")

          # NOTE: this "redirects" the import of module to the shared 'mods' directory
          fp.write(
            f"\nsys.meta_path.insert(0, AliasMetaFinder(\n"
            f"  '{pkg_file_name}.mods.{mod_name}', \n"
            f"  '{pkg_file_name}.{tool_name}.{mod_name}'))\n")

      dump(ofile, tool)

      tool_file.path = '/'.join([ tool_name, 'tool.yml' ])

      for f in os.listdir(tool_dir):
        if f.endswith('.rst'):
          f = osp.join( tool_dir, f )

          with open( f, 'r' ) as fp:
            content = fp.read()

          content = content.replace( '$__tool_doc__',
            tool.tool_doc() )

          content = content.replace( '$__pkg_name__', pkg_file_name )
          content = content.replace( '$__tool_name__', tool_name )

          with open( f, 'w' ) as fp:
            fp.write(content)

      logger.success(f'Validated tool definition: {file}')

    dump(
      osp.join( build_dir, 'nwl_pkg.yml' ),
      tool_pkg )

    with open( osp.join( tmpl_dir, 'pyproject.toml' ), 'r' ) as fp:
      pptoml_str = fp.read()

    pptoml_str = pptoml_str.replace( '$__name__',
      pkg_name )

    pptoml_str = pptoml_str.replace( '$__pkg_name__',
      pkg_file_name )

    pptoml_str = pptoml_str.replace( '$__description__',
      tool_pkg.info.label )

    pptoml_str = pptoml_str.replace( '$__version__',
      pkg_version )

    pptoml_str = pptoml_str.replace( '$__author_name__',
      re.sub('[\,]+', '', tool_pkg.info.author.name ) )

    pptoml_str = pptoml_str.replace( '$__author_email__',
      tool_pkg.info.author.email )

    py_deps_str = (
      'run = [\n'
      + ',\n'.join([
        f'  "{d}"' for d in py_deps ])
      + ' ]' )

    pptoml_str = pptoml_str.replace( '$__run_deps__',
      py_deps_str )


    with open( osp.join( build_dir, 'pyproject.toml' ), 'w' ) as fp:
      fp.write(pptoml_str)

    with open( osp.join( build_dir, '__init__.py' ), 'w' ) as fp:
      fp.write(f'"""{tool_pkg.info.doc}"""\n')

      for tool_name in tool_names:
        fp.write(f"from . import {tool_name}\n")

      mods = ', '.join(tool_names)

      fp.write(f"tools = [ {mods} ]\n")

    with open( osp.join( build_dir, 'index.rst' ), 'w' ) as fp:

      fp.write( '\n'.join([
        tool_pkg.pkg_doc(),
        '',
        '.. toctree::',
        '  :maxdepth: 2',
        '',
        *[ f'  {tool.info.label} <./{name}/index>'
          for tool, name in zip(tools, tool_names) ] ] ) )

    shutil.copytree(
      osp.join( tmpl_dir, 'doc' ),
      osp.join( build_dir, 'doc' ) )


    #...........................................................................
    for mod_name, mod_path in mods_src.items():

      fname = osp.basename(mod_path)
      dst = osp.join( mods_dir, fname )

      if osp.isfile( mod_path ):

        shutil.copyfile( mod_path, dst )

      elif osp.isdir( mod_path ):

        if not osp.exists( osp.join( mod_path, '__init__.py' ) ):
          raise ToolPkgError(
            f"Module path directory does not contain '__init__.py': {mod_path}" )

        shutil.copytree(
          mod_path,
          dst )

      else:
        raise ToolPkgError(
          f"Module path not a file or directory: {mod_path}" )

    #...........................................................................
    for data_name, data_path in data_src.items():

      # output data directory
      dst_dir = osp.join( data_dir, data_name )

      if osp.isfile( data_path ):

        if not osp.exists( dst_dir ):
          os.makedirs( dst_dir )

        fname = osp.basename(data_path)

        dst = osp.join( dst_dir, fname )

        shutil.copyfile( data_path, dst )

      elif osp.isdir( data_path ):

        shutil.copytree(
          data_path,
          dst_dir )

      else:
        raise ToolPkgError(
          f"Data path not a file or directory: {data_path}" )

    build_args = [
      'python3',
      '-m',
      'build',
      '--wheel',
      '--no-isolation',
      '-o',
      outdir,
      build_dir ]

    await run_cmd(
      build_args,
      logger,
      env = {
        **os.environ,
        'PIP_NO_BUILD_ISOLATION' : 'True' } )

    logger.success(f'Finished building tool package.')

    if build_docs:
      if not osp.exists(docdir):
        os.makedirs( docdir )

      with tempfile.TemporaryDirectory() as dtemp:

        venv = VirtualEnv(
          path = osp.join( dtemp, 'vtemp' ),
          inherit_site_packages = True,
          args = ['--without-pip'],
          logger = logger )

        await venv.trio_install([
            # not going to upgrade pip here, and may fail when pip is not installed in
            # the virtual environment
            '--disable-pip-version-check',
            # no user interaction
            '--no-input',
            '--find-links',
            outdir,
            f"{pkg_name}[doc]" ],
          env = {
            **os.environ,
            'PIP_NO_BUILD_ISOLATION' : 'True' })

        doctrees = osp.join( build_dir, '.doctrees' )
        dist_name = join_dist_filename( [pkg_file_name, pkg_version] ) + '-doc'

        build_args = [
          'python3',
          '-m',
          'sphinx.cmd.build',
          '-c',
          osp.join(build_dir, 'doc'),
          '-b',
          'html',
          '-d',
          doctrees,
          build_dir,
          osp.join( build_dir, 'html' ) ]

        await venv.trio_run_log( build_args )

        doc_dist_file = dist_name + '.tar.gz'

      logger.info(f'Packaging documentation: {doc_dist_file}')

      with dist_targz(
        outname = doc_dist_file,
        outdir = docdir ) as dist:

        dist.copytree(
          src = osp.join( build_dir, 'html' ),
          dst = dist_name )

      logger.success(f'Finished building tool documentation.')

  finally:
    if cleanup:
      shutil.rmtree( build_dir )

  return pkg_file_name
