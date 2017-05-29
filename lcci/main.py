#!/usr/bin/env python

import argparse
from lcci import __version__

def main():
     parser = argparse.ArgumentParser()

     parser.add_argument('--version', help='Display the FuseSoC version', action='version', version=__version__)

     parsed_args = parser.parse_args()
     if hasattr(parsed_args, 'func'):
         run(parsed_args)
     else:
         parser.print_help()

if __name__ == "__main__":
    main()
