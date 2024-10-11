# -*- coding: UTF-8 -*-

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
import sys
import os

from PySide2 import QtCore, QtGui, QtWidgets

import logging
log = logging.getLogger(__name__)

from pygments import (
  lexers )

from partis.view.base import (
  Heading1,
  Heading2,
  Heading3,
  HLine,
  ToolButton,
  blocked,
  AsyncTarget )

from partis.view.edit import (
  CodeEdit )

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
  Edit,
  RestrictedEdit )

from .tree_edit_w import TreeEditNode

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
class ColorEdit( Edit ):
  #-----------------------------------------------------------------------------
  def build( self ):
    super().build()

    self._picker = QtWidgets.QColorDialog(QtGui.QColor(*self.state.rgb), self)
    self._picker.setWindowFlags(QtCore.Qt.Widget)
    self._picker.setOptions(
      QtWidgets.QColorDialog.NoButtons
      | QtWidgets.QColorDialog.DontUseNativeDialog )

    self._picker.currentColorChanged.connect(self.on_color_changed)

    self._layout.addWidget( self._picker )
    self._layout.addStretch()

  #-----------------------------------------------------------------------------
  def merge( self ):

    with blocked( self._picker ):
      self._picker.setCurrentColor( QtGui.QColor(*self.state.rgb) )

    super().merge()

  #-----------------------------------------------------------------------------
  def commit( self ):
    color = self._picker.currentColor()
    color = f"#{color.red():02X}{color.green():02X}{color.blue():02X}"

    self.push_state = self._schema.decode(
      val = color,
      loc = self._loc )

    super().commit()

  #-----------------------------------------------------------------------------
  def set_enabled( self, enabled ):
    super().set_enabled( enabled )

  #-----------------------------------------------------------------------------
  def on_color_changed( self, color ):
    pass



#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
class ColorTreeEditNode ( TreeEditNode ):
  #-----------------------------------------------------------------------------
  def __init__( self,
    schema,
    subedit = None,
    **kwargs ):

    super().__init__(
      schema = schema,
      subedit = True,
      **kwargs )

  #-----------------------------------------------------------------------------
  def build_editor( self, parent, full ):

    editor = ColorEdit(
      manager = self._manager,
      schema = self._schema,
      parent = parent,
      loc = self._loc,
      readonly = self.readonly,
      popout = not full,
      manual_commit = True )

    return editor

  #----------------------------------------------------------------------------#
  def merge( self ):

    self._tree_item.setData( self.COL_EDIT, QtCore.Qt.DecorationRole, QtGui.QColor(*self.state.rgb) )

    super().merge()

  #-----------------------------------------------------------------------------
  # def bg_color( self, col ):
  #   return QtGui.QColor(*self.state.rgb)

  #-----------------------------------------------------------------------------
  def display_text(self):

    return f"{self.state._encode}"
