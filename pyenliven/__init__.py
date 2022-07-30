#!/usr/bin/env python
'''
This module assists with building games from other games, mods, and
patches.
'''
from __future__ import print_function

import sys
import platform
import os

profile = None
if platform.system() == "Windows":
    profile = os.environ.get('USERPROFILE')
else:
    profile = os.environ.get('HOME')

verbosity = 0
max_verbosity = 2


def echo0(*args, **kwargs):
    print(*args, file=sys.stderr, **kwargs)


def echo1(*args, **kwargs):
    if verbosity < 1:
        return False
    print(*args, file=sys.stderr, **kwargs)
    return True


def echo2(*args, **kwargs):
    if verbosity < 2:
        return False
    print(*args, file=sys.stderr, **kwargs)
    return True


def get_verbosity():
    return verbosity


def set_verbosity(level):
    if level is True:
        verbosity = 1
    elif level is False:
        verbosity = 0
    elif level in range(max_verbosity+1):
        verbosity = level
    raise ValueError(
        "verbosity must be {} at maximum.".format(max_verbosity)
    )


try:
    import mtanalyze
except ModuleNotFoundError as ex:
    # tryMTA = os.path.join(profile, "git", "mtanalyze")
    moduleDir = os.path.dirname(os.path.realpath(__file__))
    REPO_DIR = os.path.dirname(moduleDir)
    modulesDir = os.path.dirname(REPO_DIR)
    echo0("* looking for mtanalyze in modulesDir \"{}\""
          "".format(modulesDir))
    tryMTA = os.path.abspath(os.path.join(modulesDir, "mtanalyze"))
    if os.path.isdir(tryMTA):
        sys.path.append(tryMTA)
        import mtanalyze
        # ^ import mtanalyze/mtanalyze purposely since the main
        #   mtanalyze/ directory is a setuptools package not a module.
    else:
        echo0("")
        echo0("You must install mtanalyze alongside")
        echo0("EnlivenMinetest such that ../mtanalize/mtanalize exists")
        echo0("such as via:")
        echo0("    git clone https://github.com/poikilos/mtanalyze {}"
              "".format(tryMTA))
        echo0("")
        # raise tryMTA
        exit(1)

# from mtanalyze import profile_path
MY_MODULE_DIR = os.path.dirname(os.path.realpath(__file__))
# ^ realpath follows symlinks
REPO_DIR = os.path.dirname(MY_MODULE_DIR)
MODS_STOPGAP_DIR = os.path.join(REPO_DIR, "patches", "mods-stopgap")
if not os.path.isdir(MODS_STOPGAP_DIR):
    echo0("Error: \"{}\" is missing.".format(MODS_STOPGAP_DIR))
    exit(1)
BASE_DIR = os.path.join(REPO_DIR, "Bucket_Game-base")
if not os.path.isdir(BASE_DIR):
    echo0("Error: \"{}\" is missing.".format(BASE_DIR))
    exit(1)
BRANCHES_DIR = os.path.join(REPO_DIR, "Bucket_Game-branches")
if not os.path.isdir(BRANCHES_DIR):
    echo0("Error: \"{}\" is missing.".format(BRANCHES_DIR))
    exit(1)

# NOTE: get a git repo's origin via: git remote show origin


def getSGPath(stopgap_mod_name):
    return os.path.join(MODS_STOPGAP_DIR, stopgap_mod_name)
