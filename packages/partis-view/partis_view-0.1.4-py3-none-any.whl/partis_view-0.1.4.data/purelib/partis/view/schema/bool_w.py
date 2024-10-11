# -*- coding: UTF-8 -*-

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
import sys
import os

from PySide2 import QtCore, QtGui, QtWidgets

import logging
log = logging.getLogger(__name__)

from partis.view.base import (
  Heading1,
  Heading2,
  Heading3,
  HLine,
  ToolButton,
  blocked )

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

from .tree_edit_w import TreeEditNode

from .edit_w import (
  Edit )

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
class BoolEdit( Edit ):

  #-----------------------------------------------------------------------------
  def build( self ):
    super().build()

    self._checkbox = QtWidgets.QCheckBox( self )

    if self.readonly:
      self._checkbox.setAttribute(QtCore.Qt.WA_TransparentForMouseEvents, True )
      self._checkbox.setFocusPolicy( QtCore.Qt.NoFocus )

    self._checkbox.stateChanged.connect( self.on_changed )
    self.clicked.connect( self.on_clicked )
    self._layout.addWidget( self._checkbox )

  #-----------------------------------------------------------------------------
  def merge( self ):
    with blocked( self._checkbox ):
      self._checkbox.setChecked( self.state )

    super().merge()

  #-----------------------------------------------------------------------------
  def commit( self ):
    self.push_state = self._schema.decode(
      val = self._checkbox.isChecked(),
      loc = self._loc )

    super().commit()

  #-----------------------------------------------------------------------------
  def set_enabled( self, enabled ):
    super().set_enabled( enabled )

    self._line.setEnabled( enabled )

  #-----------------------------------------------------------------------------
  def on_clicked( self ):
    self._checkbox.setChecked( not self._checkbox.isChecked() )

  #-----------------------------------------------------------------------------
  def on_changed( self, text ):
    pass


#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
class BoolTreeEditNode( TreeEditNode ):

  #-----------------------------------------------------------------------------
  def build_editor( self, parent, full ):

    editor = BoolEdit(
      manager = self._manager,
      schema = self._schema,
      parent = parent,
      loc = self._loc,
      readonly = self.readonly,
      popout = not full,
      manual_commit = True )

    return editor

  #-----------------------------------------------------------------------------
  def display_text(self):

    return f"{self.state._encode}"
