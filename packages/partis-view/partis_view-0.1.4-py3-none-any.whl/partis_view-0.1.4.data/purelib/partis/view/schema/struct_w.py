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
  blocked )

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

from .tree_edit_w import (
  TreeEditNode,
  TreeEditItem,
  TreeEditWidget )

from .optional_w import OptionalTreeEditNode

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
class OptionalChild( ToolButton ):

  child_added = QtCore.Signal(str)

  #-----------------------------------------------------------------------------
  def __init__( self, key ):
    super().__init__(
      self._manager.svgcolor('images/icons/add.svg'),
      "Add" )

    self.clicked.connect( self.on_child_added )
    self._key = key

  #-----------------------------------------------------------------------------
  def on_child_added( self ):
    self.child_added.emit( self._key )


#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
class StructEdit( Edit ):

  #-----------------------------------------------------------------------------
  def build( self ):
    super().build()

    self._tree_editor = TreeEditWidget(
      manager = self._manager,
      widget_stack = self._widget_stack,
      tree_node_map = self._tree_node_map,
      get_eval_names = self._get_eval_names,
      schema = self._schema,
      readonly = self.readonly )

    self._tree_editor.state_changed.connect(self.on_changed)
    self._layout.addWidget( self._tree_editor )

  #-----------------------------------------------------------------------------
  def merge( self ):
    self._tree_editor.state = self.state
    super().merge()

  #-----------------------------------------------------------------------------
  def commit( self ):
    self._tree_editor.commit()
    super().commit()

  #-----------------------------------------------------------------------------
  def close( self ):
    self._tree_editor.close()

  #-----------------------------------------------------------------------------
  def on_changed( self, state ):
    self.push_state = state

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
class StructTreeEditNode( TreeEditNode ):
  allowed_as_root = True

  #-----------------------------------------------------------------------------
  def __init__( self,
    subedit = None,
    *args,
    **kwargs ):

    super().__init__( *args, **kwargs,
      subedit = True,
      editable = False )

  #-----------------------------------------------------------------------------
  def merge( self ):

    state = self.state

    for k, v in self._schema.struct.items():

      if state[k] is None:
        if k in self._tree_nodes:
          # the new state does not contain key that previously had a value
          if not isinstance( self._tree_nodes[k], OptionalTreeEditNode ):
            _state = self._tree_nodes[k].state
            self.delete_child( k )
            self.create_child_option( k, state = _state )

        else:
          self.create_child_option( k )

      elif k not in self._tree_nodes:
        # new state has a key that previously dit not have a value
        self.create_child( k, state = state[k] )

      elif (
        not isinstance(
          self._tree_nodes[k],
          self._tree_node_map(
            schema = self._schema.struct[k].schema,
            state = state[k] ) )
        or isinstance( self._tree_nodes[k], OptionalTreeEditNode ) ):

        # The key already had a value, but it was of a different type/schema

        self.delete_child( k )
        self.create_child( k, state = state[k] )

      else:
        # The new state is just updating an existing value
        child = self._tree_nodes[k]

        with blocked( child ):
          child.state = state[k]

    self._tree_item.sortChildren( self.COL_INDEX, QtCore.Qt.AscendingOrder )

    super().merge()

  #-----------------------------------------------------------------------------
  def create_child( self,
    key,
    state = None ):

    if key in self._tree_nodes:
      raise ValueError(f"child key already present: {key}")

    schema = self._schema.struct[key].schema


    index = list(self._schema.struct.keys()).index( key )

    child = self._tree_node_map( schema = schema, state = state )(
      manager = self._manager,
      parent_node = self,
      tree_widget = self._tree_widget,
      tree_item = TreeEditItem(
        parent = self._tree_item ),
      widget_stack = self._widget_stack,
      tree_node_map = self._tree_node_map,
      detail_widget_map = self._detail_widget_map,
      schema = schema,
      state = state,
      readonly = self.readonly,
      movable = False,
      removable = is_optional( schema.default_val ),
      key = key,
      key_edit = False,
      index = index )

    child._tree_item.node = child

    child.state_changed.connect( self.on_child_state_changed )
    child.removed.connect( self.on_child_removed )
    child.expr_toggled.connect( self.on_child_expr_toggled )

    self._tree_nodes[key] = child

    return child

  #-----------------------------------------------------------------------------
  def create_child_option( self,
    key,
    state = None ):

    if key in self._tree_nodes:
      raise ValueError(f"child key already present: {key}")

    schema = self._schema.struct[key].schema
    index = list(self._schema.struct.keys()).index( key )

    child = OptionalTreeEditNode(
      manager = self._manager,
      parent_node = self,
      tree_widget = self._tree_widget,
      tree_item = TreeEditItem(
        parent = self._tree_item ),
      widget_stack = self._widget_stack,
      tree_node_map = self._tree_node_map,
      detail_widget_map = self._detail_widget_map,
      schema = schema,
      state = state,
      readonly = self.readonly,
      movable = False,
      removable = False,
      key = key,
      key_edit = False,
      index = index )

    child._tree_item.node = child
    child.option_added.connect( self.on_child_option_added )

    self._tree_nodes[key] = child

  #-----------------------------------------------------------------------------
  def on_child_state_changed( self, key, state ):

    _state = copy( self._state )
    _state[key] = state

    self.push_state = _state

  #-----------------------------------------------------------------------------
  def on_child_removed( self, key ):
    state = self._tree_nodes[key].state

    self.delete_child( key )
    self.create_child_option(
      key = key,
      # Optional stores the state that was set before being removed
      state = state )

    self._tree_item.sortChildren( self.COL_INDEX, QtCore.Qt.AscendingOrder )

    self.on_child_state_changed( key, None )

  #-----------------------------------------------------------------------------
  def on_child_option_added( self, key ):

    state = None

    if self._state is not None and self._state[key] is not None:
      state = self._state[key]

    elif self._tree_nodes[key].state is not None:
      # retreive state that was previously stored in optional
      state = self._tree_nodes[key].state

    self.delete_child( key )

    child = self.create_child(
      key = key,
      state = state )

    child.expanded = True

    self._tree_item.sortChildren( self.COL_INDEX, QtCore.Qt.AscendingOrder )

    self.on_child_state_changed( key, child.state )

  #-----------------------------------------------------------------------------
  def on_child_expr_toggled( self, key, active ):

    state = self._tree_nodes[key].state

    if hasattr( self._tree_nodes[key], '_bak_state'):
      _state = self._tree_nodes[key]._bak_state
    else:
      _state = None

    if _state is None:
      if active:
        schema = self._schema.struct[key].schema
        evaluated = schema.evaluated
        support = next(iter(evaluated.supported.values()))

        _state = schema.decode(
          val = evaluated.escaped( support, str(state._encode) ),
          loc = self._loc )

      else:
        _state = None

    self.delete_child( key )

    child = self.create_child(
      key = key,
      state = _state )

    # used when toggling between literal/expression
    child._bak_state = state

    self._tree_item.sortChildren( self.COL_INDEX, QtCore.Qt.AscendingOrder )

    self.on_child_state_changed( key, child.state )

  #-----------------------------------------------------------------------------
  def build_editor( self, parent, full ):

    editor = StructEdit(
      manager = self._manager,
      widget_stack = self._widget_stack,
      tree_node_map = self._tree_node_map,
      get_eval_names = self._tree_widget._get_eval_names,
      schema = self._schema if full else self._schema.msg,
      parent = parent,
      loc = self._loc,
      readonly = self.readonly )

    return editor
