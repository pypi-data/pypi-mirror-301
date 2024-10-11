# -*- coding: UTF-8 -*-

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
import sys
import os
from copy import copy
import functools

from PySide2 import QtCore, QtGui, QtWidgets

import logging
log = logging.getLogger(__name__)

from partis.schema_meta.base import (
  name_re,
  name_cre )

from partis.schema import (
  SchemaValidationError,
  is_numeric,
  is_string,
  is_sequence,
  is_mapping,
  is_required,
  is_optional,
  is_schema_struct,
  is_valued_type,
  NotEvaluated,
  Loc )

from partis.schema.serialize.yaml import (
  loads,
  dumps )

from partis.utils import (
  odict )

from partis.view.base import (
  blocked,
  Heading1,
  Heading2,
  Heading3,
  HLine,
  ToolButton,
  EditLabel,
  rgba )

from partis.view.edit.var_tree import (
  VariableTree,
  VariableTreeItem )

from .type_combo_w import TypeComboWidget

heading_levels = [
  Heading1,
  Heading2,
  Heading3 ]

from .name_w import (
  RenameDialog )

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
class TreeEditItem( VariableTreeItem ):
  #-----------------------------------------------------------------------------
  def __init__( self, *args, **kwargs ):
    super().__init__( *args, **kwargs )

    self.node = None

  #-----------------------------------------------------------------------------
  def on_context_menu( self, index, point ):

    if self.node is not None:
      self.node.on_context_menu( index, point )

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
class TreeEditNode( QtCore.QObject ):
  """Base class of editable tree widgets
  """

  allowed_as_root = False

  COL_KEY = 0
  COL_SUBEDIT = 1
  COL_TYPE = 2
  COL_INDEX = 3
  COL_EDIT = 4
  NUM_COLS = 5

  # ( key, state )
  state_changed = QtCore.Signal(object, object)

  # ( key, new_key )
  key_changed = QtCore.Signal(object, object)

  # ( key )
  moved_up = QtCore.Signal(object)
  moved_down = QtCore.Signal(object)
  removed = QtCore.Signal(object)

  # ( key, expr_active )
  expr_toggled = QtCore.Signal(object, bool)

  #-----------------------------------------------------------------------------
  def __init__( self,
    manager,
    parent_node,
    tree_widget,
    tree_item,
    widget_stack,
    tree_node_map,
    detail_widget_map,
    schema,
    state = None,
    readonly = None,
    heading_level = 0,
    editable = True,
    movable = False,
    removable = False,
    subedit = False,
    expr_enabled = True,
    expr_active = False,
    key = None,
    key_edit = False,
    index = None,
    loc = None ):

    super( ).__init__()

    if loc is None:
      loc = Loc( filename = type(self).__module__ )

    self._loc = loc

    self._manager = manager
    self._tree_widget = tree_widget

    # stack of tree panels
    self._widget_stack = widget_stack

    # functions that map schemas to widgets
    self._tree_node_map = tree_node_map
    self._detail_widget_map = detail_widget_map

    self._tree = tree_item._tree
    self._tree_item = tree_item

    self._parent_node = parent_node
    # child tree nodes
    self._tree_nodes = odict()

    # child detail widget(s)
    self._detail_widgets = odict()

    self._key = None
    self._key_edit = key_edit

    self._index = None

    # NOTE: schema.schema ensures it is not a schema proxy
    self._schema = schema.schema
    self._state = None
    self._push_state = None
    self._view_built = False

    self._readonly = bool(readonly)
    self._editable = bool(editable)

    self._expr_enabled = expr_enabled
    self._expr_active = self._expr_enabled and expr_active
    self._expr = self._expr_enabled and ( len(self._schema.evaluated.supported) > 0 )
    self._movable = movable
    self._removable = removable
    self._subedit = subedit
    self._subedit_widget = None


    self._move_down_act = None
    self._move_up_act = None
    self._remove_act = None

    self._subedit_btn = None
    self._expr_btn = None

    self._edit_menu_actions = list()
    self._node_menu_actions = list()
    self.state = state

    if len(self._node_menu_actions) > 0:

      self._node_menu = QtWidgets.QMenu(self._tree)

      for act in self._node_menu_actions:
        if isinstance(act, QtWidgets.QAction):
          self._node_menu.addAction( act )

        elif isinstance(act, QtWidgets.QMenu):
          self._node_menu.addMenu( act )

        else:
          assert False

    if len(self._edit_menu_actions) > 0:

      self._edit_menu_btn = QtWidgets.QToolButton()


      self._tree.setItemWidget( self._tree_item, self.COL_KEY, self._edit_menu_btn )

      menu = QtWidgets.QMenu(self._edit_menu_btn)

      for act in self._edit_menu_actions:
        if isinstance(act, QtWidgets.QAction):
          menu.addAction( act )

        elif isinstance(act, QtWidgets.QMenu):
          menu.addMenu( act )

        else:
          assert False

      self._edit_menu_btn.setMenu(menu)
      self._edit_menu_btn.setPopupMode(QtWidgets.QToolButton.InstantPopup)


    self.key = key
    self.index = index

    self._tree_item.setData( self.COL_KEY, QtCore.Qt.EditRole, self )
    self._tree_item.setData( self.COL_SUBEDIT, QtCore.Qt.EditRole, self )
    self._tree_item.setData( self.COL_TYPE, QtCore.Qt.EditRole, self )
    self._tree_item.setData( self.COL_EDIT, QtCore.Qt.EditRole, self )

    if self._editable:

      self._tree_item.setFlags( QtCore.Qt.ItemIsEditable | QtCore.Qt.ItemIsEnabled )

      self._tree_item.clicked.connect( self.on_item_edit )

    # self.setAttribute( QtCore.Qt.WA_StyleSheet, True )
    # self.setAttribute( QtCore.Qt.WA_StyledBackground, True )

    # self.adjustSize()

  #-----------------------------------------------------------------------------
  @property
  def args( self ):
    return dict(
      manager = self._manager,
      tree_item = self._tree_item,
      widget_stack = self._widget_stack,
      tree_node_map = self._tree_node_map,
      detail_widget_map = self._detail_widget_map,
      schema = self._schema,
      state = self.state,
      movable = self._movable,
      removable = self._removable,
      subedit = self._subedit,
      expr_active = self._expr_active,
      key = self._key,
      key_edit = self._key_edit,
      index = self._index,
      loc = self._loc )

  #-----------------------------------------------------------------------------
  @property
  def nodes( self ):
    return self._tree_nodes

  #-----------------------------------------------------------------------------
  @property
  def schema( self ):
    return self._schema

  #-----------------------------------------------------------------------------
  def get_expanded(self):
    return self._tree_item.isExpanded()

  #-----------------------------------------------------------------------------
  def set_expanded(self, val):
    return self._tree_item.setExpanded( val )

  #-----------------------------------------------------------------------------
  expanded = property( get_expanded, set_expanded )

  #-----------------------------------------------------------------------------
  def set_expanded_all(self, val):
    self.expanded = val

    for k, v in self.nodes.items():
      v.set_expanded_all(val)

  #-----------------------------------------------------------------------------
  @property
  def readonly( self ):
    return self._readonly

  #-----------------------------------------------------------------------------
  def bg_color( self, col ):

    return None

  #-----------------------------------------------------------------------------
  def build_node_menu_actions( self ):
    self._node_menu_actions.append( QtWidgets.QAction(
      # QtGui.QIcon(self._manager.svgcolor('images/icons/move_down.svg')),
      "Expand all",
      self,
      statusTip="Expand all",
      triggered = self.on_expand_all ) )

    self._node_menu_actions.append( QtWidgets.QAction(
      # QtGui.QIcon(self._manager.svgcolor('images/icons/move_down.svg')),
      "Collapse all",
      self,
      statusTip = "Collapse all",
      triggered = self.on_collapse_all ) )
      
    if not self.readonly:
      if len(self.schema.preset_vals) > 0:
        preset_menu = QtWidgets.QMenu("Preset", self._tree)
        self._node_menu_actions.append(preset_menu)

        for i, preset in enumerate(self.schema.preset_vals):
          preset_menu.addAction( QtWidgets.QAction(
            preset.label,
            self,
            statusTip = preset.doc,
            triggered = functools.partial(self.on_preset_state, i) ) )

      paste_menu = QtWidgets.QMenu("Paste", self._tree)
      self._node_menu_actions.append(paste_menu)

      paste_menu.addAction( QtWidgets.QAction(
        "State",
        self,
        statusTip = "Paste state",
        triggered = self.on_paste_state ) )

      if self._key_edit:
        paste_menu.addAction( QtWidgets.QAction(
          "Key only",
          self,
          statusTip = "Paste key",
          triggered = self.on_paste_key ) )

    copy_menu = QtWidgets.QMenu("Copy", self._tree)
    self._node_menu_actions.append(copy_menu)

    copy_menu.addAction( QtWidgets.QAction(
      "Full state",
      self,
      statusTip = "Copy state",
      triggered = self.on_copy_state ) )

    copy_menu.addAction( QtWidgets.QAction(
      "Minimal state",
      self,
      statusTip = "Copy 'minimal' state",
      triggered = self.on_copy_state_min ) )

    copy_menu.addAction( QtWidgets.QAction(
      "Key only",
      self,
      statusTip = "Copy key",
      triggered = self.on_copy_key ) )

  #-----------------------------------------------------------------------------
  def build_edit_menu_actions( self ):
    if not self.readonly:
      if self._key_edit:
        self._edit_menu_actions.append( QtWidgets.QAction(
          # QtGui.QIcon(self._manager.svgcolor('images/icons/move_down.svg')),
          "Rename key",
          self,
          statusTip="Rename item key",
          triggered = self.on_rename_key ) )

      if self._movable:
        self._move_up_act = QtWidgets.QAction(
          QtGui.QIcon(self._manager.svgcolor('images/icons/move_up.svg')),
          "Move Up",
          self,
          statusTip="Move item up",
          triggered = self.move_up )

        self._edit_menu_actions.append( self._move_up_act )

        self._move_down_act = QtWidgets.QAction(
          QtGui.QIcon(self._manager.svgcolor('images/icons/move_down.svg')),
          "Move Down",
          self,
          statusTip="Move item down",
          triggered = self.move_down )

        self._edit_menu_actions.append( self._move_down_act )

      if self._removable:
        self._remove_act = QtWidgets.QAction(
          QtGui.QIcon(self._manager.svgcolor('images/icons/remove.svg')),
          "Remove",
          self,
          statusTip="Remove key and all children",
          triggered = self.remove )

        self._edit_menu_actions.append( self._remove_act )

  #-----------------------------------------------------------------------------
  def build_type( self ):

    if not self.readonly:
      if self._expr:
        if self._expr_active:
          self._expr_btn = ToolButton(
            name = 'script_active',
            tooltip = "Switch to Evaluated Input" )
        else:
          self._expr_btn = ToolButton(
            name = 'script',
            tooltip = "Switch to Evaluated Input" )

        self._expr_btn.clicked.connect( self.on_expr_toggle )

        self._tree.setItemWidget( self._tree_item, self.COL_TYPE, self._expr_btn )

  #-----------------------------------------------------------------------------
  def build_subedit( self ):

    if self._subedit:
      # self._subedit_btn = ToolButton(
      #   self._manager.svgcolor('images/icons/edit.svg'),
      #   "Open Full Viewer" if self.readonly else "Open Full Editor" )

      self._subedit_btn = ToolButton(
        name = 'edit',
        tooltip = "Open Full Viewer" if self.readonly else "Open Full Editor")

      self._subedit_btn.clicked.connect( self.on_subedit )

      self._tree.setItemWidget( self._tree_item, self.COL_SUBEDIT, self._subedit_btn )

  #-----------------------------------------------------------------------------
  def build_tooltip( self ):

    tooltip = "<FONT>" + self._schema.doc + "</FONT>"
    self._tree_item.setToolTip( self.COL_KEY, tooltip )
    # self._tree_item.setToolTip( self.COL_EDIT, tooltip )

  #-----------------------------------------------------------------------------
  def on_context_menu( self, index, point ):

    if index.column() == self.COL_KEY:
      self._node_menu.exec_( point )

  #-----------------------------------------------------------------------------
  def display_text(self):

    return ""

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
      self.state_changed.emit( self._key, self._state )

    else:
      # otherwise, the new state is *not* the outbound state, meaning that it is
      # assumed to be the inbound state.

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
    self.build_node_menu_actions()
    self.build_edit_menu_actions()
    self.build_type()
    self.build_subedit()
    self.build_tooltip()

  #-----------------------------------------------------------------------------
  def merge( self ):
    pass

  #-----------------------------------------------------------------------------
  def commit( self ):

    for k, v in self._tree_nodes.items():
      v.commit()

    if self._subedit_widget is not None:
      self._subedit_widget.commit()

  #-----------------------------------------------------------------------------
  def close( self ):

    if self._subedit_widget is not None:
      self._subedit_widget.close()
      self._subedit_widget = None

    for v in self._tree_nodes.values():
      v.close()

    for v in self._detail_widgets.values():
      v.close()

  #-----------------------------------------------------------------------------
  def set_state_editor( self, state, full ):
    self.push_state = state
    self.merge()

  #-----------------------------------------------------------------------------
  def get_state_editor( self, full ):
    return self.state

  #-----------------------------------------------------------------------------
  @property
  def removable( self ):
    return self._removable

  #-----------------------------------------------------------------------------
  @removable.setter
  def removable( self, val ):
    self._removable = val

    if self._remove_act:
      self._remove_act.setEnabled( val )

  #-----------------------------------------------------------------------------
  def refresh( self ):
    for v in self._tree_nodes.values():
      v.refresh()

    for v in self._detail_widgets.values():
      v.refresh()

  #-----------------------------------------------------------------------------
  def set_enabled( self, enabled ):
    self.setEnabled( enabled )

    if self._tree_item is not None:
      self._tree_item.setDisabled( not enabled )

    if self._tree_widget is not None:
      for v in self._tree_nodes.values():
        v.set_enabled( enabled )

  #-----------------------------------------------------------------------------
  def set_visible( self, visible ):
    self.setVisible( visible )

    if self._tree_item is not None:
      self._tree_item.setHidden( not visible )

  #-----------------------------------------------------------------------------
  @property
  def key( self ):
    return self._key

  #-----------------------------------------------------------------------------
  @key.setter
  def key( self, key ):
    if self._key == key:
      return

    old_key = self._key
    self._key = key

    self.key_changed.emit( old_key, self._key )

  #-----------------------------------------------------------------------------
  @property
  def treepath( self ):
    path = list()

    if self._parent_node is not None:
      _path = self._parent_node.treepath
      if _path != "":
        path.append(_path)

    if self._key is not None:
      path.append(self._key)

    return ".".join(path)

  #-----------------------------------------------------------------------------
  @property
  def index( self ):
    return self._index

  #-----------------------------------------------------------------------------
  @index.setter
  def index( self, val ):
    if val is None:
      self._index = None
      return

    val = int(val)

    if self._index == val:
      return

    self._index = val

    self._tree_item.setText( self.COL_INDEX,
      f"{self._index:4d}" )

  #-----------------------------------------------------------------------------
  def on_rename_key( self ):
    # key, ok = QtWidgets.QInputDialog.getText(
    #   self._manager,
    #   "Rename Key",
    #   "New Key:",
    #   text = self._key, )
    #
    # if ok:
    #   self.key = key

    dialog = RenameDialog(
      manager = self._manager,
      name = self._key )

    if dialog.exec() == QtWidgets.QDialog.Accepted:
      self.key = dialog.name

  #-----------------------------------------------------------------------------
  def move_up( self ):
    self.moved_up.emit( self._key )

  #-----------------------------------------------------------------------------
  def move_down( self ):
    self.moved_down.emit( self._key )

  #-----------------------------------------------------------------------------
  def remove( self ):
    if not self._removable:
      return

    self.removed.emit( self._key )

  #-----------------------------------------------------------------------------
  def on_expand_all(self):
    self.set_expanded_all( True )

  #-----------------------------------------------------------------------------
  def on_collapse_all(self):
    self.set_expanded_all( False )

  #-----------------------------------------------------------------------------
  def on_expr_toggle( self, *args ):
    self.expr_toggled.emit( self._key, not self._expr_active )


  #-----------------------------------------------------------------------------
  def on_subedit( self ):
    if self._subedit_widget is not None:
      return

    # close any currently open editors before creating a sub-editor
    delegate = self._tree.itemDelegate()
    delegate.close_editors()

    self._subedit_widget = self.build_editor(
      parent = self._widget_stack,
      full = True )
    self._subedit_widget.state_changed.connect(self.on_subedit_changed)

    self._subedit_widget.state = self.get_state_editor( full = True )

    self._widget_stack.push_widget(
      self._subedit_widget,
      name = self.treepath )

    self._subedit_widget.on_widget_stack_pop = lambda: self.on_subedit_popped()

  #-----------------------------------------------------------------------------
  def on_subedit_changed(self, state):
    self.set_state_editor( state = state, full = True )

  #-----------------------------------------------------------------------------
  def on_subedit_popped( self ):
    self._subedit_widget.commit()
    self._subedit_widget.close()
    self._subedit_widget = None


  #-----------------------------------------------------------------------------
  def create_child( self,
    schema,
    state = None,
    movable = False,
    removable = False,
    key = None,
    key_edit = False,
    index = None ):

    if key in self._tree_nodes:
      raise ValueError(f"child key already present: {key}")

    if key is None:
      i = len(self._state)
      key = f"new_key"

      while key in self._tree_nodes:
        i += 1
        key = f"new_key_{i}"

    if index is None:
      index = self._tree_item.childCount()

    # create new widgets for the tree and editor for this state
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
      movable = movable,
      removable = removable,
      key = key,
      key_edit = key_edit,
      index = index )

    child._tree_item.node = child

    self._tree_nodes[key] = child

    child.state_changed.connect( self.on_child_state_changed )
    child.key_changed.connect( self.on_child_key_changed )

    child.moved_up.connect( self.on_child_moved_up )
    child.moved_down.connect( self.on_child_moved_down )
    child.removed.connect( self.on_child_removed )
    child.expr_toggled.connect( self.on_child_expr_toggled )

    return child

  #-----------------------------------------------------------------------------
  def delete_child( self, key ):


    child = self._tree_nodes.pop( key )

    child.close()

    self._tree_item.removeChild( child._tree_item )


  #-----------------------------------------------------------------------------
  def on_child_state_changed( self, key, state ):
    raise NotImplementedError(f"Not implemented by class: {type(self).__name__}")

  #-----------------------------------------------------------------------------
  def on_child_moved_up( self, key ):
    raise NotImplementedError(f"Not implemented by class: {type(self).__name__}")

  #-----------------------------------------------------------------------------
  def on_child_moved_down( self, key ):
    raise NotImplementedError(f"Not implemented by class: {type(self).__name__}")

  #-----------------------------------------------------------------------------
  def on_child_removed( self, key ):
    raise NotImplementedError(f"Not implemented by class: {type(self).__name__}")

  #-----------------------------------------------------------------------------
  def on_child_key_changed( self, key, new_key ):
    raise NotImplementedError(f"Not implemented by class: {type(self).__name__}")

  #-----------------------------------------------------------------------------
  def on_child_expr_toggled( self, key, active ):
    raise NotImplementedError(f"Not implemented by class: {type(self).__name__}")

  #-----------------------------------------------------------------------------
  def on_item_edit( self, col ):
    if col == self.COL_EDIT:
      self._tree.editItem( self._tree_item, col )

  #-----------------------------------------------------------------------------
  def build_editor( self, parent, full ):
    raise NotImplementedError(f"Not implemented by class: {type(self).__name__}")

  #-----------------------------------------------------------------------------
  def on_copy_state(self):
    cb = QtWidgets.QApplication.instance().clipboard()
    cb.setText( dumps(self.state) )

  #-----------------------------------------------------------------------------
  def on_copy_state_min(self):
    cb = QtWidgets.QApplication.instance().clipboard()
    cb.setText( dumps(self.state, no_defaults = True) )


  #-----------------------------------------------------------------------------
  def on_paste_state(self):
    cb = QtWidgets.QApplication.instance().clipboard()
    data = cb.text()

    if data is None:
      return

    try:
      state = loads(
        data,
        schema = self._schema )
    except SchemaValidationError as e:
      self._manager.show_exception("Paste failed", e)
      return

    self.push_state = state
    self.merge()

  #-----------------------------------------------------------------------------
  def on_preset_state(self, idx):
    self.push_state = self._schema.decode(self._schema.preset_vals[idx].val)
    self.merge()

  #-----------------------------------------------------------------------------
  def on_paste_key(self):
    cb = QtWidgets.QApplication.instance().clipboard()
    data = cb.text()

    if not data:
      return

    if not name_cre.fullmatch(data):
      self._manager.show_exception("Paste failed", [f"Invalid key: {data}"])
      return

    self.key = data

  #-----------------------------------------------------------------------------
  def on_copy_key(self):
    cb = QtWidgets.QApplication.instance().clipboard()
    cb.setText( str(self.key) )
