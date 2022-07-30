#!/usr/bin/python3
# -*- coding: utf-8 -*-
'''
This script uses the pyenliven.compatiblizemod submodule to try to make
the mod
'''
import re
import sys
import os

UTILITIES_DIR = os.path.dirname(os.path.realpath(__file__))
REPO_DIR = os.path.dirname(UTILITIES_DIR)
# try:
#     from pyenliven.compatiblizemod import main
# except ModuleNotFoundError:
if os.path.isfile(os.path.join(REPO_DIR, "pyenliven", "__init__.py")):
    sys.path.append(REPO_DIR)

from pyenliven.compatiblizemod import main

if __name__ == '__main__':
    # sys.argv[0] = re.sub(r'(-script\.pyw|\.exe)?$', '', sys.argv[0])
    sys.exit(main())
