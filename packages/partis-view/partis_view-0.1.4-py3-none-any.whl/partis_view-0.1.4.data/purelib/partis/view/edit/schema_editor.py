import os
import os.path as osp
import re
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
class SchemaFileEditor( FileEditor ):
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
  def load( self, backup = False ):
    self._hist.clear()
    self.clear_changes()

    state = None

    src, loc = self._load(
      backup = backup,
      binary = False )
    state = loads(
      src = src,
      schema = self._schema,
      loc = loc )
    self.state = state
    self.clear_changes()

    super().load( backup = backup )

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

    schema = cls.default_schema.schema

    try:
      src = data[str]
      val = data[ruamel.yaml.comments.CommentedBase]

      # bias from being able to parse the string as a yaml document
      bias += 0.02*len(src)

    except Exception as e:
      return 0.0

    schema_hash = ''

    if is_mapping( val ) and '__schema_hash__' in val:
      schema_hash = val.pop('__schema_hash__')

    elif is_sequence( val ):
      for i, v in enumerate(val):
        if is_mapping( v ) and '__schema_hash__' in v:
          schema_hash = v['__schema_hash__']
          val.pop(i)
          break

    if schema_hash != '':
      if schema_hash == schema.schema_hash:
        # 6 bits per character in base-64 encoded hash
        bias += 6.0*len(schema_hash)

    try:
      _val = schema.decode(
        val = val )

      bias += float(_val._bias)

    except Exception as e:
      return 0.0

    return bias

    # hash_pattern = r"__schema_hash__[\t ]*\:[\t ]*[\'\"]?([a-zA-Z0-9\-\_]+)[\'\"]?"
    # hash_pattern = re.compile(hash_pattern)
    #
    # similarity = 0.0
    #
    # try:
    #
    #   if not osp.exists(filename):
    #     try:
    #       return lexers.guess_lexer_for_filename(filename, "")
    #     except:
    #       return 0.0
    #
    #   head_str = head(
    #     path = filename,
    #     n = 10 )
    #
    #   if filename is not None:
    #
    #     try:
    #
    #       lexer = lexers.guess_lexer_for_filename(filename, "\n".join(head_str))
    #
    #       if isinstance(lexer, lexers.YamlLexer):
    #         similarity = 1.0
    #
    #     except:
    #       pass
    #
    #   lines = (
    #     head_str
    #     + tail(
    #       path = filename,
    #       n = 10 ) )
    #
    #
    #   for l in lines:
    #
    #     m = hash_pattern.match( l )
    #
    #     if m:
    #       if m.group(1) == schema.schema_hash:
    #         similarity = max( similarity, 10.0 )
    #
    # except:
    #   log.exception("Error while parsing guess", exc_info = True )
    #
    # return similarity

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
class SchemaTreeFileEditor( SchemaFileEditor ):

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
    from .plugin import SchemaEditNodePlugin
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
class SchemaStructTreeFileEditor( SchemaFileEditor ):
  guess_strict = False

  #-----------------------------------------------------------------------------
  def __init__( self,
    manager,
    widget_stack,
    schema = None,
    filename = None,
    state = None,
    readonly = None,
    hidden = None ):

    if hidden is None:
      hidden = list()

    self._hidden = hidden

    super().__init__(
      manager = manager,
      widget_stack = widget_stack,
      schema = schema,
      filename = filename,
      state = state,
      readonly = readonly )

    assert isinstance( self._schema, SchemaStruct )

  #-----------------------------------------------------------------------------
  def build( self ):

    from .plugin import SchemaEditNodePlugin
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


    self.tabs = QtWidgets.QTabWidget()
    self.layout.addWidget( self.tabs )

    self._struct_editors = dict()

    for k, v in self.schema.struct.items():
      if k in self._hidden:
        continue

      _editor = TreeEditWidget(
        manager = self._manager,
        widget_stack = self._widget_stack,
        tree_node_map = tree_node_map,
        schema = v,
        state = self.state[k],
        readonly = self.readonly,
        get_eval_names = self.get_eval_names )

      _editor.state_changed.connect(
        functools.partial(
          self.on_state_changed,
          k ) )

      self._struct_editors[k] = _editor

      self.tabs.addTab( _editor, k )

    self.tabs.currentChanged.connect( self.on_current_tab_change )

  #-----------------------------------------------------------------------------
  def merge( self ):
    for k, v in self._struct_editors.items():
      with blocked( v ):
        v.state = self.state[k]

    super().merge()

  #-----------------------------------------------------------------------------
  def commit( self ):
    for k, v in self._struct_editors.items():
      v.commit()

    super().commit()

  #-----------------------------------------------------------------------------
  # @classmethod
  # def guess( cls, filename ):
  #   schema = cls.default_schema.schema
  #
  #   if not osp.exists(filename):
  #     return 0.0
  #
  #   similarity = 0.0
  #
  #   try:
  #
  #     lines = (
  #       head(
  #         path = filename,
  #         n = 10 )
  #       + tail(
  #         path = filename,
  #         n = 10 ) )
  #
  #     type_pattern = rf"^{schema.tag_key}[\t ]*\:[\t ]*{schema.tag}"
  #     type_pattern = re.compile(type_pattern)
  #
  #     hash_pattern = r"__schema_hash__[\t ]*\:[\t ]*[\'\"]?([a-zA-Z0-9\-\_]+)[\'\"]?"
  #     hash_pattern = re.compile(hash_pattern)
  #
  #
  #     for l in lines:
  #       if type_pattern.match( l ):
  #         similarity = max( similarity, 1.0 )
  #
  #       m = hash_pattern.match( l )
  #
  #       if m:
  #         if m.group(1) == schema.schema_hash:
  #           similarity = max( similarity, 10.0 )
  #
  #         elif cls.guess_strict:
  #           return 0.0
  #
  #   except:
  #     log.exception("Error while parsing guess", exc_info = True )
  #
  #   return similarity


  #-----------------------------------------------------------------------------
  def on_state_changed( self, key, state ):
    if self.state is None or state is None:
      return

    _state = copy( self.state )
    _state[key] = state
    self.push_state = _state


  #-----------------------------------------------------------------------------
  def on_current_tab_change( self, index ):
    for k, v in self._struct_editors.items():
      # ensure no editors remain open when the tab switches
      v.close_editors()

  #-----------------------------------------------------------------------------
  def get_eval_names( self, context = None ):
    return dict()
