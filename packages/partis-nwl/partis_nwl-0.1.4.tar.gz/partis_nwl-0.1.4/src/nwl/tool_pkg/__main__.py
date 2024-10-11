"""
"""
import sys
import argparse
from argparse import RawTextHelpFormatter
import trio

from partis.utils import (
  init_logging,
  getLogger,
  ModelHint,
  Loc )

from .build import build

log = getLogger(__name__)

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++#

def argument_parser( ):

  """Parse for commandline arguments.
  """

  parser = argparse.ArgumentParser(
    description = __doc__,
    formatter_class = RawTextHelpFormatter )


  parser.add_argument( "pkg_file",
    type = str,
    help = "path to tool package definition file" )

  parser.add_argument( "-o", "--out",
    type = str,
    help = "path to place the resulting package file" )

  parser.add_argument( "-d", "--doc-out",
    type = str,
    help = "path to place the resulting doc file" )


  parser.add_argument( "--tmp",
    type = str,
    help = "temporary build directory" )

  parser.add_argument( "--no-cleanup",
    action = 'store_true',
    help = "do not cleanup temporary build directory" )

  parser.add_argument( "--no-doc",
    action = 'store_true',
    help = "do not generate documentation" )

  parser.add_argument( "-l", "--log",
    type = str,
    default = "",
    help = "Redirect output to the given log file" )

  parser.add_argument( "-v", "--verbosity",
    type = str,
    default = 'info',
    help = "Log verbosity {all, debug, info, warning, error, critical}" )

  parser.add_argument( "--color",
    action = 'store_true',
    help = "Enable color log output" )

  parser.add_argument( "--no-color",
    action = 'store_true',
    help = "Disable color log output" )

  parser.add_argument( "--ascii",
    action = 'store_true',
    help = "Disable non-ascii log output" )


  return parser

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
def feat_enabled(enabled, disabled):
  if not ( enabled or disabled ):
    return None

  if enabled:
    return True

  return False

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
async def _main():
  parser = argument_parser( )
  args = parser.parse_args( )

  init_logging(
    level = args.verbosity,
    filename = args.log,
    with_color = feat_enabled(args.color, args.no_color),
    with_unicode = not args.ascii )

  try:
    await build(
      pkg_file = args.pkg_file,
      outdir = args.out,
      docdir = args.doc_out,
      tmpdir = args.tmp,
      cleanup = not args.no_cleanup,
      build_docs = not args.no_doc )

    return 0

  except Exception as e:
    log.error(ModelHint(
      f"Failed to build package",
      loc = Loc(filename = args.pkg_file),
      hints = e ))

    return 1

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
def main():
  return trio.run( _main )

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
if __name__ == "__main__":
  sys.exit(main())
