#!/usr/bin/env python
'''
This script is a remake of the ENLIVEN build script in Python using
Bucket_Game as the basis.
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
print("This doesn't work (not yet implemented)")

# from mtanalyze import profile_path

gamespec = {}
gamespec['remove_mods'] = [
    "coderblocks",  # includes lmb blocks; no recipes
    "facade", # no recipes
    "placecraft", # interferes with eating
    "more_chests", # See https://github.com/poikilos/EnlivenMinetest/issues/446
]
myDir = os.path.dirname(__file__)
mods_stopgap = os.path.join(myDir, "patches", "mods-stopgap")
if not os.path.isdir(mods_stopgap):
    error("Error: \"{}\" is missing.".format(mods_stopgap))
    exit(1)
gamespec['local_mods_paths'] = []
gamespec['local_mods_paths'].append(mods_stopgap)
# NOTE: get a git repo's origin via: git remote show origin
gamespec['add_mods'] = [
    # "https://github.com/poikilos/homedecor_ua",
    "animal_materials_legacy",
    "https://github.com/minetest-mods/ccompass.git",
    "https://github.com/octacian/chat3.git",
    "https://github.com/poikilos/compassgps.git",
    "elk_legacy",
    "https://github.com/MinetestForFun/fishing.git",
    "glooptest_missing",
    "https://github.com/minetest-mods/item_drop.git",
    "https://github.com/poikilos/metatools.git",
    "nftools_legacy",
    "https://github.com/poikilos/slimenodes.git",
    "https://github.com/BenjieFiftysix/sponge.git",
    "https://github.com/minetest-mods/throwing.git",
    "https://github.com/minetest-mods/throwing_arrows.git",
]
gamespec['disable_mobs'] = [
    "old_lady",
]

warnings = '''
WARNINGS:
(Bucket_Game 200527)
- The "rope" required for making a fishing rod has no recipe!
  See <https://github.com/poikilos/EnlivenMinetest/issues/444>
'''


def main():
    pass
    print(warnings)

if __name__ == "__main__":
    main()
