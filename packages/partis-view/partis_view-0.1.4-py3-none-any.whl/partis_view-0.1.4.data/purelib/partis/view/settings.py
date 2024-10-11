# -*- coding: UTF-8 -*-

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
from PySide2 import QtCore, QtGui, QtWidgets

from partis.schema import (
  PresetValue,
  required,
  optional,
  derived,
  is_sequence,
  is_mapping,
  is_evaluated,
  is_valued,
  is_valued_type,
  is_optional,
  PJCEvaluated,
  BoolPrim,
  IntPrim,
  FloatPrim,
  StrPrim,
  SeqPrim,
  MapPrim,
  UnionPrim,
  PassPrim,
  StructValued,
  MapValued,
  SchemaError,
  SeqValued,
  schema_declared,
  SchemaModule )

from partis.schema.color import (
  Color )

from partis.view.base import (
  WidgetStack,
  AsyncTarget )


from partis.view.schema import (
  TreeEditWidget,
  TreeEditNodeMap )

from partis.view.edit import (
  SchemaStructTreeFileEditor )

TEXT_PRESETS = [
  PresetValue(
    label = "Roboto",
    val = {
      'narrative' : {
        'font': 'Roboto',
        'size': 10 },
      'syntactic' : {
        'font': 'Roboto Mono',
        'size': 10 } }) ]

