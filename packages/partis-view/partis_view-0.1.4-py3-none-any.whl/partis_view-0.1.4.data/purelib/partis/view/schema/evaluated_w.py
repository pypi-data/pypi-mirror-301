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
  blocked,
  ScrollComboBox )

from partis.view.edit import (
  VariableTreeItem,
  CodeEdit )

from partis.view.highlight import (
  PygmentsHighlighter )

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

from .edit_w import (
  Edit )

from .tree_edit_w import TreeEditNode

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
class EvaluatedEdit( Edit ):

  #-----------------------------------------------------------------------------
  def build( self ):
    super().build()

    self._support_combo = ScrollComboBox()
    self._support_combo.readonly = self.readonly
    # self._support_combo.setVisible(not self.readonly)

    for k, v in self._schema.evaluated.supported.items():
      if v.lexer is not None:
        self._support_combo.addItem( v.name, userData = v )

    self._support_combo.currentIndexChanged.connect( self.on_support_changed )

    self._multiline = CodeEdit(
      manager = self._manager,
      expanding = False )

    self._multiline.code.setReadOnly( self.readonly )

    self._multiline.code.embed_func = True

    # self._multiline.code.textChanged.connect( self.commit )

    self._layout.addWidget( self._support_combo )
    self._layout.addWidget( self._multiline )

  #-----------------------------------------------------------------------------
  def merge( self ):

    with blocked( self._multiline, self._support_combo ):
      res = self._schema.evaluated.check( self.state._encode )

      if res is not None:
        support, src = res
        self._multiline.code.setPlainText( src )
        self._multiline.code.set_lang( support.lexer )

        index = self._support_combo.findData( support )
        self._support_combo.setCurrentIndex( index )

    super().merge()

  #-----------------------------------------------------------------------------
  def commit( self ):

    src = self._multiline.code.toPlainText()

    src = self._schema.evaluated.escaped(
      support = self._support_combo.currentData(),
      src = src )

    self.push_state = self._schema.decode(
      val = src,
      loc = self._loc )

    super().commit()

  #-----------------------------------------------------------------------------
  def set_enabled( self, enabled ):
    super().set_enabled( enabled )

    self._support_combo.setEnabled( enabled )
    self._multiline.setEnabled( enabled )

  #-----------------------------------------------------------------------------
  def on_support_changed( self, index ):
    support = self._support_combo.currentData()
    self._multiline.code.set_lang( support.lexer )
    self.commit()


#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
class EvaluatedTreeEditNode ( TreeEditNode ):

  #-----------------------------------------------------------------------------
  def __init__( self,
    expr_active = True,
    subedit = True,
    **kwargs ):

    super().__init__(
      expr_active = True,
      subedit = True,
      **kwargs )

  #-----------------------------------------------------------------------------
  def build_editor( self, parent, full ):

    editor = EvaluatedEdit(
      manager = self._manager,
      schema = self._schema,
      parent = parent,
      loc = self._loc,
      readonly = self.readonly,
      popout = not full,
      manual_commit = True  )

    editor._multiline.code.set_external_names(
      names = self._tree_widget.get_eval_names(
        context = self._schema.evaluated.context ) )

    return editor

  #-----------------------------------------------------------------------------
  def display_text(self):

    return f"\"{self.state._encode}\""
