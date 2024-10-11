import os
import re
import subprocess
import shutil

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
avail_use_pattern = r"^-+ (\S+) \-+$"
avail_use_rec = re.compile( avail_use_pattern, flags = re.M )

avail_mod_pattern = r"(\S+)"
avail_mod_rec = re.compile( avail_mod_pattern )

list_mod_pattern = r"(?P<id>[0-9]+)\)(\t| )(?P<mod>\S+)"
list_mod_rec = re.compile( list_mod_pattern )

#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
MODULECMD = None

def init_modules():

  global MODULECMD

  if 'MODULESHOME' not in os.environ:
    raise ValueError("Environment modules not initialized (no `MODULESHOME` environment variable).")

  MODULECMD = shutil.which('modulecmd')

  if MODULECMD is None:
    raise ValueError(f"`modulecmd` not found")

  if 'MODULEPATH' not in os.environ:
    with open( os.path.join( os.environ['MODULESHOME'], 'init', '.modulespath' ), 'r' ) as f:
      paths = list()

      for line in f.readlines():
        line = re.sub("#.*$", '', line)

        if line != '':
          paths.append(line)

      os.environ['MODULEPATH'] = ':'.join(paths)

  if 'LOADEDMODULES' not in os.environ:
    os.environ['LOADEDMODULES'] = ''

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
class ModuleCmdError( Exception ):
  pass

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
def module(*args):
  """Base command call to environment modules
  """
  if type(args[0]) == type([]):
    args = args[0]
  else:
    args = list(args)
  (output, error) = subprocess.Popen(
    [ MODULECMD, 'python' ] + args,
    stdout = subprocess.PIPE,
    stderr = subprocess.PIPE ).communicate()

  exec( output )

  error = error.decode( 'ascii', errors = 'ignore' )

  return error

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
def module_avail():
  """

  https://modules.readthedocs.io/en/latest/module.html#subcmd-avail

  List all available modulefiles in the current MODULEPATH. All directories in the MODULEPATH are recursively searched for files containing the modulefile magic cookie. If an argument is given, then each directory in the MODULEPATH is searched for modulefiles whose pathname, symbolic version-name or alias match the argument. Argument may contain wildcard characters. Multiple versions of an application can be supported by creating a subdirectory for the application containing modulefiles for each version.

  Symbolic version-names and aliases found in the search are displayed in the result of this sub-command. Symbolic version-names are displayed next to the modulefile they are assigned to within parenthesis. Aliases are listed in the MODULEPATH section where they have been defined. To distinguish aliases from modulefiles a @ symbol is added within parenthesis next to their name. Aliases defined through a global or user specific module RC file are listed under the global/user modulerc section.

  When colored output is enabled and a specific graphical rendition is defined for module default version, the default symbol is omitted and instead the defined graphical rendition is applied to the relative modulefile. When colored output is enabled and a specific graphical rendition is defined for module alias, the @ symbol is omitted. The defined graphical rendition applies to the module alias name. See MODULES_COLOR and MODULES_COLORS sections for details on colored output.

  Module tags applying to the available modulefiles returned by the avail sub-command are reported along the module name they are associated to (see Module tags section).

  A Key section is added at the end of the output in case some elements are reported in parentheses or chevrons along module name or if some graphical rendition is made over some outputed elements. This Key section gives hints on the meaning of such elements.

  The parameter path may also refer to a symbolic modulefile name or a modulefile alias. It may also leverage a specific syntax to finely select module version (see Advanced module version specifiers section below).
  """

  res = module('avail')

  sections = list()

  for m in re.finditer( avail_use_rec, res ):
    dir = os.path.abspath( m.group(1) )
    sections.append( ( dir, m.start(), m.end() ) )

  sections.append( (None, len(res), len(res) ) )

  mods_avail = dict()

  for i in range( len(sections) - 1 ):
    s, s_start, s_end = sections[i]
    _, _start, _end = sections[i+1]

    mods_str = res[s_end:_start]

    mods = list()

    for m in re.finditer( avail_mod_rec, mods_str ):
      mods.append( m.group(1) )

    mods_avail[ s ] = mods

  return mods_avail

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
def module_list():
  """

  https://modules.readthedocs.io/en/latest/module.html#subcmd-list
  List loaded modules.

  Module tags applying to the loaded modules are reported along the module name they are associated to (see Module tags section).

  Module variants selected on the loaded modules are reported along the module name they belong to (see Module variants section).

  A Key section is added at the end of the output in case some elements are reported in parentheses or chevrons along module name or if some graphical rendition is made over some outputed elements. This Key section gives hints on the meaning of such elements.
  """

  res = module('list')

  mods = list()

  for m in re.finditer( list_mod_rec, res ):
    mods.append( ( m.group('id'), m.group('mod') ) )

  mods = sorted( mods, key = lambda g: g[0] )
  mods = [ m[1] for m in mods ]

  return mods

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
def module_load( mods ):
  """

  https://modules.readthedocs.io/en/latest/module.html#subcmd-load
  Load modulefile into the shell environment.

  Once loaded, the loaded module tag is associated to the loaded module. If module has been automatically loaded by another module, the auto-loaded tag is associated instead (see Module tags section).

  The parameter modulefile may also be a symbolic modulefile name or a modulefile alias. It may also leverage a specific syntax to finely select module version (see Advanced module version specifiers section below).


  """
  if not isinstance( mods, list ):
    mods = [ mods, ]

  args = mods

  res = module( 'load', *args )

  if len(res) > 0:
    raise ModuleCmdError( res )

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
def module_unload( mods ):
  """
  Remove modulefile from the shell environment.

  The parameter modulefile may also be a symbolic modulefile name or a modulefile alias. It may also leverage a specific syntax to finely select module version (see Advanced module version specifiers section below).

  """
  if not isinstance( mods, list ):
    mods = [ mods, ]

  args = mods

  res = module( 'unload', *args )

  if len(res) > 0:
    raise ModuleCmdError( res )

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
def module_switch(
  modulefile1 = None,
  modulefile2 = None ):
  """
  Switch loaded modulefile1 with modulefile2. If modulefile1 is not specified, then it is assumed to be the currently loaded module with the same root name as modulefile2.

  The parameter modulefile may also be a symbolic modulefile name or a modulefile alias. It may also leverage a specific syntax to finely select module version (see Advanced module version specifiers section below).

  """

  if modulefile2 is None:
    return

  if modulefile1 is None:
    args = [ modulefile2, ]
  else:
    args = [ modulefile1, modulefile2 ]

  res = module( 'switch', *args )


  if len(res) > 0:
    raise ModuleCmdError( res )

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
def module_purge():
  """
  https://modules.readthedocs.io/en/latest/module.html#subcmd-purge

  Unload all loaded modulefiles.

  """

  res = module( 'purge' )

  if len(res) > 0:
    raise ModuleCmdError( res )

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
def module_use( dirs, append = None ):
  """

  https://modules.readthedocs.io/en/latest/module.html#subcmd-use

  Prepend one or more directories to the MODULEPATH environment variable. The --append flag will append the directory to MODULEPATH.

  When directory is already defined in MODULEPATH, it is not added again or moved at the end or at the beginning of the environment variable.

  If module use is called during a modulefile evaluation, the reference counter environment variable __MODULES_SHARE_MODULEPATH is also set to increase the number of times directory has been added to MODULEPATH. Reference counter is not updated when module use is called from the command-line or within an initialization modulefile script.

  A directory that does not exist yet can be specified as argument and then be added to MODULEPATH.

  """

  if not isinstance( dirs, list ):
    dirs = [ dirs, ]

  if append:
    res = module( 'use', '--append', *dirs )

  else:
    res = module( 'use', *dirs )


  if len(res) > 0:
    raise ModuleCmdError( res )

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
def module_unuse( dirs ):
  """

  https://modules.readthedocs.io/en/latest/module.html#subcmd-use

  Prepend one or more directories to the MODULEPATH environment variable. The --append flag will append the directory to MODULEPATH.

  When directory is already defined in MODULEPATH, it is not added again or moved at the end or at the beginning of the environment variable.

  If module use is called during a modulefile evaluation, the reference counter environment variable __MODULES_SHARE_MODULEPATH is also set to increase the number of times directory has been added to MODULEPATH. Reference counter is not updated when module use is called from the command-line or within an initialization modulefile script.

  A directory that does not exist yet can be specified as argument and then be added to MODULEPATH.

  """

  if not isinstance( dirs, list ):
    dirs = [ dirs, ]

  res = module( 'use', *dirs )


  if len(res) > 0:
    raise ModuleCmdError( res )

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
init_modules()