COLOR_PRESETS = [
  PresetValue(
    label = "Light",
    val = {
      # static areas (frame, panel...)
      'static': {
        'fore': '#31363B',
        'back': '#EFF0F1',
        'edge': '#BAB9B8',
        'fore_alt': '#31363B',
        'back_alt': '#dee2e7',
        'edge_alt': '#787876' },
      # dynamic areas (scroll, table, list...)
      'dynamic': {
        'fore': '#31363B',
        'back': '#FCFCFC',
        'edge': '#BAB9B8',
        'fore_alt': '#31363B',
        'back_alt': '#f5f5f5',
        'edge_alt': '#BAB9B8' },
      # hover, select, click, toggle
      'active': {
        'fore': '#27323d',
        'back': '#d3e7f2',
        'edge': '#3dade8',
        'fore_alt': '#27323d',
        'back_alt': '#d3e7f2',
        'edge_alt': '#3dade8' },
      # handles, buttons, input field, combo-box...
      'control': {
        'fore': '#484f57',
        'back': '#d2d5d9',
        'edge': '#6A6969',
        'fore_alt': '#31363B',
        'back_alt': '#FCFCFC',
        'edge_alt': '#BAB9B8' },

      'gray': {
        'low': '#1c1d1f',
        'mid': '#3b3d41',
        'high': '#5c626c' },
      'red': {
        'low': '#5c140f',
        'mid': '#791e25',
        'high': '#dd4f4f' },
      'orange': {
        'low': '#ac5f14',
        'mid': '#a27106',
        'high': '#a27106' },
      'yellow': {
        'low': '#a27106',
        'mid': '#a27106',
        'high': '#a27106' },
      'green': {
        'low': '#39601f',
        'mid': '#39601f',
        'high': '#39601f' },
      'cyan': {
        'low': '#005d69',
        'mid': '#246c75',
        'high': '#246c75' },
      'blue': {
        'low': '#005298',
        'mid': '#005298',
        'high': '#005298' },
      'magenta': {
        'low': '#691982',
        'mid': '#691982',
        'high': '#691982' } }),
  PresetValue(
    label = "Dark",
    val = {
      # static areas (frame, panel...)
      'static': {
        'fore': '#eff0f1',
        'back': '#31363b',
        'edge': '#76797c',
        'fore_alt': '#eff0f1',
        'back_alt': '#3b4045',
        'edge_alt': '#76797c' },
      # dynamic areas (scroll, table, list...)
      'dynamic': {
        'fore': '#eff0f1',
        'back': '#282c2f',
        'edge': '#32383c',
        'fore_alt': '#9b9fa2',
        'back_alt': '#1f1f1f',
        'edge_alt': '#33393e' },
      # hover, select, click, toggle
      'active': {
        'fore': '#eff0f1',
        'back': '#31363b',
        'edge': '#3daee9',
        'fore_alt': '#eff0f1',
        'back_alt': '#152e3c',
        'edge_alt': '#3daee9' },
      # handles, buttons, input field, combo-box...
      'control': {
        'fore': '#eff0f1',
        'back': '#232629',
        'edge': '#76797c',
        'fore_alt': '#eff0f1',
        'back_alt': '#232629',
        'edge_alt': '#76797c' },

      'gray': {
        'low': '#c9cdd1',
        'mid': '#9b9fa2',
        'high': '#757a7d' },
      'red': {
        'low': '#e06c75',
        'mid': '#be5046',
        'high': '#bd382c' },
      'orange': {
        'low': '#d19a66',
        'mid': '#e6c07b',
        'high': '#e8af47' },
      'yellow': {
        'low': '#d1c366',
        'mid': '#d0bd41',
        'high': '#d0b81c' },
      'green': {
        'low': '#98c379',
        'mid': '#82af61',
        'high': '#76b646' },
      'cyan': {
        'low': '#79bac2',
        'mid': '#56b6c2',
        'high': '#30a9b8' },
      'blue': {
        'low': '#61aeee',
        'mid': '#51a1e4',
        'high': '#3389d0' },
      'magenta': {
        'low': '#cc8fde',
        'mid': '#c678dd',
        'high': '#bc58da' } }) ]

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
class ColorContext( StructValued ):
  schema = dict(
    tag = 'color_ctx',
    default_val = derived )

  fore = Color(default_val = '#000000')
  fore_alt = Color(default_val = '#222222')

  back = Color(default_val = '#ffffff')
  back_alt = Color(default_val = '#eeeeee')

  edge = Color(default_val = '#aaaaaa')
  edge_alt = Color(default_val = '#bbbbbb')

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
class ColorRange( StructValued ):
  schema = dict(
    tag = 'color_rng',
    default_val = derived )

  low = Color(default_val = '#550000')
  mid = Color(default_val = '#aa0000')
  high = Color(default_val = '#ff0000')

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
class ColorTheme( StructValued ):
  schema = dict(
    tag = 'color_theme',
    default_val = COLOR_PRESETS[0].val,
    preset_vals = COLOR_PRESETS )

  static = ColorContext
  dynamic = ColorContext
  passive = ColorContext
  active = ColorContext
  control = ColorContext

  gray = ColorRange
  red = ColorRange
  orange = ColorRange
  yellow = ColorRange
  green = ColorRange
  cyan = ColorRange
  blue = ColorRange
  magenta = ColorRange

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
class TextContext( StructValued ):
  schema = dict(
    tag = 'text_ctx',
    default_val = derived )

  font = StrPrim(default_val = 'Ariel')
  size = IntPrim(
    min = 5,
    max = 25,
    default_val = 10 )

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
class TextTheme( StructValued ):
  schema = dict(
    tag = 'text_theme',
    default_val = TEXT_PRESETS[0].val,
    preset_vals = TEXT_PRESETS )

  narrative = TextContext
  syntactic = TextContext

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
class Theme( StructValued ):
  schema = dict(
    tag = 'theme',
    default_val = derived )

  text = TextTheme
  color = ColorTheme

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
class Settings( StructValued ):
  schema = dict(
    tag = 'settings',
    default_val = derived )

  theme = Theme

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
class SettingsEditor(SchemaStructTreeFileEditor):
  default_schema = Settings
  # State is not saved to a file (by default)
  default_fileonly = False

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# class ConfigDialog ( QtWidgets.QDialog ):
#   #-----------------------------------------------------------------------------
#   def __init__( self,
#     manager,
#     parent = None ):
#
#     super().__init__(parent)
#
#     self.setWindowIcon( QtGui.QIcon(manager.resource_path("images/icons/app_icon.png")) )
#     self.setAttribute( QtCore.Qt.WA_StyleSheet, True )
#     self.setAttribute( QtCore.Qt.WA_StyledBackground, True )
#     self.setStyleSheet( manager.stylesheet )
#
#     self.setWindowTitle("")
#
#     self._manager = manager
#
#     self._layout = QtWidgets.QVBoxLayout()
#
#     self.setLayout( self._layout )
#
#     self._widget_stack = WidgetStack(
#       manager = self._manager )
#
#     self._layout.addWidget( self._widget_stack )
#
#     self._config_tree = TreeEditWidget(
#       manager = self._manager,
#       widget_stack = self._widget_stack,
#       schema = Config )
#
#     self._widget_stack.push_widget( self._config_tree )
#
#     screen = QtGui.QGuiApplication.primaryScreen()
#     screenGeometry = screen.geometry()
#     height = screenGeometry.height()
#     width = screenGeometry.width()
#
#     self.resize( int( width / 2.0 ), int( height / 2.0 ) )
