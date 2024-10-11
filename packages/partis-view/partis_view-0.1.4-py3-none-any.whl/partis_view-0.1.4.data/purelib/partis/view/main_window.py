# -*- coding: UTF-8 -*-

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
from PySide2 import QtCore, QtGui, QtWidgets

from .edit import (
  Project,
  editor_map )

import tempfile
from datetime import datetime
import sys
import os
import os.path as osp
import re
from timeit import default_timer as timer
import time
import math

import logging
from partis.utils import (
  f,
  ModelHint,
  getLogger )

log = getLogger( __name__ )

from partis.view.base import (
  AsyncTarget )

from partis.view.dialog import (
  LogDialog )

from .settings import (
  Settings,
  SettingsEditor )

from .theme import (
  svgcolor,
  qss_process,
  pygments_style )

# this is only needed for Qt 5 on Mac OS
os.environ['QT_MAC_WANTS_LAYER'] = '1'

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
class MainWindow ( QtWidgets.QMainWindow ):
  """Main application window
  """

  #-----------------------------------------------------------------------------
  def __init__( self,
    manager,
    theme,
    logger = None ):
    super( ).__init__()

    if logger is None:
      logger = log

    self._logger = logger
    self._manager = manager
    self._closed = False
    self._is_full_screen = False

    self._prev_state = None

    self.init = True

    self._resource_dir = os.path.join(
      osp.dirname(os.path.abspath(__file__)), "theme" )

    self._resource_tmp_o = tempfile.TemporaryDirectory()
    self._resource_tmp = self._resource_tmp_o.name

    self.stylesheet = ""
    # self.font_db = QtGui.QFontDatabase()

    # self._px_per_ex = self.fontMetrics().xHeight()
    screens = self._manager._app.screens()
    dpi = max([ s.physicalDotsPerInch() for s in screens ])
    npt = 10

    self._px_per_pt = float( dpi / 72.0 )
    self._px_per_em = self._px_per_pt * npt
    self._px_per_ex = 0.5 * self._px_per_em

    self._settings_edit = None
    self.settings = Settings()

    if theme is not None:
      for preset in self.settings.theme.color._schema.preset_vals:
        if preset.label.lower() == theme.lower():
          self.settings.theme.color = preset.val

    fonts_path = self.resource_path( 'fonts', check_exists = False )

    if osp.exists( fonts_path ):
      fonts = os.listdir(fonts_path)
      rec = re.compile( "^.*\.ttf$" )

      for font in fonts:
        if rec.match( font ):
          path = os.path.join( fonts_path, font )

          self._logger.debug( f"Loading font: {path}" )

          try:
            assert osp.exists(path)
            QtGui.QFontDatabase.addApplicationFont( path )
          except Exception as e:
            self._logger.error( ModelHint.cast(e) )

    self.stylesheet_raw = self.load_qss()

    self.update_styles()

    self.setWindowIcon( QtGui.QIcon(self.resource_path("images/icons/app_icon.png")) )
    self.setWindowTitle("partis-view")

    self.project = Project(
      manager = self,
      editor_map = editor_map )

    self.project.editor_changed.connect(self.on_editor_changed)

    self.setCentralWidget( self.project )

    self.readSettings()
    self.createActions()
    self.createMenus()
    self.createToolBars()
    self.createStatusBar()

    self.setUnifiedTitleAndToolBarOnMac(True)

    # initially set as if there is not editor
    self.on_editor_changed(None)

  #----------------------------------------------------------------------------#
  def dispatch( self, action ):
    self._manager.dispatch( action )

  #-----------------------------------------------------------------------------
  @property
  def state(self):
    return self._manager.state

  #-----------------------------------------------------------------------------
  async def async_close( self ):
    # self.writeSettings()
    # self._manager.dispatch( njm.actions.system.Shutdown() )
    await self.project.close()

    self.writeSettings()

    self._closed = True

    self.close()

  #-----------------------------------------------------------------------------
  def closeEvent( self, event ):
    if self._closed:
      event.accept()
      self._manager.exit()
      return

    self._manager._async_queue.append( (self.async_close, ) )

  #-----------------------------------------------------------------------------
  def newState (self):
    self.project.on_open_editor()

  #-----------------------------------------------------------------------------
  def loadState (self):
    dialog = QtWidgets.QFileDialog(self)
    dialog.setDirectory( self.project.workdir.root_dir )
    dialog.setFileMode(QtWidgets.QFileDialog.AnyFile )
    dialog.setAcceptMode(QtWidgets.QFileDialog.AcceptOpen)

    dialog.fileSelected.connect( self.loadStateFinish )
    dialog.open()

  #-----------------------------------------------------------------------------
  def open_dir (self):
    dialog = QtWidgets.QFileDialog(self)
    dialog.setDirectory( self.project.workdir.root_dir )
    dialog.setFileMode(QtWidgets.QFileDialog.Directory )
    dialog.setAcceptMode(QtWidgets.QFileDialog.AcceptOpen)

    dialog.fileSelected.connect( self.loadStateFinish )
    dialog.open()

  #-----------------------------------------------------------------------------
  def loadStateFinish (self, file):
    if file is not None and file != "":
      if os.path.isfile( file ):
        self.project.on_open_editor( file )

      elif os.path.isdir( file ):
        self.project.set_root_dir( file )

  #-----------------------------------------------------------------------------
  def saveState (self):

    self.project.on_save_editor()

  #-----------------------------------------------------------------------------
  def saveStateAs (self):
    self.project.on_save_editor_as()

  #-----------------------------------------------------------------------------
  def on_editor_changed(self, editor):
    self.saveAct.setEnabled( not (
      editor is None
      or editor.readonly
      or editor.filename in [None, ''] ) )

    self.saveAsAct.setEnabled(editor is not None)

  #-----------------------------------------------------------------------------
  def about(self):

    try:
      import pkg_resources
      version = pkg_resources.get_distribution("partis-view").version
    except:
      version = "??"

    QtWidgets.QMessageBox.about(self, "About partis-view",
      "partis-view\n"
      f"version: {version}\n\n"
      "")

  #-----------------------------------------------------------------------------
  def documentWasModified(self):
    #self.setWindowModified(self.textEdit.document().isModified())
    pass


  #-----------------------------------------------------------------------------
  def createActions(self):

    self.newAct = QtWidgets.QAction(
      QtGui.QIcon(self.svgcolor('images/icons/new.svg')),
      "&New File",
      self,
      shortcut=QtGui.QKeySequence.New,
      statusTip="Create a new file",
      triggered=self.newState )

    self.openAct = QtWidgets.QAction(
      QtGui.QIcon(self.svgcolor('images/icons/load.svg')),
      "&Open File",
      self,
      shortcut=QtGui.QKeySequence.Open,
      statusTip="Open a file",
      triggered=self.loadState )

    self.openDirAct = QtWidgets.QAction(
      QtGui.QIcon(self.svgcolor('images/icons/load.svg')),
      "&Open Folder",
      self,
      shortcut=QtGui.QKeySequence("Ctrl+Shift+O"),
      statusTip="Open a directory",
      triggered=self.open_dir )

    self.saveAct = QtWidgets.QAction(
      QtGui.QIcon(self.svgcolor('images/icons/save.svg')),
      "&Save", self,
      shortcut=QtGui.QKeySequence.Save,
      statusTip="Save state to disk",
      triggered=self.saveState )
    #
    self.saveAsAct = QtWidgets.QAction(
      QtGui.QIcon(self.svgcolor('images/icons/saveAs.svg')),
      "Save &As...",
      self,
      shortcut=QtGui.QKeySequence("Ctrl+Shift+S"),
      statusTip="Save the document under a new name",
      triggered=self.saveStateAs)


    self.exitAct = QtWidgets.QAction("E&xit",
      self,
      shortcut="Ctrl+Q",
      statusTip="Exit the application",
      triggered=self.close)


    self.aboutAct = QtWidgets.QAction("&About",
      self,
      statusTip="Show the application's About box",
      triggered=self.about)

    self.window_act = QtWidgets.QAction(
      "Full-Screen",
      self, shortcut="F11",
      statusTip="Window mode",
      triggered=self.on_window_mode )

    self.settings_act = QtWidgets.QAction(
      "Settings",
      self,
      shortcut= QtGui.QKeySequence(QtCore.Qt.CTRL + QtCore.Qt.Key_Comma),
      statusTip="Settings",
      triggered=self.on_settings )

    self.settings_act.setMenuRole(QtWidgets.QAction.PreferencesRole)

  #-----------------------------------------------------------------------------
  def createMenus(self):
      self.fileMenu = self.menuBar().addMenu("&File")
      self.fileMenu.addAction(self.newAct)
      self.fileMenu.addAction(self.openAct)
      self.fileMenu.addAction(self.openDirAct)
      self.fileMenu.addAction(self.saveAct)
      self.fileMenu.addAction(self.saveAsAct)
      self.fileMenu.addSeparator()
      self.fileMenu.addAction(self.exitAct)

      #
      self.edit_menu = self.menuBar().addMenu("Edit")
      self.edit_menu.addAction(self.settings_act)

      self.view_menu = self.menuBar().addMenu("View")
      self.view_menu.addAction(self.window_act)

      # self.menuBar().addSeparator()

      self.helpMenu = self.menuBar().addMenu("&Help")
      self.helpMenu.addAction(self.aboutAct)

  #-----------------------------------------------------------------------------
  def createToolBars(self):
      # self.fileToolBar = self.addToolBar("Operations")
      # self.fileToolBar.addAction(self.newAct)
      # self.fileToolBar.addAction(self.openAct)
    pass

  #-----------------------------------------------------------------------------
  def createStatusBar(self):
      self.statusBar().showMessage("Ready")

 #-----------------------------------------------------------------------------
  def readSettings(self):
    settings = QtCore.QSettings("partis-view", "partis-view")
    pos = settings.value("pos", QtCore.QPoint(200, 200))
    size = settings.value("size", QtCore.QSize(400, 400))
    self.resize(size)
    self.move(pos)

  #-----------------------------------------------------------------------------
  def writeSettings(self):
      settings = QtCore.QSettings("partis-view", "partis-view")
      settings.setValue("pos", self.pos())
      settings.setValue("size", self.size())


  #-----------------------------------------------------------------------------
  def on_window_mode( self ):

    if self._is_full_screen:
      self._is_full_screen = False
      self.showNormal()
      # self.setWindowFlags( self.window_flags )
      # self.setWindowState( self.window_state )
    else:
      self._is_full_screen = True
      self.window_flags = self.windowFlags()
      self.window_state = self.windowState()
      # self.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint | QtCore.Qt.FramelessWindowHint)
      # self.setWindowState( self.window_state ^ QtCore.Qt.WindowFullScreen )
      self.showFullScreen()

  #-----------------------------------------------------------------------------
  def load_qss_recurse( self, path ):
    path = os.path.normpath( path )

    self._logger.debug( f"Importing stylesheet: {path}" )

    stylesheet_str = None

    with open(path) as fp:
      stylesheet_str = fp.read()

    style_imports = re.finditer(
      r"@import [\"\'](?P<path>[^\"\']+)[\"\']\;",
      stylesheet_str )

    for match in style_imports:
      path = match.group("path")

      imported_str = self.load_qss_recurse( self.resource_path(f'styles/{path}') )

      imported_str = (
        f"\n/* BEGIN: {match.group(0)} */\n\n"
        + imported_str
        + f"\n/* END: {match.group(0)} */\n\n"  )

      # include loaded qss file where the @import statement occurs
      stylesheet_str = stylesheet_str.replace( match.group(0), imported_str, 1 )


    return stylesheet_str

  #-----------------------------------------------------------------------------
  def load_qss( self ):
    stylesheet_str = self.load_qss_recurse( self.resource_path('styles/main.qss') )

    return stylesheet_str

  #-----------------------------------------------------------------------------
  def update_styles( self ):

    stylesheet_str = qss_process(
      self.stylesheet_raw,
      variables = self.settings.theme,
      px_per_pt = self._px_per_pt,
      idir = self._resource_dir,
      odir = self._resource_tmp )

    # print(stylesheet_str)
    # self._logger.debug(stylesheet_str)

    self.stylesheet = stylesheet_str

    # NOTE: for some reason directly setting a non-empty stylesheet over an
    # existing non-empty stylesheet causes the application to freeze.
    # This is a workaround to clear the stylesheet first (appears to work)
    self._manager._app.setStyleSheet("")

    self._manager._app.setStyleSheet( self.stylesheet )

  #-----------------------------------------------------------------------------
  def resource_path( self,
    path,
    check_exists = True,
    as_url = False ):
    """Converts generic paths to local platform-dependent file path

    Parameters
    ----------
    path : str
      relative path in the theme-specific resource directory
      in forward-slash format
    check_exists : bool
      Raise exception if the file does not exist
    as_url : bool
      Format path as a resource URL
    """

    parts = [ self._resource_dir, ] + path.split("/")
    full_path = os.path.join( *parts )

    if check_exists and not os.path.exists( full_path ):
      raise ValueError(f"Path `{str(full_path)}` not found in the resource directory.")

    if as_url:
      full_path = QtCore.QUrl.fromLocalFile( full_path ).url()

    return full_path

  #-----------------------------------------------------------------------------
  def svgcolor(self, path, fore = None, edge = None, back = None ):
    color = self.settings.theme.color.static

    fore = fore or color.fore_alt
    edge = edge or color.edge_alt
    back = back or color.back_alt

    path = svgcolor(path, fore, edge, back, self._resource_dir, self._resource_tmp)

    return path

  #-----------------------------------------------------------------------------
  def pygments_style(self):
    return pygments_style(self.settings.theme.color)

  #-----------------------------------------------------------------------------
  async def test_project( self ):
    self._manager.test( self.project )

  #-----------------------------------------------------------------------------
  def show_exception( self, title, exc ):

    dialog = LogDialog(
      manager = self )

    dialog.setWindowTitle( title )

    dialog.log_hint( ModelHint(
      msg = title,
      level = 'error',
      hints = exc ) )

    dialog.exec()

    dialog = None

  #-----------------------------------------------------------------------------
  def on_settings( self ):
    if self._settings_edit is not None:
      return

    self._settings_edit = self.project.add_editor(
      editor_class = SettingsEditor,
      state = self.settings,
      name = "Settings",
      tab_index = 0 )

    self._settings_edit.state_changed.connect(self.on_settings_changed)
    self._settings_edit.closed.connect(self.on_settings_closed)

  #-----------------------------------------------------------------------------
  def on_settings_changed( self, editor, state ):
    self.settings = state
    self.update_styles()

  #-----------------------------------------------------------------------------
  def on_settings_closed( self, editor ):
    self._settings_edit = None
