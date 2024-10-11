
from .tool_edit import ToolEditor
from .tool_results_edit import ToolResultsEditor
from .workflow_edit import WorkflowEditor

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
def get_view_editors():
  from partis.view.edit.plugin import (
    EditorPluginGroup,
    SchemaEditNodePlugin )

  class _ToolResultsEditor( ToolResultsEditor ):
    guess_strict = False

  plugins = list()

  plugins.append( EditorPluginGroup(
    editors = {
      "NWL Tool" : ToolEditor,
      "NWL Tool Results" : _ToolResultsEditor,
      "NWL Workflow" : WorkflowEditor } ) )


  return plugins
