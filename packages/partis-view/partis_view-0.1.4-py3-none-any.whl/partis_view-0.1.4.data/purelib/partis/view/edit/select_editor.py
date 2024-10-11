# -*- coding: UTF-8 -*-

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
import logging
log = logging.getLogger( __name__ )

from PySide2 import QtCore, QtGui, QtWidgets

from partis.view.base import (
  blocked )

from partis.schema import (
  is_mapping )

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
class SelectEditor( QtWidgets.QTreeWidget ):
  double_clicked = QtCore.Signal()

  def __init__(self,
    manager,
    editors,
    guesses = None,
    default = None ):

    super().__init__()

    self._manager = manager
    self._editors = editors
    self._guesses = guesses
    self._max_bias = 0.0
    self._max_editor = None

    self.setGeometry(QtCore.QRect(10, 10, 311, 321))
    self.setObjectName('select_editor')
    self.setSelectionMode( QtWidgets.QAbstractItemView.SingleSelection )
    self.resize(350, 400)

    # set context menu policy
    self.setContextMenuPolicy( QtCore.Qt.CustomContextMenu )
    self.customContextMenuRequested.connect( self.on_context_menu )
    self.itemDoubleClicked.connect( self.on_double_clicked )

    self.setHeaderHidden(True)

    self._items = dict()
    self._flat_items = dict()

    self.build(
      parent = self,
      editors = self._editors,
      items = self._items,
      path = list(),
      flat_items = self._flat_items )

    self.show()
    self.setAttribute( QtCore.Qt.WA_StyleSheet, True )
    self.setAttribute( QtCore.Qt.WA_StyledBackground, True )

  #+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
  def build( self, parent, editors, items, path, flat_items ):
    # options is a two level tree.
    # first level is overall type.
    for k, v in editors.items():
      _path = path + [ k, ]

      tree_item = QtWidgets.QTreeWidgetItem( parent )
      tree_item.setText(0, k)
      tree_item.setExpanded(1)

      if isinstance( v, dict ):
        items[k] = dict()

        self.build(
          parent = tree_item,
          editors = v,
          items = items[k],
          path = _path,
          flat_items = flat_items )

      else:
        if self._guesses is not None:
          bias = self._guesses.get(v, 0.0)
          tree_item._bias = bias
          tree_item.setText(0, f"{k} ({tree_item._bias:.0%})")

          if bias > self._max_bias:
            self._max_bias = bias
            self._max_editor = v
            self.setCurrentItem(tree_item)

        else:
          tree_item._bias = None
       

        flat_items[ ".".join(_path) ] = tree_item
        items[k] = tree_item

        tree_item._editor = v
        tree_item._name = k

  #-----------------------------------------------------------------------------
  def on_context_menu(self, point):
    item = self.itemAt( point )

    if item is not None:
      item.setSelected( True )
      if hasattr(item, 'on_context_menu'):
        item.on_context_menu( self.mapToGlobal(point) )

  #-----------------------------------------------------------------------------
  def on_double_clicked( self, item, col ):
    self.double_clicked.emit()


#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
class SelectEditorDialog( QtWidgets.QDialog ):
  #-----------------------------------------------------------------------------
  def __init__( self,
    manager,
    title,
    editors,
    guesses = None ):
    super().__init__()

    self._manager = manager

    self.setWindowTitle(title)
    self.setWindowIcon( QtGui.QIcon(manager.resource_path("images/icons/app_icon.png")) )

    self.setStyleSheet( manager.stylesheet )

    self.layout = QtWidgets.QGridLayout()
    self.setLayout(self.layout)

    self._readonly = QtWidgets.QCheckBox( "Open as Read-Only", self )

    self.add_btn = QtWidgets.QPushButton("Add")
    self.add_btn.clicked.connect(self.add)

    self.cancel_btn = QtWidgets.QPushButton("Cancel")
    self.cancel_btn.clicked.connect(self.reject)

    self.select_editor = SelectEditor(
      manager = self._manager,
      editors = editors,
      guesses = guesses )

    self.select_editor.double_clicked.connect( self.add )

    if self.select_editor._max_editor:
        with blocked( self._readonly ):
          self._readonly.setChecked( self.select_editor._max_editor.default_readonly )

    self.layout.addWidget(
      self._readonly,
      row = 0,
      column = 0,
      rowSpan = 1,
      columnSpan = 2 )

    self.layout.addWidget(
      self.select_editor,
      row = 1,
      column = 0,
      rowSpan = 1,
      columnSpan = 2 )

    self.layout.addWidget( self.add_btn, 2, 0 )
    self.layout.addWidget( self.cancel_btn, 2, 1 )

    self.selected = None
    self.readonly = None

    self.setAttribute( QtCore.Qt.WA_StyleSheet, True )
    self.setAttribute( QtCore.Qt.WA_StyledBackground, True )

  #-----------------------------------------------------------------------------
  def add(self):
    selected = self.select_editor.selectedItems()

    if len(selected) > 0 and hasattr(selected[0], "_editor"):
      self.selected = selected[0]._editor
      self.readonly = self._readonly.isChecked()

      self.accept()
