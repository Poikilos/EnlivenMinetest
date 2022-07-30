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


def echo0(*args, **kwargs):
    print(*args, file=sys.stderr, **kwargs)


try:
    import mtanalyze
except ModuleNotFoundError as ex:
    tryMTA = os.path.join(profile, "git", "mtanalyze")
    if os.path.isdir(tryMTA):
        sys.path.append(tryMTA)
        import mtanalyze
    else:
        echo0("")
        echo0("You must install mtanalyze in the directory alongside")
        echo0("EnlivenMinetest or as ~/git/mtanalize")
        echo0("such as via:")
        echo0("git clone https://github.com/poikilos/mtanalyze ~/git/mtanalize")
        echo0("")
        # raise tryMTA
        sys.exit(1)


def main():
    echo0("This doesn't work (not yet implemented). See build.py.")
    return 1


if __name__ == "__main__":
    sys.exit(main())
