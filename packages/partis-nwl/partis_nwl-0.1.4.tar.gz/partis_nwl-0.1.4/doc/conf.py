# -*- coding: utf-8 -*-

from partis.utils.sphinx import basic_conf

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# configuration
#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

globals().update( basic_conf(
  package = 'partis-nwl',
  copyright_year = '2022' ) )


# pylint: disable-next=E0602
intersphinx_mapping['partis.pyproj'] = (
  "https://nanohmics.bitbucket.io/doc/partis/pyproj",
  None )
# pylint: disable-next=E0602
intersphinx_mapping['partis.utils'] = (
  "https://nanohmics.bitbucket.io/doc/partis/utils",
  None )
# pylint: disable-next=E0602
intersphinx_mapping['partis.schema'] = (
  "https://nanohmics.bitbucket.io/doc/partis/schema",
  None )

bibtex_bibfiles = [
  'refs/workflow.bib' ]
