# -*- coding: UTF-8 -*-

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
from PySide2 import QtCore, QtGui, QtWidgets

from pygments import (
  lexers )

from partis.view.base import (
  Heading1,
  Heading2,
  Heading3,
  HLine,
  ToolButton,
  blocked )

from partis.view.edit import TextFileEditor

from .code import CodeEdit

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
class PlainTextEditor ( TextFileEditor ):

  #-----------------------------------------------------------------------------
  def __init__( self,
    manager,
    widget_stack,
    filename = None,
    state = None,
    readonly = None ):

    if state is None:
      state = ""

    super().__init__(
      manager = manager,
      widget_stack = widget_stack,
      filename = filename,
      state = state,
      readonly = readonly )

  #-----------------------------------------------------------------------------
  def build( self ):

    self._layout = QtWidgets.QVBoxLayout( self )
    self.setLayout(self._layout)

    self._layout.setContentsMargins(0,0,0,0)
    self._layout.setSpacing(0)

    self._lang = QtWidgets.QComboBox()

    self._lang.addItem( "None", userData = None )

    self._lexer_names = [ l[1][0]
      for l in lexers.get_all_lexers()
      if len(l) > 1 and len(l[1]) > 0 ]

    for lexer in self._lexer_names:
      self._lang.addItem( lexer, userData = lexer )

    self._lang.currentIndexChanged.connect( self.on_lang_changed )

    self._layout.addWidget( self._lang )

    self._multiline = CodeEdit(
      manager = self._manager )

    self._multiline.code.setReadOnly(self.readonly)

    self._multiline.code.textChanged.connect( self.on_finished_multiline )

    self._layout.addWidget( self._multiline )

    if self.filename is not None:

      try:
        lexer = lexers.guess_lexer_for_filename(self.filename, self.state)

        self.set_lang( lexer.aliases[0] )
      except:
        pass

  #-----------------------------------------------------------------------------
  def merge( self ):

    with blocked( self._multiline.code ):
      self._multiline.code.setPlainText( self.state )

    super().merge()

  #-----------------------------------------------------------------------------
  def commit(self):
    self.push_state = self._multiline.code.toPlainText()

  #-----------------------------------------------------------------------------
  def set_lang( self, lang ):

    with blocked( self._lang ):
      index = self._lang.findData( lang )
      self._lang.setCurrentIndex( index )


    self._multiline.code.set_lang( lang )

  #-----------------------------------------------------------------------------
  def on_lang_changed( self, index ):
    self.set_lang( self._lang.currentData() )

  #-----------------------------------------------------------------------------
  def on_finished_multiline( self ):
    self.commit()

  #-----------------------------------------------------------------------------
  async def test_plaintext_editor( self ):
    self._multiline.code.setPlainText(test_text)

    self._lang.setCurrentIndex( 10 % len(self._lexer_names) )

    self.save()

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
test_text = """
some dummy text
"""
