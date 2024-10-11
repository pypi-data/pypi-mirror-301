# -*- coding: UTF-8 -*-

from partis.utils import (
  ModelHint,
  ModelError )

from partis.schema import (
  UnionPrim,
  schema_declared )

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# create declareds for all the 'input' schemas

tool_declared = schema_declared( tag = 'tool' )

workflow_declared = schema_declared( tag = 'workflow' )

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++#
UnionToolWorkflow = UnionPrim(
  cases = [
    tool_declared,
    workflow_declared ] )

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
class ToolError( ModelError ):
  pass

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
class WorkflowError( ModelError ):
  pass

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++#
class SerialGroup(list):
  pass

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++#
class ParallelGroup(list):
  pass
