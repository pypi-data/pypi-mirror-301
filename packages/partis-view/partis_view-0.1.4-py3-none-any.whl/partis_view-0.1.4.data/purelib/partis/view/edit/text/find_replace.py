# -*- coding: UTF-8 -*-

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
import logging
log = logging.getLogger( __name__ )

import re

from PySide2 import QtCore, QtGui, QtWidgets

from partis.view.base import (
  blocked,
  Heading1,
  Heading2,
  Heading3,
  HLine,
  ToolButton,
  ToolTextButton,
  EditLabel,
  rgba )


#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
class ReValidator ( QtGui.QValidator ):
  #----------------------------------------------------------------------------#
  def __init__ ( self ):
    super().__init__()
    self.msg = ''


  #----------------------------------------------------------------------------#
  def validate( self, input, pos ):

    try:
      re.compile(input)
      self.msg = ''

      return QtGui.QValidator.Acceptable

    except re.error as e:
      self.msg = f"Invalid regular expression: {e.msg}"

    return QtGui.QValidator.Intermediate

  #----------------------------------------------------------------------------#
  def fixup( self, input ):
    return input

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
class FindReplace( QtWidgets.QWidget ):

  pattern_changed = QtCore.Signal(object)
  find_prev = QtCore.Signal()
  find_next = QtCore.Signal()
  closed = QtCore.Signal()

  #-----------------------------------------------------------------------------
  def __init__( self,
    manager ):

    super().__init__()
    self._manager = manager
    self._pattern = None

    self.setAttribute( QtCore.Qt.WA_StyleSheet, True )
    self.setAttribute( QtCore.Qt.WA_StyledBackground, True )

    self.setLayout(QtWidgets.QGridLayout())
    self.layout().setContentsMargins(0,0,0,0)
    self.layout().setSpacing(0)
    self.tool_layout = QtWidgets.QHBoxLayout()
    self.layout().addLayout(self.tool_layout, 0, 0, 1, 3)

    self._case_btn = ToolTextButton( "Aa", "Case sensitive" )
    self._case_btn.setCheckable(True)
    self._case_btn.toggled.connect( self.on_case_toggled )
    self.tool_layout.addWidget( self._case_btn )

    self._re_btn = ToolTextButton( ".*", "Regular Expression" )
    self._re_btn.setCheckable(True)
    self._re_btn.toggled.connect( self.on_re_toggled )
    self.tool_layout.addWidget( self._re_btn )

    self._msg = QtWidgets.QLabel()
    self.tool_layout.addWidget( self._msg )

    self.tool_layout.addStretch()

    self._closed_btn = ToolButton(
      self._manager.svgcolor('images/icons/remove.svg'),
      "Close" )
    self._closed_btn.clicked.connect( self.closed.emit )
    self.tool_layout.addWidget( self._closed_btn )

    self.pattern_edit = QtWidgets.QLineEdit()
    self.pattern_edit.setPlaceholderText("Find pattern")
    self.pattern_edit.setProperty("asdasd", True)

    self.pattern_edit.textChanged.connect( self.on_pattern_changed )
    self.layout().addWidget( self.pattern_edit, 1, 0 )

    self._prev_btn = ToolButton(
      self._manager.svgcolor('images/icons/left_arrow.svg'),
      "Previous match" )
    self._prev_btn.clicked.connect( self.find_prev.emit )
    self.layout().addWidget( self._prev_btn, 1, 1 )

    self._next_btn = ToolButton(
      self._manager.svgcolor('images/icons/right_arrow.svg'),
      "Next match" )
    self._next_btn.clicked.connect( self.find_next.emit )
    self.layout().addWidget( self._next_btn, 1, 2 )

  #-----------------------------------------------------------------------------
  @property
  def pattern(self):
    return self._pattern

  #-----------------------------------------------------------------------------
  @pattern.setter
  def pattern(self, pattern):
    self.pattern_edit.setText(pattern)

  #-----------------------------------------------------------------------------
  def on_pattern_changed(self, pattern):
    self.update_pattern()

  #-----------------------------------------------------------------------------
  def on_re_toggled(self, enabled):

    if enabled:
      self.pattern_edit.setValidator( ReValidator() )
    else:
      self.pattern_edit.setValidator( None )
      self._msg.setText('')

    self.update_pattern()

  #-----------------------------------------------------------------------------
  def on_case_toggled(self, enabled):
    self.update_pattern()

  #-----------------------------------------------------------------------------
  def update_pattern(self):

    v = self.pattern_edit.validator()

    if v is not None:
      # NOTE: needed to update style when acceptableInput property changes
      self.pattern_edit.style().polish(self.pattern_edit)
      self._msg.setText("  " + v.msg)

    if not self.pattern_edit.hasAcceptableInput():
      pattern = None

    pattern = self.pattern_edit.text()

    if pattern in ['', None]:
      pattern = None

    else:
      if not self._re_btn.isChecked():
        # escape characters in string that are regular expression syntax
        pattern = re.escape(pattern)

      flags = re.MULTILINE

      if not self._case_btn.isChecked():
        flags |= re.IGNORECASE

      try:
        pattern = re.compile( pattern, flags )
      except re.error:
        pattern = None

    self._pattern = pattern
    self.pattern_changed.emit( self._pattern )

  #-----------------------------------------------------------------------------
  def keyPressEvent( self, event ):

    if event.key() in [ QtCore.Qt.Key_Return, QtCore.Qt.Key_Enter ]:

      if event.modifiers() & QtCore.Qt.ShiftModifier:
        self.find_prev.emit()
      else:
        self.find_next.emit()
