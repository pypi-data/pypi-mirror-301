import sys
# NOTE: this is needed to perform "redirects" of the import of module to
# the shared 'mods' directory for tools that specify a 'resources.python.module'
from partis.utils.module import AliasMetaFinder

from . import inputs
from . import outputs
from . import commands
from . import results

from ._load_tool import load_tool

tool = load_tool( )
