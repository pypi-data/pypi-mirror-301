# -*- coding: UTF-8 -*-

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
from copy import copy
import os
import os.path as osp
import re
import tempfile
import logging

from partis.utils import (
  getLogger,
  head,
  isinstance_any,
  VirtualEnv,
  ModelHint,
  MutexFile,
  LogListHandler )

from PySide2 import QtCore, QtGui, QtWidgets

from partis.nwl import (
  Workflow )

from partis.view.base import (
  blocked,
  WidgetStack )

from partis.view.dialog import (
  ProgressDialog )

from partis.schema.serialize.yaml import (
  loads,
  dumps )

from partis.schema import (
  is_mapping,
  is_sequence,
  is_valued_type,
  is_schema_struct_valued,
  MapPrim,
  UnionPrim )

from partis.nwl.context import (
  EnabledInputContext,
  OutputsContext,
  CommandsContext )

from partis.view.edit import SchemaStructTreeFileEditor

from partis.view.edit.text.code import (
  ExternalName )

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
class WorkflowEditor( SchemaStructTreeFileEditor ):
  default_schema = Workflow

  #-----------------------------------------------------------------------------
  def __init__( self,
    manager,
    widget_stack,
    schema = None,
    filename = None,
    state = None,
    readonly = None ):

    super().__init__(
      manager = manager,
      widget_stack = widget_stack,
      schema = schema,
      filename = filename,
      state = state,
      readonly = readonly,
      hidden = ['nwl'] )

    # TODO: running from gui doesn't work yet
    # self.run_btn = QtWidgets.QPushButton("Run Workflow")
    # self.run_btn.clicked.connect(self.on_run_workflow)
    # self.layout.addWidget( self.run_btn )

  #-----------------------------------------------------------------------------
  def on_run_workflow( self ):

    self._manager._manager._async_queue.append( (self.run_workflow, ) )

  #-----------------------------------------------------------------------------
  async def run_workflow( self ):

    pbar = ProgressDialog(
      self._manager,
      with_log = True )

    nwl_log = getLogger(f"nwl")
    nwl_log.setLevel( 0 )
    nwl_log.addHandler( pbar.log_handler )

    venv_log = nwl_log.getChild("venv")
    venv_log.propagate = False
    venv_log_handler = LogListHandler()
    venv_log.addHandler( venv_log_handler )

    log = nwl_log.getChild("run")


    pbar.set_title( "Running Workflow" )
    pbar.set_status( "" )
    pbar.set_range( 0, 0 )
    pbar.show()

    self.setEnabled(False)

    try:

      with tempfile.TemporaryDirectory() as rundir:
        if self._filename != "":
          startdir = osp.dirname( self._filename  )
        else:
          startdir = os.getcwd()

        workdir = startdir

        venv_dir = osp.join( rundir, 'venv_nwlrun' )

        venv_mutex = MutexFile(
          prefix = osp.basename(venv_dir),
          dir = osp.dirname(venv_dir),
          # 10 min
          timeout = 600.0 )

        venv = VirtualEnv(
          path = venv_dir,
          # inherit_site_packages = venv_in,
          # reuse_existing = not args.venv_force,
          args = ['--without-pip'],
          logger = venv_log,
          mutex = venv_mutex )

        test_results = await self.state.run(
          startdir = startdir,
          workdir = workdir,
          rundir = rundir,
          workflow_file = '',
          venv = venv,
          log = nwl_log.getChild("workflow"),
          initlogs = list(),
          find_links = None,
          processes = 1,
          cpus_per_process = 1,
          threads_per_cpu = 1,
          gpus_per_process = 0,
          run_serial = False )

        pbar.set_range( 0, 1 )
        pbar.set_value( 1 )

    except BaseException as e:
      pbar.set_range( 0, 1 )
      pbar.set_value( 0 )

      log.error("Could not run test suite.", exc_info = True )

    log.removeHandler(pbar.log_handler)

    self.setEnabled(True)

  #-----------------------------------------------------------------------------
  async def overwrite( self ):

      target = AsyncTarget()


      message_box = QtWidgets.QMessageBox()
      message_box.setWindowTitle( f"Overwrite" )
      message_box.setWindowIcon( QtGui.QIcon(self._manager.resource_path("images/icons/app_icon.png")) )
      message_box.setStyleSheet( self._manager.stylesheet )
      message_box.setText(
        f"Overwrite existing output package file?")

      message_box.setStandardButtons(
        QtWidgets.QMessageBox.Yes
        | QtWidgets.QMessageBox.Cancel )


      message_box.setDefaultButton( QtWidgets.QMessageBox.Yes )


      message_box.finished.connect( target.on_result )
      message_box.open()

      result, error = await target.wait()

      return result == QtWidgets.QMessageBox.Yes
