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

# see <https://stackoverflow.com/questions/5574702/how-to-print-to-stderr-in-python>
def error(*args, **kwargs):
    print(*args, file=sys.stderr, **kwargs)

try:
    import mtanalyze
except ModuleNotFoundError as ex:
    # tryMTA = os.path.join(profile, "git", "mtanalyze")
    tryMTA = os.path.abspath(os.path.join("..", "mtanalyze"))
    if os.path.isdir(tryMTA):
        sys.path.append(tryMTA)
        import mtanalyze
    else:
        error("")
        error("You must install mtanalyze alongside")
        error("EnlivenMinetest such that ../mtanalize/mtanalize exists")
        error("such as via:")
        error("    git clone https://github.com/poikilos/mtanalyze {}"
              "".format(tryMTA))
        error("")
        # raise tryMTA
        exit(1)

# from mtanalyze import profile_path

gamespec = {}
gamespec['remove_mods'] = [
    "coderblocks",  # includes lmb blocks; no recipes
    "facade", # no recipes
    "placecraft", # interferes with eating
    "more_chests", # See https://github.com/poikilos/EnlivenMinetest/issues/446
    "emeralds", # See https://github.com/poikilos/EnlivenMinetest/issues/497
    "give_initial_stuff",  # or make it configurable (It only uses a give_initial_stuff boolean, no configurable item list)
]
myDir = os.path.dirname(os.path.abspath(__file__))
mods_stopgap = os.path.join(myDir, "patches", "mods-stopgap")
if not os.path.isdir(mods_stopgap):
    error("Error: \"{}\" is missing.".format(mods_stopgap))
    exit(1)
gamespec['local_mods_paths'] = []
gamespec['local_mods_paths'].append(mods_stopgap)
# NOTE: get a git repo's origin via: git remote show origin

def getSGPath(stopgap_mod_name):
    return os.path.join(mods_stopgap, stopgap_mod_name)

gamespec['add_mods'] = [
    # {'repo':"https://github.com/poikilos/homedecor_ua"},
    {'src_path': getSGPath("animal_materials_legacy")},
    {'repo':"https://github.com/minetest-mods/ccompass.git"},
    {'repo':"https://github.com/octacian/chat3.git"},
    {'repo':"https://github.com/poikilos/compassgps.git"},
    {'src_path': getSGPath("elk_legacy")},
    {'repo':"https://github.com/MinetestForFun/fishing.git"},
    {'src_path': getSGPath("glooptest_missing")},
    {'repo':"https://github.com/minetest-mods/item_drop.git"},
    {'repo':"https://github.com/poikilos/metatools.git"},
    {'src_path': getSGPath("nftools_legacy")},
    {'src_path': getSGPath("glooptest_missing")},
    {'repo':"https://github.com/poikilos/slimenodes.git"},
    {'repo':"https://github.com/BenjieFiftysix/sponge.git"},
    {'repo':"https://github.com/poikilos/throwing.git"},  # Can utilize toolranks, toolranks_extras, wielded_light
    {'repo':"https://github.com/poikilos/throwing_arrows.git"},  # Can utilize mesecons, mesecons_button
    {'repo':"https://gitlab.com/VanessaE/biome_lib.git"},
    {
        'repo': "https://github.com/Poikilos/vines.git",
        'branch': "Bucket_Game", # git clone <url> --branch <branch>
    },
    {"https://github.com/MinetestForFun/unified_inventory"},
]

'''
# Items with no URL below are from EnlivenMinetest
# - [x] Ensure everything is in gamespec['add_mods']
minimum_live_server_based_on_bucket_game_200527 = [
    {'name': 'animal_materials_legacy'},
    {'name': 'ccompass', 'repo': "https://github.com/minetest-mods/ccompass"},  # Remove this one or point to world-specific spawn area via settings? It is a regular spawn-pointing compass by default
    {'name': 'chat3', 'repo': "https://github.com/octacian/chat3"},  # Doesn't seem to have any effect
    {'name': 'compassgps', 'repo': "https://github.com/poikilos/compassgps"},
    {'name': 'elk_legacy'},
    {'name': 'fishing', 'repo': "https://github.com/MinetestForFun/fishing"},
    {'name': 'glooptest_missing'},
    # {'name': 'ircpack', 'repo': ""},  # ONLY for servers!
    # {'name': 'item_drop', 'repo': ""},  # In bucket_game now (but see mt_conf_by_mod['item_drop'] for settings)
    {'name': 'metatools', 'repo': "https://github.com/poikilos/metatools"},
    {'name': 'nftools_legacy'},
    {'name': 'slimenodes', 'repo': "https://github.com/poikilos/slimenodes"},
    {'name': 'sponge', 'repo': "https://github.com/BenjieFiftysix/sponge"},  # In bucket_game but only in coderblocks
    {'name': 'throwing', 'repo': "https://github.com/poikilos/throwing"},
    {'name': 'throwing_arrows', 'repo': "https://github.com/poikilos/throwing_arrows"},
]
'''

'''
Remove server_only_mods from the client and packaged copies of
ENLIVEN.
'''
server_only_mods = [
    'ircpack',
    'chat3',
]

'''
mt_conf_by_mod settings should be placed in minetest.conf such as
/opt/minebest/mtworlds/center/ENLIVEN/minetest.conf
but for now just use
- patches/subgame/minetest.conf
  To define the game.
  If minebest is present, combine minetest.conf and
  minetest.server-example.conf
  but maybe make an alternate version with stuff that isn't in
  world.conf.
  For other conf settings:
- patches/subgame/minetest.server-example.conf goes in the server only.
  - Place the result in the game directory such as will result in
    /opt/minebest/mtworlds/center/ENLIVEN/minetest.conf
- patches/subgame/minetest.client-example.conf goes in clients only.
'''
mt_conf_by_mod = {
    'item_drop': {
        'item_drop.pickup_radius': "1.425",
    }
    'throwing_arrows': {
        'throwing.enable_arrow', "true",
    }
}

why = {}
why_not["https://github.com/FaceDeer/vines.git"] = '''
'''
why["https://github.com/MinetestForFun/unified_inventory"] = '''
This fork makes a "nicer interface". The fork hasn't been tested yet.
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
    raise NotImplementedError("pyenliven build")

if __name__ == "__main__":
    main()
