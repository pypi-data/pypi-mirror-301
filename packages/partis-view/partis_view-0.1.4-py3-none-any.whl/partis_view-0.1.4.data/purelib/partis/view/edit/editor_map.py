# -*- coding: UTF-8 -*-

import os

try:
  from importlib.metadata import distributions

except ImportError:
  from importlib_metadata import distributions

from partis.utils import getLogger
log = getLogger(__name__)

from partis.utils.plugin import (
  plugin_manager )

from .text import (
  PlainTextEditor )

from .h5_editor import(
  H5TreeFileEditor)

from .schema_editor import (
  SchemaTreeFileEditor )

from partis.schema.plugin import (
  SchemaPluginGroup )

from partis.schema.hint import HintList

from .plugin import (
  EditorPluginGroup,
  SchemaEditNodePlugin )

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
class LogFileEditor( SchemaTreeFileEditor ):
  default_schema = HintList
  default_readonly = True

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
class EditorMap:

  #-----------------------------------------------------------------------------
  @property
  def editors( self ):

    editors = {
      "HDF5" : H5TreeFileEditor,
      "Plain Text" : PlainTextEditor,
      "YAML" : SchemaTreeFileEditor,
      "Log + YAML" : LogFileEditor }

    editor_schemas = set()

    for plugin in plugin_manager.plugins( EditorPluginGroup ):
      pkg = f"{plugin.package}"
      pkg_editors = editors.setdefault( pkg, dict() )

      if plugin.label:
        group_editors = pkg_editors.setdefault( plugin.label, dict() )
      else:
        # root level group
        group_editors = pkg_editors

      for k, v in plugin.editors.items():

        group_editors[k] = v

        editor_schemas.add( v.default_schema.schema )

    for plugin in plugin_manager.plugins( SchemaPluginGroup ):

      group_editors = dict()

      for k, v in plugin.schemas.items():
        if v not in editor_schemas:
          group_editors[k] = SchemaTreeFileEditor.specialize_schema(v)

      if group_editors:
        pkg = f"{plugin.package}"
        pkg_editors = editors.setdefault( pkg, dict() )

        if plugin.label:
          pkg_editors[plugin.label] = group_editors
        else:
          # root level group
          pkg_editors.update(group_editors)

    return editors

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
editor_map = EditorMap()
