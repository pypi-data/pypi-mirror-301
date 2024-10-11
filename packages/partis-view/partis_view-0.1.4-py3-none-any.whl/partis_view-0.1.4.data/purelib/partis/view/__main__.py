# import faulthandler
# faulthandler.enable()

import subprocess
import sys
import argparse
from argparse import RawTextHelpFormatter
import logging

log = logging.getLogger(__name__)

from partis.utils import (
  logging_parser_add, 
  logging_parser_init )

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++#

def argument_parser( ):

  """Parse for commandline arguments.
  """

  parser = argparse.ArgumentParser(
    description = __doc__,
    formatter_class = RawTextHelpFormatter )

  parser.add_argument( "-t", "--theme",
    type = str,
    default = 'light',
    help = "gui theme { 'light', 'dark' }." )

  parser.add_argument( "-i", "--init",
    type = str,
    default = "",
    help = "Initialization file" )

  parser.add_argument('init',
    type = str,
    default = None,
    nargs='?',
    help = "File or directory to open initially" )

  logging_parser_add(parser)

  return parser


#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++#

def main():

  parser = argument_parser( )
  args = parser.parse_args( )

  logging_parser_init(args)

  from partis.view import (
    MainWindow,
    Manager )

  app_manager = Manager(
    main_window_class = MainWindow,
    theme = args.theme,
    init_file = args.init )

  return app_manager.run()

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++#
if __name__ == "__main__":
  exit( main() )
