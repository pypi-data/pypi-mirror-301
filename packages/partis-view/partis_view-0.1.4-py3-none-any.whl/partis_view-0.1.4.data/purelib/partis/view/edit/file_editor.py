# -*- coding: UTF-8 -*-

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
from PySide2 import QtCore, QtGui, QtWidgets

import os
import os.path as osp
import h5py

from partis.utils import (
  ModelHint,
  getLogger )

log = getLogger( __name__ )

from partis.schema import (
  Loc )

from partis.view.base import (
  blocked,
  WidgetStack,
  DirectoryTreeWidget )


#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
class History:
  def __init__( self, max_len = None ):
    self._max_len = max_len
    self._cur_hist = -1
    self._hist = list()

  #-----------------------------------------------------------------------------
  def current( self ):
    if self._cur_hist < 0:
      return None

    state = self._hist[ self._cur_hist ]

    return state

  #-----------------------------------------------------------------------------
  def clear( self ):
    self._cur_hist = -1
    self._hist = list()

  #-----------------------------------------------------------------------------
  def push( self, state ):
    if ( self._max_len is not None
      and len(self._hist) == self._max_len
      and self._cur_hist > 0 ):

      self._hist.pop(0)
      self._cur_hist -= 1

    self._cur_hist += 1

    if self._cur_hist < len(self._hist):
      # pushing to a re-wound state discards the existing forward states
      self._hist = self._hist[:self._cur_hist]

    self._hist.insert( self._cur_hist, state )

  #-----------------------------------------------------------------------------
  def forward( self ):

    if self._cur_hist == len(self._hist)-1:
      state = None

    else:
      self._cur_hist += 1

      state = self.current()

    return state

  #-----------------------------------------------------------------------------
  def backward( self ):

    if self._cur_hist <= 0:
      state = None

    else:
      self._cur_hist -= 1

      state = self.current()

    return state


