# -*- coding: UTF-8 -*-

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
from PySide2 import QtCore, QtGui, QtWidgets

from copy import copy
import logging
log = logging.getLogger(__name__)

from partis.utils import (
  split_lines,
  record_to_hint,
  ModelHint,
  HINT_LEVELS )

from partis.schema.hint import (
  Hint,
  HintLoc,
  HintList )

from partis.view.base import (
  WidgetStack,
  AsyncTarget )

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
class LogWidgetHandler( logging.Handler ):
  """Collects log records in local list

  Parameters
  ----------
  send_channel : SendChannel
  level : int
    The level enabled for the handler
  **kwargs :
    Keyword arguments passed to the ModelHint when casting
  """
  #-----------------------------------------------------------------------------
  def __init__(self, widget, **kwargs ):
    super().__init__( logging.NOTSET )

    self._widget = widget
    self._kwargs = kwargs

  #-----------------------------------------------------------------------------
  def emit(self, record):
    hint = record_to_hint(record)

    self._widget.log_hint( hint )


#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
class LogWidget ( QtWidgets.QWidget ):

  #-----------------------------------------------------------------------------
  def __init__( self,
    manager,
    widget_stack ):
    super().__init__()

    self._manager = manager

    self.vlayout = QtWidgets.QVBoxLayout(self)
    self.setLayout(self.vlayout)

    from ..schema import TreeEditNodeMap
    from ..schema.hint_w import HintListEdit
    tree_node_map = TreeEditNodeMap()

    self.log_tree = HintListEdit(
      manager = self._manager,
      schema = HintList,
      widget_stack = widget_stack,
      tree_node_map = tree_node_map,
      readonly = True )

    self.vlayout.addWidget(
      self.log_tree )

    # self.log_area = QtWidgets.QScrollArea()
    # self.log_area.setWidgetResizable( True )
    # policy = QtWidgets.QSizePolicy.Expanding
    # self.log_area.setSizePolicy( QtWidgets.QSizePolicy(policy, policy) )
    #
    # self.log_frame = QtWidgets.QFrame(self.log_area)
    # self.log_layout = QtWidgets.QVBoxLayout()
    # self.log_frame.setLayout(self.log_layout)
    # self.log_layout.setSpacing(0)
    # self.log_layout.setContentsMargins(0,0,0,0)
    # self.log_layout.addWidget( self.log_tree )
    #
    # self.log_area.setWidget( self.log_frame )
    #
    # self.vlayout.addWidget(
    #   self.log_area )



    self.setAttribute( QtCore.Qt.WA_StyleSheet, True )
    self.setAttribute( QtCore.Qt.WA_StyledBackground, True )

    self._hints = list()

  #-----------------------------------------------------------------------------
  def log_hint( self, hint ):

    if not isinstance( hint, ModelHint ):
      hint = ModelHint.cast( hint )

    self._hints.append( hint )

    # self.log_text.append( hint.fmt(
    #   level = self.log_level ) )
    state = copy(self.log_tree.state)
    state.append( hint.to_dict() )
    self.log_tree.state = state

  #-----------------------------------------------------------------------------
  def clear_hints( self ):
    self.log_tree.state = list()

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
class LogDialog ( QtWidgets.QDialog ):

  #-----------------------------------------------------------------------------
  def __init__( self, manager ):
    super().__init__()

    self._manager = manager

    self.setWindowIcon( QtGui.QIcon(self._manager.resource_path("images/icons/app_icon.png")) )
    self.setWindowTitle("")

    self.setAttribute( QtCore.Qt.WA_StyleSheet, True )
    self.setAttribute( QtCore.Qt.WA_StyledBackground, True )

    self.setStyleSheet( self._manager.stylesheet )

    self.vlayout = QtWidgets.QVBoxLayout(self)
    self.setLayout(self.vlayout)

    self._widget_stack = WidgetStack(
      manager = self._manager )

    self.log = LogWidget(
      manager = self._manager,
      widget_stack = self._widget_stack )

    self._widget_stack.push_widget( self.log )

    self.vlayout.addWidget( self._widget_stack )

    screen = QtGui.QGuiApplication.primaryScreen()
    screenGeometry = screen.geometry()
    height = screenGeometry.height()
    width = screenGeometry.width()

    self.resize( int( width / 2.0 ), int( height / 2.0 ) )


  #-----------------------------------------------------------------------------
  def log_hint( self, hint ):
    self.log.log_hint( hint )

  #-----------------------------------------------------------------------------
  def on_open_log( self ):

    self.show()
    # workaround since raise is reserved word in Python
    getattr(self, 'raise')()
    self.activateWindow()

  #-----------------------------------------------------------------------------
  def close( self ):
    self.log.close()

  #-----------------------------------------------------------------------------
  def closeEvent( self, event ):
    self.close()
    super().closeEvent( event )
