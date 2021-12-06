#!/usr/bin/python3
# -*- coding: utf-8 -*-
'''
This script uses the pyenliven.compatiblizemod submodule to try to make
the mod
'''
import re
import sys
import os

myDir = os.path.dirname(os.path.realpath(__file__))
repoDir = os.path.dirname(myDir)
# try:
#     from pyenliven.compatiblizemod import main
# except ModuleNotFoundError:
if os.path.isdir(os.path.join(repoDir, "pyenliven")):
    sys.path.append(repoDir)

from pyenliven.compatiblizemod import main

if __name__ == '__main__':
    # sys.argv[0] = re.sub(r'(-script\.pyw|\.exe)?$', '', sys.argv[0])
    sys.exit(main())