#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
class FileEditor ( QtWidgets.QWidget ):
  """Generic editor for a file

  Parameters
  ----------
  manager
  widget_stack : WidgetStack
  filename : None | PathLike
  state : None | object
  readonly : None | bool
    "editor" is meant only to display the state in a similar way as when editing,
    but not allow changing the values.
  fileonly : None | bool
    If True, editor state is backed only by a file, and will prompt when changes
    have not been saved before closing editor
    If False, editor state is *not necessarily* saved to a file (e.g. application settings),
    and will not prompt to "save-as" changes to a new file
  """

  default_readonly = False
  default_fileonly = True

  state_changed = QtCore.Signal(object, object)

  loaded = QtCore.Signal(object)
  loaded_backup = QtCore.Signal(object)

  saved = QtCore.Signal(object)
  saved_backup = QtCore.Signal(object)

  closed = QtCore.Signal(object)

  #-----------------------------------------------------------------------------
  def __init__( self,
    manager,
    widget_stack,
    filename = None,
    state = None,
    readonly = None,
    fileonly = None ):

    super().__init__()

    if readonly is None:
      readonly = self.default_readonly

    if fileonly is None:
      fileonly = self.default_fileonly

    self._manager = manager
    self._state = None
    self._push_state = None
    self._view_built = False

    self._widget_stack = widget_stack

    self._filename = filename
    self._has_changes = False
    self._hist = History( max_len = 100 )
    self._block_hist = False

    self._readonly = bool(readonly)
    self._fileonly = bool(fileonly)

    self.setAttribute( QtCore.Qt.WA_StyleSheet, True )
    self.setAttribute( QtCore.Qt.WA_StyledBackground, True )

    self.installEventFilter(self)

    self.state = state

  #-----------------------------------------------------------------------------
  @property
  def readonly( self ):
    return self._readonly

  #-----------------------------------------------------------------------------
  @property
  def fileonly( self ):
    return self._fileonly

  #-----------------------------------------------------------------------------
  @classmethod
  def guess( self, data ):
    return 0.0

  #-----------------------------------------------------------------------------
  @property
  def state( self ):
    return self._state

  #-----------------------------------------------------------------------------
  @state.setter
  def state( self, state ):
    if state is self._state:
      return
   # print("Does this go here: ", state)
    self._state = state

    if not self._block_hist:
      # NOTE: adds new state to history so that an undo -> redo sequence
      # will recover this state
      self._hist.push( state )

    if self._state is self._push_state:
      # set flag here in case events are being blocked
      self._has_changes = True

      # if the new state *is* the outbound state, then the state_changed signal
      # is emitted to propagate the changes "outward", toward the manager.
      self.state_changed.emit( self, self._state )

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
    if self._push_state == state:
      return
      
    self._push_state = state
    self.state = state

  #-----------------------------------------------------------------------------
  def build(self):
    pass

  #-----------------------------------------------------------------------------
  def merge(self):
    pass

  #-----------------------------------------------------------------------------
  @property
  def has_changes( self ):
    return self._has_changes

  #-----------------------------------------------------------------------------
  def clear_changes( self ):
    self._has_changes = False

  #-----------------------------------------------------------------------------
  def eventFilter( self, watched, event ):
    if ( event.type() != QtCore.QEvent.KeyPress
      or event.isAutoRepeat() ):
      return False

    seq = QtGui.QKeySequence( event.modifiers() | event.key() )

    state = None

    if seq == QtGui.QKeySequence.Undo:
      state = self._hist.backward()

    elif seq == QtGui.QKeySequence.Redo:
      state = self._hist.forward()

    else:
      return False

    if state is not None:

      self._block_hist = True

      with blocked( self ):
        self.state = state

      self._block_hist = False

      # need to emit here, since all events were blocked
      self.state_changed.emit( self, self._state )

    return True

  #-----------------------------------------------------------------------------
  @property
  def filename( self ):
    return self._filename

  #-----------------------------------------------------------------------------
  @filename.setter
  def filename( self, filename ):
    self._filename = filename

  #-----------------------------------------------------------------------------
  @property
  def filename_backup( self ):
    if self._filename is None:
      raise ValueError("Filename has not be set")

    return self._filename + ".bak"

  #-----------------------------------------------------------------------------
  def check_backup( self ):
    """Check whether there is a backup file that is more recent than the save file
    """
    if self.filename is None:
      return False

    path = self.filename
    bak_path = self.filename_backup

    if not osp.exists( path ) or not osp.exists( bak_path ):
      return False

    if os.state(path).st_mtime >= os.state(bak_path).st_mtime:
      # if save file is more recent, ignore backup file
      return False

    return True

  #-----------------------------------------------------------------------------
  def close( self ):
    self.closed.emit( self )

  #-----------------------------------------------------------------------------
  def commit(self):
    """Force pending internal/intermediate editor state into a change

    .. note::

      This should be called right before the state needs to be written to file
    """
    pass

  #-----------------------------------------------------------------------------
  def _load( self,
    backup = False,
    binary = False ):
    """Internal load method
    """

    if self._filename is None:
      raise ValueError("Filename has not be set")

    if backup:
      path = self.filename_backup
    else:
      path = self.filename

    if not osp.exists( path ):
      raise ValueError(f"File not found: {path}")

    if not osp.isfile( path ):
      raise ValueError(f"Path is not a file: {path}")

    with open( path, 'rb' ) as fp:
      data = fp.read()

    if not binary:
      data = data.decode( 'utf-8', errors = 'replace' )


    loc = Loc(
      filename = path )

    return data, loc

  #-----------------------------------------------------------------------------
  def load( self,
    backup = False ):
    """Load file contents into state
    """
    if backup:
      self.loaded_backup.emit(self)
    else:
      self.loaded.emit(self)

  #-----------------------------------------------------------------------------
  def _save( self,
    data,
    backup = False,
    binary = False,
    options = None ):
    """Internal save method
    """

    if self._filename is None:
      raise ValueError("Filename has not be set")

    if backup:
      path = self.filename_backup
    else:
      path = self.filename

    if not binary:
      data = data.encode( 'utf-8', errors = 'replace' )

    dir, file = osp.split( path )

    if not osp.exists( dir ):
      os.makedirs( dir )

    with open( path, 'wb' ) as fp:
      fp.write( data )

  #-----------------------------------------------------------------------------
  def save( self,
    backup = False,
    options = None ):
    """Save state to file
    """

    if backup:
      self.saved_backup.emit(self)
    else:
      self.saved.emit(self)

    self.clear_changes()

  #-----------------------------------------------------------------------------
  def save_options(self):
    return None

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
class TextFileEditor( FileEditor ):
  #-----------------------------------------------------------------------------
  def load( self, backup = False ):
    self._hist.clear()
    self.clear_changes()

    src, loc = self._load(
      backup = backup,
      binary = False )
    self.state = src #HDF5reader break at this line
    self.clear_changes()
    super().load( backup = backup )

  #-----------------------------------------------------------------------------
  @classmethod
  def guess( cls, data ):
    filename = data.filename
    bias = 0.0
    try:
      f = h5py.File(filename, 'r')
      f.close()
      return bias
    except Exception as e:
      pass
    try:
      src = data[str]

      # bias from being able to decode as a string
      bias += 0.01*len(src)

    except Exception as e:
      return 0.0
    return bias

  #-----------------------------------------------------------------------------
  def save( self,
    backup = False,
    options = None ):

    self._save(
      data = self.state,
      backup = backup,
      binary = False,
      options = options )

    super().save(
      backup = backup,
      options = options )
