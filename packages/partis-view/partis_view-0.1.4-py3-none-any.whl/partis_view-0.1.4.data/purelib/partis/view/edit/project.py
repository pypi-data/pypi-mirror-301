# -*- coding: UTF-8 -*-

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
import os
import os.path as osp
import sys
import trio
from collections.abc import (
  Mapping,
  MutableMapping,
  Sequence,
  Set,
  Iterable )

from PySide2 import QtCore, QtGui, QtWidgets

import ruamel.yaml

from partis.utils import (
  ModelHint,
  getLogger )

log = getLogger( __name__ )

from partis.schema.serialize.yaml import (
  dumps )

from partis.view.base import (
  WidgetStack,
  AsyncTarget,
  FileDialogOptions)

from .workdir import WorkDirWidget

from .select_editor import (
  SelectEditorDialog )

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
class InstanceMap( MutableMapping ):
  #-----------------------------------------------------------------------------
  def __init__(self):
    self._data = list()

  #-----------------------------------------------------------------------------
  def __str__(self):
    return str(self._data)

#-----------------------------------------------------------------------------
  def __repr__(self):
    return repr(self._data)

  #-----------------------------------------------------------------------------
  def __len__(self):
    return len(self._data)

  #-----------------------------------------------------------------------------
  def __iter__(self):
    return iter([k for k,v in self._data])

  #-----------------------------------------------------------------------------
  def __getitem__(self, key):
    for k,v in self._data:
      if k is key:
        return v

    raise KeyError(f"{key}")

  #-----------------------------------------------------------------------------
  def __setitem__(self, key, value):
    for i, (k,v) in enumerate(self._data):
      if k is key:
        self._data[i] = (key, value)
        return

    self._data.append((key, value))

  #-----------------------------------------------------------------------------
  def __delitem__(self, key):
    for i, (k,v) in enumerate(self._data):
      if k is key:
        self._data.pop(i)
        return

    raise KeyError(f"{key}")

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
class LoaderData( InstanceMap ):
  #-----------------------------------------------------------------------------
  def __init__(self, filename):
    self.filename = filename
    self._data = list()
    if osp.exists(filename):
        #TODO:
        #How to indicate that the failure to open HDF5 file means guess should be 0%
      try:

        with open( filename, 'rb' ) as fp:
          src_b = fp.read()

        self[bytes] = src_b

        try:
          src_t = src_b.decode( 'utf-8', errors = 'replace' )
          self[str] = src_t

          try:
            src_y = ruamel.yaml.round_trip_load( src_t )
            self[ruamel.yaml.comments.CommentedBase] = src_y

          except Exception as e:
            pass
        except Exception as e:
          pass

      except Exception as e:
          pass

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
def _guess_editor( editors, data ):
  guesses = InstanceMap()
  for k, v in editors.items():
    if isinstance( v, Mapping ):
      guesses.update(_guess_editor(v, data))

    else:
      try:
        bias = v.guess(data)

        bias = bias or 0.0

        if bias > 0.0:
          guesses[v] = bias
          
      except Exception as e:
        pass

  return guesses

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
def guess_editor( editors, data ):
  guesses = _guess_editor( editors, data )
  max_bias = 0.0
  for v, bias in guesses.items():

    max_bias = max(max_bias, bias)

  if max_bias > 0.0:

    for v, bias in guesses.items():
      guesses[v] = bias / max_bias

  return guesses

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
class Project( QtWidgets.QWidget ):
  """The whole project
  """

  editor_changed = QtCore.Signal(object)

  #-----------------------------------------------------------------------------
  def __init__( self,
    manager,
    editor_map,
    root_dir = None ):
    super().__init__( )

    self._manager = manager
    self._editor_map = editor_map
    self._editors = list()
    # self._editor_stacks = list()


    self.layout = QtWidgets.QVBoxLayout( self )
    self.setLayout(self.layout)

    self.layout.setContentsMargins(0,0,0,0)
    self.layout.setSpacing(0)

    self.splitter = QtWidgets.QSplitter( self )
    self.layout.addWidget( self.splitter )

    self.workdir = WorkDirWidget(
      manager = self._manager,
      root_dir = root_dir )

    self.workdir.file_open.connect( self.on_open_editor )

    self.workdir.file_open_as.connect(lambda path: self.on_open_editor( path, open_as = True ))

    self.editor_tabs = QtWidgets.QTabWidget()
    self.editor_tabs.setTabsClosable( True )
    self.editor_tabs.tabCloseRequested.connect( self.on_close_editor )

    self.splitter.insertWidget( 0, self.workdir )
    self.splitter.insertWidget( 1, self.editor_tabs )

    width = QtWidgets.QApplication.instance().desktop().availableGeometry(self).width()
    self.splitter.setSizes([width * 0.25, width * 0.75])

    # self.setAttribute( QtCore.Qt.WA_StyleSheet, True )
    # self.setAttribute( QtCore.Qt.WA_StyledBackground, True )

  #-----------------------------------------------------------------------------
  def current_index( self ):
    if len(self._editors) == 0:
      return None

    return self.editor_tabs.currentIndex()

  #-----------------------------------------------------------------------------
  def editor( self, editor = None ):
    if isinstance( editor, int ):
      editor = self._editors[ editor ]

    if editor is None:
      index = self.current_index()

      if index is None:
        editor = None
      else:
        editor = self._editors[ index ]

    return editor

  #-----------------------------------------------------------------------------
  def set_root_dir( self, root_dir ):

    self.workdir.root_dir = root_dir

  #-----------------------------------------------------------------------------
  def add_editor( self,
    editor_class,
    state = None,
    readonly = None,
    name = None,
    filename = None,
    tab_index = None ):
    if name is None:
      if filename is not None:

        filename = osp.abspath( filename )

        dir, name = osp.split(filename)

      else:
        name = "untitled"

    widget_stack = WidgetStack(
      manager = self._manager )

    # self._editor_stacks.append( widget_stack )

    load_failed = False

    editor = editor_class(
      manager = self._manager,
      widget_stack = widget_stack,
      state = state,
      filename = filename,
      readonly = readonly )

    editor.clear_changes()

    if filename is not None:
      if osp.exists( filename ) and state is None:
        try:
          editor.load()

        except Exception as e:
          self._manager.show_exception(
            title = f"Error loading {filename}",
            exc = e )

          log.error( ModelHint.cast(e) )

          load_failed = True


    if tab_index is None:
      # add to end of tab bar
      self.editor_tabs.addTab(
        widget_stack,
        name + (" (readonly)" if readonly else "") )

      self._editors.append( editor )

      self.editor_tabs.setCurrentIndex( len(self._editors)-1 )

    else:
      tab_index = max(0, min(len(self._editors), int(tab_index)) )

      self.editor_tabs.insertTab(
        tab_index,
        widget_stack,
        name + (" (readonly)" if readonly else "") )

      self._editors.insert( tab_index, editor )

      self.editor_tabs.setCurrentIndex( tab_index )

    widget_stack.push_widget( editor )
    if load_failed:
      # TODO: surely there is a better way to do this. The problem is if the widgets
      # are never added to any parent it seems to eventually cause a seg. fault.
      # Clearly a bug in Qt/Python memory management confict, but this seems to work ok
      self.on_close_editor( editor = editor, allow_cancel = False )

      return None

    self.editor_changed.emit( self.editor() )

    return editor

  #-----------------------------------------------------------------------------
  def remove_editor( self, editor = None ):
    editor = self.editor( editor )

    if editor is None:
      return

    editor.close()

    index = self._editors.index( editor )
    self.editor_tabs.removeTab( index )
    self._editors.pop( index )

    self.editor_changed.emit( self.editor() )


  #-----------------------------------------------------------------------------
  async def close( self ):
    while len(self._editors) > 0:
      await self.close_editor( allow_cancel = False )

  #-----------------------------------------------------------------------------
  async def save_editor_as( self, editor = None ):
    editor = self.editor( editor )

    if editor is None:
      return

    target = AsyncTarget()

    save_dialog = FileDialogOptions(
      self,
      editor.save_options() )

    save_dialog.setFileMode(QtWidgets.QFileDialog.AnyFile)
    save_dialog.setAcceptMode(QtWidgets.QFileDialog.AcceptSave)
    save_dialog.fileSelected.connect( target.on_result )
    save_dialog.rejected.connect( target.on_result )
    save_dialog.open()

    result, error = await target.wait()

    if result is not None:
      editor.filename = result
      editor.commit()
      editor.save( options = save_dialog.options )

      tab_index = self._editors.index(editor)

      if not editor.readonly:
        self.editor_tabs.setTabText(
          tab_index,
          osp.basename(editor.filename) )

      else:
        # convert editor to be writable, since the file was saved presumably to change
        # the contents
        state = editor.state
        editor_class = type(editor)

        self.remove_editor(editor)

        self.add_editor(
          editor_class,
          state = state,
          readonly = False,
          filename = result,
          tab_index = tab_index )

  #-----------------------------------------------------------------------------
  async def save_editor( self, editor = None ):

    editor = self.editor( editor )

    if editor is None:
      return

    if editor.filename is None:
      await self.save_editor_as()

    else:
      editor.commit()
      editor.save()

  #-----------------------------------------------------------------------------
  async def open_editor( self,
    filename = None,
    editor_class = None,
    readonly = None ,
    open_as = False ):
    guesses = None
    if editor_class is None and filename is not None:
      guesses = guess_editor(
        editors = self._editor_map.editors, 
        data = LoaderData(filename) )
      if not open_as and len(guesses) == 1:
        editor_class = next(iter(guesses))
    if editor_class is None:

      if filename is None:
        title = f"Select Editor for 'untitled'"
      else:
        title = f"Select Editor for '{filename}'"
      target = AsyncTarget()

      select_dialog = SelectEditorDialog(
        title = title,
        manager = self._manager,
        editors = self._editor_map.editors,
        guesses = guesses )
      select_dialog.accepted.connect( target.on_result )
      select_dialog.rejected.connect( target.on_result )
      select_dialog.open()

      result, error = await target.wait()

      editor_class = select_dialog.selected
      readonly = select_dialog.readonly
    if editor_class is not None:

      return self.add_editor(
        editor_class = editor_class,
        filename = filename,
        readonly = readonly )


    return None

  #-----------------------------------------------------------------------------
  async def close_editor( self, editor = None, allow_cancel = True ):

    editor = self.editor( editor )

    if editor is None:
      return

    editor.commit()

    if editor.has_changes and (editor.filename is not None or editor.fileonly):
      target = AsyncTarget()

      if editor.filename is not None:
        name = editor.filename
      else:
        name = 'untitled'

      message_box = QtWidgets.QMessageBox()
      message_box.setWindowTitle( f"Closing '{name}'" )
      message_box.setWindowIcon( QtGui.QIcon(self._manager.resource_path("images/icons/app_icon.png")) )
      message_box.setStyleSheet( self._manager.stylesheet )
      message_box.setText(
        f"Closing editor with changes for '{name}'.")

      if allow_cancel:
        message_box.setStandardButtons(
          QtWidgets.QMessageBox.Save
          | QtWidgets.QMessageBox.Cancel
          | QtWidgets.QMessageBox.Discard )

      else:
        message_box.setStandardButtons(
          QtWidgets.QMessageBox.Save
          | QtWidgets.QMessageBox.Discard )

      message_box.setDefaultButton( QtWidgets.QMessageBox.Save )


      message_box.finished.connect( target.on_result )
      message_box.open()

      result, error = await target.wait()

      if result == QtWidgets.QMessageBox.Cancel:
        return

      elif result == QtWidgets.QMessageBox.Save:

        await self.save_editor( editor )

      # discard -> simply close editor

    self.remove_editor()


  #-----------------------------------------------------------------------------
  def on_open_editor( self, filename = None, editor_class = None, open_as = False ):
    self._manager._manager._async_queue.append( ( self.open_editor, filename, editor_class, open_as ) )

  #-----------------------------------------------------------------------------
  def on_save_editor( self, editor = None ):
    self._manager._manager._async_queue.append( (self.save_editor, editor) )

  #-----------------------------------------------------------------------------
  def on_save_editor_as( self, editor = None ):
    self._manager._manager._async_queue.append( (self.save_editor_as, editor) )

  #-----------------------------------------------------------------------------
  def on_close_editor( self, editor = None, allow_cancel = True ):
    self._manager._manager._async_queue.append( (self.close_editor, editor, allow_cancel ) )

  #-----------------------------------------------------------------------------
  def on_close( self ):
    self._manager._manager._async_queue.append( (self.close, ) )

  #-----------------------------------------------------------------------------
  async def test_project_editors( self ):

    await self._test_project_editors( self._editor_map.editors )

  #-----------------------------------------------------------------------------
  async def _test_project_editors( self, editors ):
    for i, (editor_name, editor_class) in enumerate( editors.items() ):

      log.info(f"testing editor: {editor_name}")

      if isinstance( editor_class, dict ):
        return self._test_project_editors( editor_class )

      editor = await self.open_editor(
        filename = f"test_{i}.txt",
        editor_class = editor_class )

      assert( editor is not None )

      self._manager._manager.test( editor )
