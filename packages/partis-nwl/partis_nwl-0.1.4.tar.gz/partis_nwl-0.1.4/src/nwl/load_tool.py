import os
import os.path as osp
import re
import shlex
import shutil
from glob import glob
import hashlib
import pathlib
import platform
import importlib
import subprocess
import logging
import tempfile

try:
  from importlib.metadata import metadata, requires, PackageNotFoundError

except ImportError:
  from importlib_metadata import metadata, requires, PackageNotFoundError

from packaging.requirements import Requirement
from packaging.specifiers import SpecifierSet
from packaging.markers import Marker

from partis.utils import (
  ModelHint )

from partis.pyproj import (
  norm_dist_filename )

from partis.schema import (
  SchemaDetectionError,
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

from partis.schema.serialize import (
  yaml,
  json )

from partis.nwl.tool_pkg.build import build as build_pkg

from .base import (
  UnionToolWorkflow )

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
async def install_tool_deps(
  tools,
  venv,
  find_links ):

  if find_links is None:
    find_links = list()

  if venv.logger.isEnabledFor( logging.DEBUG ):
    _verbosity = ['-v', '-v', '-v']
  else:
    _verbosity = list()

  _pip_args = [
    # the cache is not safe when changed from multiple processes
    '--no-cache-dir',
    # not going to upgrade pip here
    '--disable-pip-version-check',
    # no user interaction
    '--no-input' ]

  _find_links = list()

  for f in ['.'] + find_links:
    _find_links.extend([
      '--find-links',
      f ])

  # combine requirements of all tool packages
  deps = dict()
  marker_env = {'extra': 'run'}

  for tool in tools:
    pkg_name, _, _ = tool.qualname.partition('.')

    if pkg_name == '':
      reqs = list(tool.resources.python.dependencies)

    else:
      try:
        reqs = requires(pkg_name)
      except PackageNotFoundError as e:
        venv.logger.warning(ModelHint(
          f"Failed to get dependencies for package: {pkg_name}",
          hints = e ))

        reqs = list(tool.resources.python.dependencies)


    for req in reqs:
      req = Requirement(req)

      if req.marker is None or req.marker.evaluate(marker_env):
        _req = deps.setdefault(req.name, Requirement(req.name))
        _req.extras |= req.extras
        _req.specifier &= req.specifier

  deps = [ str(dep) for dep in deps.values() ]

  args = [
    '--upgrade',
    *_verbosity,
    *_find_links,
    *_pip_args,
    *deps ]

  venv.logger.debug(ModelHint(
    "Install arguments",
    hints = args))

  # ensure all tool dependencies are installed
  try:
    await venv.trio_install(
      args,
      env = {
        **os.environ,
        'PIP_NO_BUILD_ISOLATION' : 'True' })

    return deps

  except subprocess.CalledProcessError as e:

    venv.logger.error(ModelHint(
      f"Failed to install tool dependencies",
      hints = e ))

  return None

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
async def load_tool(
  name,
  venv,
  find_links,
  no_deps = False ):

  if find_links is None:
    find_links = list()

  tool_mod = None
  deps_installed = False
  tmpdir = None
  _find_links = list()


  if venv.logger.isEnabledFor( logging.DEBUG ):
    _verbosity = ['-v', '-v', '-v']
  else:
    _verbosity = list()

  _pip_args = [
    # the cache is not safe when changed from multiple processes
    '--no-cache-dir',
    # not going to upgrade pip here, and may fail when pip is not installed in
    # the virtual environment
    '--disable-pip-version-check',
    # no user interaction
    '--no-input' ]


  try:
    if osp.isfile( name ):

      tool = yaml.load(
        file = name,
        schema = UnionToolWorkflow )

      if tool.type != 'tool':
        return tool, None

      tool_name = norm_dist_filename( osp.basename( name ).rsplit('.', 1)[0] )
      pkg_name = f"nwlpkg_{tool_name}"
      _name = f"{pkg_name}.{tool_name}"

      try:
        with venv:
          tool_mod = importlib.import_module(_name)

        name = _name

        tool = tool_mod.tool

        results_schema = tool_mod.results.results

      except ImportError:


        venv.logger.info(f'Building tool package: {name}')

        tmpdir = tempfile.mkdtemp()

        find_links.append( tmpdir )

        pkg_name = await build_pkg(
          tool_file = name,
          outdir = tmpdir,
          logger = venv.logger,
          build_docs = False )

        name = f"{pkg_name}.{tool_name}"

    venv.logger.info(ModelHint(
      f'PIP Links',
      hints = find_links ) )

    for f in ['.'] + find_links:
      venv.logger.info(f"  '{f}'")

      _find_links.extend([
        '--find-links',
        f ])

    try:
      with venv:
        tool_mod = importlib.import_module(name)

      tool = tool_mod.tool

      results_schema = tool_mod.results.results

    except ImportError:
      pass

    if not tool_mod:

      # search current directory for a distribution containing the tool
      pkg_name, _, mod = name.partition('.')

      venv.logger.info(f"Installing tool package: {pkg_name}")

      try:

        await venv.trio_install([
            *_verbosity,
            *_find_links,
            *_pip_args,
            f'{pkg_name}' if no_deps else f'{pkg_name}[run]' ],
          env = {
            **os.environ,
            'PIP_NO_BUILD_ISOLATION' : 'True' })

      except subprocess.CalledProcessError as e:
        venv.logger.error(ModelHint(
          f"Failed to install tool package: {pkg_name}",
          hints = e ))

        return None, None

      deps_installed = not no_deps

      with venv:
        tool_mod = importlib.import_module(name)

      tool = tool_mod.tool

      results_schema = tool_mod.results.results

    tool_dir = osp.dirname( osp.abspath(tool_mod.__file__) )
    data_dir = osp.join( tool_dir, os.pardir, 'data' )

    # update tool resource data paths
    for name, data in tool.resources.static.items():
      data_path = data.path

      if not osp.isabs( data_path ):
        tool.resources.static[name] = osp.join( data_dir, data_path )

    if not ( no_deps or deps_installed ) and len(tool.resources.python.dependencies) > 0:
      # ensure all tool dependencies are installed
      try:
        await venv.trio_install([
            '--upgrade',
            *_verbosity,
            *_find_links,
            *_pip_args,
            *[ str(dep) for dep in tool.resources.python.dependencies ] ],
          env = {
            **os.environ,
            'PIP_NO_BUILD_ISOLATION' : 'True' })

      except subprocess.CalledProcessError as e:

        venv.logger.error(ModelHint(
          f"Failed to install tool dependencies: {name}",
          hints = e ))

        return None, None

  finally:
    if tmpdir:
      shutil.rmtree( tmpdir )

  return tool, results_schema

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
def load_tool_wait( *args, **kwargs ):

  import trio
  from functools import partial

  return trio.run( partial( load_tool, *args, **kwargs ) )
