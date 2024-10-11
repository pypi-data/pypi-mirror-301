# -*- coding: UTF-8 -*-

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
import sys
import os
from copy import copy

from PySide2 import QtCore, QtGui, QtWidgets

import logging
log = logging.getLogger(__name__)

from partis.view.base import (
  Heading1,
  Heading2,
  Heading3,
  HLine,
  ToolButton,
  ToolTextButton,
  LeftButton,
  MiddleButton,
  RightButton,
  blocked,
  ScrollComboBox )

from partis.view.edit.var_tree import VariableTreeItem

from .type_combo_w import TypeComboWidget

heading_levels = [
  Heading1,
  Heading2,
  Heading3 ]

from partis.schema import (
  is_required,
  is_optional,
  is_schema_struct,
  is_valued_type,
  Loc )

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
class CloseCommit( QtWidgets.QWidget ):
  close = QtCore.Signal()
  commit = QtCore.Signal()

  #-----------------------------------------------------------------------------
  def __init__( self,
    manager,
    parent = None ):

    super().__init__( parent )
    self.setAttribute( QtCore.Qt.WA_StyleSheet, True )
    self.setAttribute( QtCore.Qt.WA_StyledBackground, True )
    self.setSizePolicy(
      QtWidgets.QSizePolicy.Fixed,
      QtWidgets.QSizePolicy.MinimumExpanding )

    self._manager = manager

    self.setLayout( QtWidgets.QHBoxLayout( self ) )
    self.layout().setContentsMargins(0,0,0,0)
    self.layout().setSpacing(0)

    self.commit_btn = RightButton(
      text = "Apply",
      parent = self)

    self.commit_btn.clicked.connect(self.commit)

    self.commit_btn.setSizePolicy(
      QtWidgets.QSizePolicy.Fixed,
      QtWidgets.QSizePolicy.MinimumExpanding )

    self.close_btn = LeftButton(
      icon = QtGui.QIcon(self._manager.svgcolor('images/icons/remove.svg')),
      tooltip = "Apply and Close",
      parent = self)

    self.close_btn.enter.connect(self.on_enter_close_btn)
    self.close_btn.pressed.connect(self.on_pressed_close_btn)
    self.close_btn.released.connect(self.on_released_close_btn)
    self.close_btn.leave.connect(self.on_leave_close_btn)
    self.close_btn.clicked.connect(self.close)

    self.close_btn.setSizePolicy(
      QtWidgets.QSizePolicy.Fixed,
      QtWidgets.QSizePolicy.MinimumExpanding )

    self.layout().addWidget(self.close_btn)
    self.layout().addWidget(self.commit_btn)

    # self.layout().setAlignment(self.close_btn, QtCore.Qt.AlignLeft)
    # self.layout().setCurrentIndex(self.layout().indexOf(self.close_btn))

  #-----------------------------------------------------------------------------
  def on_enter_close_btn(self):
    self.commit_btn.setProperty("highlighted", True)
    self.commit_btn.style().polish(self.commit_btn)

  #-----------------------------------------------------------------------------
  def on_leave_close_btn(self):
    self.commit_btn.setProperty("highlighted", False)
    self.commit_btn.style().polish(self.commit_btn)

  #-----------------------------------------------------------------------------
  def on_pressed_close_btn(self):
    self.commit_btn.setProperty("emphasized", True)
    self.commit_btn.style().polish(self.commit_btn)

  #-----------------------------------------------------------------------------
  def on_released_close_btn(self):
    self.commit_btn.setProperty("emphasized", False)
    self.commit_btn.style().polish(self.commit_btn)

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
class Edit( QtWidgets.QWidget ):
  state_changed = QtCore.Signal( object )
  clicked = QtCore.Signal()
  closed = QtCore.Signal()

  #-----------------------------------------------------------------------------
  def __init__( self,
    manager,
    schema,
    widget_stack = None,
    tree_node_map = None,
    get_eval_names = None,
    parent = None,
    state = None,
    readonly = None,
    loc = None,
    popout = None,
    manual_commit = None ):

    super().__init__( parent )
    self.setAttribute( QtCore.Qt.WA_StyleSheet, True )
    self.setAttribute( QtCore.Qt.WA_StyledBackground, True )

    if loc is None:
      loc = Loc(
        filename = __name__ )

    if readonly is None:
      readonly = False

    self._widget_stack = widget_stack
    self._tree_node_map = tree_node_map
    self._get_eval_names = get_eval_names
    self._schema = schema
    self._loc = loc

    self._popout = bool(popout)
    self._manual_commit = bool(manual_commit)

    self._reset_state = None
    self._state = None
    self._push_state = None
    self._view_built = False

    self._manager = manager
    self._readonly = bool(readonly)

    self._layout = QtWidgets.QVBoxLayout( self )
    self.setLayout(self._layout)


    self._layout.setSpacing(0)

    if self._popout or ( not self.readonly and self._manual_commit ):
      self.toolbar = QtWidgets.QToolBar(self)
      self.layout().addWidget(self.toolbar)

    if not self._popout:
      self._layout.setContentsMargins(0,0,0,0)

    else:
      ex = self._manager._px_per_ex
      margin_ex = int(round(max(1, 0.5*ex)))
      self._layout.setContentsMargins(margin_ex, 0, margin_ex, margin_ex)

      shadow = QtWidgets.QGraphicsDropShadowEffect(self)
      shadow.setColor(QtGui.QColor(0, 0, 0, 255 * 0.75))
      shadow.setOffset(0)
      shadow.setBlurRadius(int(round(max(1, 2*ex))))
      self.setGraphicsEffect(shadow)

      self.setProperty("popoutStyle", True)

      close_commit = CloseCommit(self._manager)
      self.toolbar.addWidget(close_commit)
      close_commit.close.connect(self.on_close)
      close_commit.commit.connect(self.commit)

      # self.toolbar.addAction(QtWidgets.QAction(
      #   QtGui.QIcon(self._manager.svgcolor('images/icons/remove.svg')),
      #   "Close",
      #   self,
      #   statusTip = "Commit and close editor",
      #   triggered = self.on_close ))

    if not self.readonly and self._manual_commit:
      if not self._popout:
        self.toolbar.addAction(QtWidgets.QAction(
          "Apply",
          self,
          statusTip = "Reset to initital editor value(s)",
          triggered = self.commit ))

      self.toolbar.addAction(QtWidgets.QAction(
        "Reset",
        self,
        statusTip = "Reset to initital editor value(s)",
        triggered = self.reset ))
    self.state = state

  #-----------------------------------------------------------------------------
  @property
  def readonly( self ):
    return self._readonly

  #-----------------------------------------------------------------------------
  @property
  def state( self ):
    return self._state

  #-----------------------------------------------------------------------------
  @state.setter
  def state( self, state ):

    if state is None:
      state = self._schema.decode(
        val = self._schema.init_val )

    if state is self._state:
      return

    self._state = state

    if self._state is self._push_state:
      # if the new state *is* the outbound state, then the state_changed signal
      # is emitted to propagate the changes "outward", toward the manager.
      self.state_changed.emit( self._state )

    else:
      # otherwise, the new state is *not* the outbound state, meaning that it is
      # assumed to be the inbound state.

      self._reset_state = copy(self._state)

      if not self._view_built:
        # First time, build the initial gui elements
        self.build()
        self._view_built = True

      # The changes must instead be propagated "inward", toward the view/user,
      # by synchronizing the gui elements with the new state.
      self.merge()
      self._push_state = self._state

  #-----------------------------------------------------------------------------
  @property
  def push_state( self ):
    return self._push_state

  #-----------------------------------------------------------------------------
  @push_state.setter
  def push_state( self, state ):
    self._push_state = state
    self.state = state

  #-----------------------------------------------------------------------------
  def build( self ):
    pass

  #-----------------------------------------------------------------------------
  def merge( self ):
    pass

  #-----------------------------------------------------------------------------
  def commit(self):
    pass

  #-----------------------------------------------------------------------------
  def close( self ):
    pass

  #-----------------------------------------------------------------------------
  def on_close( self ):
    self.closed.emit()

  #-----------------------------------------------------------------------------
  def reset( self ):
    self.state = self._reset_state

  #-----------------------------------------------------------------------------
  def set_enabled( self, enabled ):
    self.setEnabled( enabled )

  #-----------------------------------------------------------------------------
  def set_visible( self, visible ):
    self.setVisible( visible )

  #-----------------------------------------------------------------------------
  def mousePressEvent( self, event ):
    self.clicked.emit()

  #-----------------------------------------------------------------------------
  @property
  def schema( self ):
    return self._schema

  #-----------------------------------------------------------------------------
  @property
  def loc( self ):
    return self._loc

  #-----------------------------------------------------------------------------
  def get_eval_names( self, context = None ):
    if self._get_eval_names:
      return self._get_eval_names( context = context )

    return dict()

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
class RestrictedEdit( Edit ):

  #-----------------------------------------------------------------------------
  def build( self ):
    super().build()

    self._combo = ScrollComboBox()
    self._combo.readonly = self.readonly

    for opt in self._schema.restricted:
      self._combo.addItem( str(opt),
        userData = opt )

    self._combo.currentIndexChanged.connect( self.on_changed_combo )

    self._layout.addWidget( self._combo )

  #-----------------------------------------------------------------------------
  def merge( self ):

    with blocked( self._combo ):
      index = self._combo.findData( self.state )
      self._combo.setCurrentIndex( index )

    super().merge()

  #-----------------------------------------------------------------------------
  def set_enabled( self, enabled ):
    super().set_enabled( enabled )

    self._combo.setEnabled( enabled )

  #-----------------------------------------------------------------------------
  def on_changed_combo( self, index ):

    self.push_state = self._schema.decode(
      val = self._combo.currentData(),
      loc = self._loc )
