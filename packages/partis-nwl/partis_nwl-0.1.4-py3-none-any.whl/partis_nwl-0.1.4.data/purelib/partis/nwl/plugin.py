#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
def get_base_schemas():
  from partis.schema.plugin import (
    SchemaPluginGroup )

  from . import (
    ToolResults,
    Tool,
    Workflow,
    NWLToolPkg)

  return [ SchemaPluginGroup(
    schemas = {
      'NWL Tool' : Tool,
      'NWL Workflow' : Workflow,
      'NWL Tool Results' : ToolResults,
      'NWL Package' : NWLToolPkg}) ]
