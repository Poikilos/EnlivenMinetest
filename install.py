#!/usr/bin/env python
from __future__ import print_function

import sys
import platform
import os

profile = None
if platform.system() == "Windows":
    profile = os.environ.get('USERPROFILE')
else:
    profile = os.environ.get('HOME')

def error(msg):
    sys.stderr.write("{}\n".format(msg))
    sys.stderr.flush()

try:
    import mtanalyze
except ModuleNotFoundError as ex:
    tryMTA = os.path.join(profile, "git", "mtanalyze")
    if os.path.isdir(tryMTA):
        sys.path.append(tryMTA)
        import mtanalyze
    else:
        error("")
        error("You must install mtanalyze in the directory alongside")
        error("EnlivenMinetest or as ~/git/mtanalize")
        error("such as via:")
        error("git clone https://github.com/poikilos/mtanalyze ~/git/mtanalize")
        error("")
        # raise tryMTA
        exit(1)
print("This doesn't work (not yet implemented). See build.py.")
