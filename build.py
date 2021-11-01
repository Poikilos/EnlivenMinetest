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
    "https://gitlab.com/VanessaE/biome_lib.git",
    {
        'url': "https://github.com/Poikilos/vines.git",
        'branch': "Bucket_Game", # git clone <url> --branch <branch>
    },
]
why = {}
why_not["https://github.com/FaceDeer/vines.git"] = '''
'''
why["https://github.com/poikilos/vines.git"] = '''
This Poikilos fork (The Bucket_Game branch) adds support for Bucket_Game
jungle node names which are in a standard naming format (like other
trees are).

> I've finally done it, I've split this mod in twain. The new
> stand-alone ropes mod has no dependency on biome_lib and no vine
> content, though its crafting recipes remain compatible with the vines
> produced by this mod.
>
> My fork of this vines mod has had the rope-related content removed
> from it, leaving it as just a vines mod. Note that I haven't tested
> it extensively - I have to admit, I've mainly been in this for the
> ropes. :) I'll do what I can to maintain it, though, if anyone has
> bug reports or requests.
>
> I've added a node upgrade function to the new ropes mod that will
> convert the ropes from both my fork of the vines mod and the original
> version of the vines mod by bas080 to the new ropes mod's ropes. So
> if you wish to upgrade an existing world it should work.

- FaceDeer on [[Mod] Vines and Rope [2.3] [vines]]
  (https://forums.minetest.org/viewtopic.php?f=11&t=2344&start=50
  &sid=bf15c996963e891cd3f2460c2525044a)

Note that vines requires:

default
biome_lib
moretrees?
doc?
intllib?
mobs?
creatures?
'''
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
