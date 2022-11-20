#!/usr/bin/python3
# -*- coding: utf-8 -*-
'''
This script uses the pyenliven.compatiblizemod submodule to try to make
the mod
'''
from __future__ import print_function
import re
import sys
import os

from find_pyenliven import pyenliven

from pyenliven.compatiblizemod import main

if __name__ == '__main__':
    # sys.argv[0] = re.sub(r'(-script\.pyw|\.exe)?$', '', sys.argv[0])
    sys.exit(main())
