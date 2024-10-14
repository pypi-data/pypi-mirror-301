#!/usr/bin/env python3
import argparse
from argparse import RawDescriptionHelpFormatter
from argparse import RawTextHelpFormatter

from g4l.cli_common.app_version import *
from g4l.cli_common.cfg import *

def main():
    parser = argparse.ArgumentParser(
            prog='g4l', 
            description='Generic Minimal Launcher',
            epilog='',
            formatter_class=RawTextHelpFormatter)

    version_psr = parser.add_argument(
            '--version', 
            help='show the cli version', 
            action='version', 
            version=get_app_version())

    parser.add_argument(
        '--verbose',
        action='store_true',
        help='request verbose output')

    sps = parser.add_subparsers(required=True, help='sub-command help')

    cfg = load_cfg('g4l')



    if os.environ.get('GML_GEN_DOCS', '0') == '1':
        generate_argparse_docs(parser)

    args = parser.parse_args()
    args.func(args)


if __name__ == '__main__':
    main()