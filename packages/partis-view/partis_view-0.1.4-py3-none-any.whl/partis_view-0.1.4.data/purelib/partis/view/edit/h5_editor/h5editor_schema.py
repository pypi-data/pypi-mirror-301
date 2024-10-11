import os
import os.path as osp
import re
import h5py
from copy import copy
import functools

from PySide2 import QtCore, QtGui, QtWidgets

import ruamel.yaml

from pygments import (
  lexers )

from partis.utils import (
  ModelHint,
  getLogger,
  head,
  tail )

log = getLogger(__name__)

from partis.schema import (
  SchemaError,
  Loc,
  is_schema,
  is_sequence,
  is_string,
  is_mapping,
  SchemaStruct )

from partis.schema.prim.any_prim import (
  any_prim_cases,
  AnyPrim )

from partis.schema.serialize.yaml import (
  loads,
  dumps )

from partis.view.base import (
  blocked )

from partis.view.edit import (
  FileEditor )

from partis.view.schema import (
  TreeEditWidget,
  TreeEditNodeMap )


#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
class H5FileEditor( FileEditor ):
  default_schema = AnyPrim

  #-----------------------------------------------------------------------------
  def __init__( self,
    manager,
    widget_stack,
    schema = None,
    filename = None,
    state = None,
    readonly = None ):

    self._schema = schema or type(self).default_schema

    # ensure not a proxy
    self._schema = self._schema.schema

    if not is_schema( self._schema ):
      raise ValueError(f"'schema' or class 'default_schema' must be a Schema: {self._schema}")

    if state is None:
      state = self._schema.decode( self._schema.init_val )

    super().__init__(
      manager = manager,
      widget_stack = widget_stack,
      filename = filename,
      state = state,
      readonly = readonly )

  #-----------------------------------------------------------------------------
  @property
  def schema( self ):
    return self._schema

  #-----------------------------------------------------------------------------
  def build_objects(self, fileobject):
    src = {}
    for i in fileobject:
      dset = fileobject[i]
      try:
        src['shape of ' + i] = dset.shape
      except Exception as e:
        pass
    fileobject.close()
    return src


  #-----------------------------------------------------------------------------
  def load( self, backup = False ):

    self._hist.clear()
    self.clear_changes()
    state = None
    if osp.exists(self.filename):
      try:
        f = h5py.File(self.filename, 'r')
        src = self.build_objects(f)
        #print(src)
        #val = "Why is this not working for meeeee"
        loc = Loc(
          filename = self.filename)
        state = self._schema.schema.decode(val = src, loc = loc )
        self.state = state
        self.clear_changes()
      except:
        pass
    #super().load( backup = backup )

  #-----------------------------------------------------------------------------
  def save( self,
    backup = False,
    options = None ):

    options = options or dict()

    self._save(
      data = dumps(
        self.state,
        no_defaults = options.get('no_defaults', True) ),
      backup = backup,
      binary = False,
      options = options )

    super().save(
      backup = backup,
      options = options )

  #-----------------------------------------------------------------------------
  def save_options(self):
    return {
      'no_defaults' : ("No Defaults", True, f"""
        If set, will attempt to remove values that are equivalent to the default
        values defined for the schema {self._schema.__name__}
        """ ) }

  #-----------------------------------------------------------------------------
  @classmethod
  def specialize_schema( cls, schema ):

    # ensure not a schema proxy
    schema = schema.schema

    class _Editor( cls ):
      default_schema = schema


    return _Editor

  #-----------------------------------------------------------------------------
  @classmethod
  def guess( cls, data ):
    
    filename = data.filename
    bias = 0.0
    try:
      f = h5py.File(filename, 'r')
      bias = 100.0
      f.close()
      return bias
    except Exception as e:
      return bias


#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
class H5TreeFileEditor( H5FileEditor):

  #-----------------------------------------------------------------------------
  def __init__( self,
    manager,
    widget_stack,
    schema = None,
    filename = None,
    state = None,
    readonly = None ):

    super().__init__(
      manager = manager,
      widget_stack = widget_stack,
      schema = schema,
      filename = filename,
      state = state,
      readonly = readonly )

  #-----------------------------------------------------------------------------
  def build( self ):
    from partis.view.edit.plugin import SchemaEditNodePlugin
    from partis.utils.plugin import plugin_manager

    node_map = dict()

    for plugin in plugin_manager.plugins( SchemaEditNodePlugin ):
      if isinstance( self, plugin.editor ):
        node_map.update( plugin.node_map )

    tree_node_map = TreeEditNodeMap(node_map)

    self.layout = QtWidgets.QVBoxLayout( self )
    self.setLayout(self.layout)

    self.layout.setContentsMargins(0,0,0,0)
    self.layout.setSpacing(0)

    self.edit_tree = TreeEditWidget(
      manager = self._manager,
      widget_stack = self._widget_stack,
      tree_node_map = tree_node_map,
      schema = self.schema,
      state = self.state,
      readonly = self.readonly,
      get_eval_names = self.get_eval_names )

    self.edit_tree.state_changed.connect( self.on_edit_tree_state_changed )

    self.layout.addWidget( self.edit_tree )

  #-----------------------------------------------------------------------------
  def merge( self ):

    with blocked( self.edit_tree ):
      self.edit_tree.state = self.state

    super().merge()

  #-----------------------------------------------------------------------------
  def commit(self):
    self.edit_tree.commit()
    super().commit()

  #-----------------------------------------------------------------------------
  def on_edit_tree_state_changed( self, state ):
    self.push_state = state
    # if self.state is None or state is None:
    #   return

    # _state = copy( self.state )
    #
    # for k, v in state.items():
    #   _state[k] = v
    #
    # self.state = _state

  #-----------------------------------------------------------------------------
  def get_eval_names( self, context = None ):
    return dict()

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
