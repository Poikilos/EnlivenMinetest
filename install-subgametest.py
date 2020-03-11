#!/usr/bin/env python

import os
import shutil
import sys
from forwardfilesync import *

# region options
force_update_mtg_enable = False  # first delete subgametest then remake
# endregion options

try:
    input = raw_input
except NameError:
    pass

gitpython_msg = """
You do not have gitpython installed.
Please run the following commands in terminal
For installing Python in Windows, the most usable option
 is CUSTOM install, then change System Path to
   'install to hard drive'
 (otherwise first cd C:\\Python27 [or your Python folder],
 but if in *nix-like environment first 'su -', and if no
 pip, use your software manager to install:
   python-pip or python2-pip or python3-pip)
sudo python3 -m pip install --upgrade pip
sudo python3 -m pip install --upgrade pip wheel
sudo python3 -m pip install gitpython
# Possible commands:
# sudo pkg install -y python3-pip python2-pip
# sudo apt install -y python3-pip python2-pip
# sudo pacman -Syuu python2-pip python-pip
# #("Passing two --refresh or -y flags forces pacman to refresh
# #all package lists even if they are considered to be up to
# #date.")

"""

try:
    from git import Repo
except ImportError:
    print(gitpython_msg)
    print("")
    input("press enter to close...")
    exit(1)

profile_path = None
if 'HOME' in os.environ:  # if os.name=="windows":
    profile_path = os.environ['HOME']
else:
    profile_path = os.environ['USERPROFILE']


if not os.path.isdir(profile_path):
    print("")
    print("Failed to get existing home path--tried HOME & USERPROFILE")
    print("")
    input("press enter to close")
    exit(2)

configs_path = os.path.join(profile_path, ".config")
if os.name == "windows":
    base_path = os.path.join(profile_path, "AppData")
    configs_path = os.path.join(base_path, "Local")

CONFIG_PATH = os.path.join(configs_path, "EnlivenMinetest")
if not os.path.isdir(CONFIG_PATH):
    os.makedirs(CONFIG_PATH)

# NOTE: not using /var/cache
caches_path = os.path.join(CONFIG_PATH, "cache")
RELEASES_PATH = os.path.join(caches_path, "releases")
GIT_REPOS_PATH = os.path.join(caches_path, "git")
GIT_BRANCHES_PATH = os.path.join(caches_path, "git-branches")

if not os.path.isdir(RELEASES_PATH):
    os.makedirs(RELEASES_PATH)

if not os.path.isdir(GIT_REPOS_PATH):
    os.makedirs(GIT_REPOS_PATH)

if not os.path.isdir(GIT_BRANCHES_PATH):
    os.makedirs(GIT_BRANCHES_PATH)

USR_SHARE_MINETEST = "/usr/share/games/minetest"
if not os.path.isdir(USR_SHARE_MINETEST):
    if os.path.isdir("/usr/local/share/minetest"):
        # IF git version is installed:
        USR_SHARE_MINETEST = "/usr/local/share/minetest"
    if os.path.isdir("/usr/share/minetest"):
        USR_SHARE_MINETEST = "/usr/share/minetest"

    if not os.path.isdir(USR_SHARE_MINETEST):
        print("Minetest could not be found in any known location."
              " Try installing minetest or compiling from source or"
              " editing value of USR_SHARE_MINETEST in this script."
              " The script ended early.")
        input("press enter to close...")
        exit(3)


MT_GAMES_DIR = os.path.join(USR_SHARE_MINETEST, "games")
MT_MYGAME_NAME = "subgametest"
MT_MYGAME_DIR = os.path.join(MT_GAMES_DIR, MT_MYGAME_NAME)

mtg_game_name = "minetest_game"
MTG_PATH = os.path.join(MT_GAMES_DIR, mtg_game_name)
folder_path = MTG_PATH
MTG_MODS_PATH = os.path.join(MTG_PATH, "mods")

if not os.path.isdir(folder_path):
    print("Could not find \"" + folder_path + "\". Script ended early.")
    input("press enter to close...")
    exit(4)

if force_update_mtg_enable:
    shutil.rmtree(MT_MYGAME_DIR)

# yes | cp -rf $MT_GAMES_DIR/minetest_game/* MT_MYGAME_DIR"
# sudo rsync -a $MT_GAMES_DIR/minetest_game/* MT_MYGAME_DIR"

try:
    # DOES update minetest_game, but does NOT delete extra mods:
    update_tree(folder_path, MT_MYGAME_DIR)
    print("Updated \"" + MT_MYGAME_DIR + "\"...")
except PermissionError:
    print(str(sys.exc_info()))
    print("")
    print("You must run " + __file__ + " as a user that can write to "
          "\"" + MT_MYGAME_DIR + "\"")
    print("")
    input("press enter to close...")
    exit(5)

try:
    # cd $HOME
    # tmp_game_conf_path = os.path.join(profile_path, "game.conf")
    outs = open(os.path.join(MT_MYGAME_DIR, "game.conf"), 'w')
    outs.write("name = subgametest")
    outs.close()
except PermissionError:
    print(str(sys.exc_info()))
    print("")
    print("You must run " + __file__ + " as a user that can write to "
          "\"" + MT_MYGAME_DIR + "\"")
    print("")
    input("press enter to close...")
    exit(6)
# cmd_string = "sudo mv -f game.conf \MT_MYGAME_DIR\""
# shutil.move(tmp_game_conf_path, os.path.join(MT_MYGAME_DIR, "game.conf"))

if os.path.isdir(os.path.join(MT_MYGAME_DIR, "mods")):
    print("Copied subgame to " + MT_MYGAME_DIR)
else:
    print("FAILED to copy subgame to " + MT_MYGAME_DIR)
    input("press enter to close...")
    exit(7)


MT_MYGAME_MODS_PATH = os.path.join(MT_MYGAME_DIR, "mods")
MTMOD_DEST_NAME = "minigamer"
MTMOD_DEST_PATH = os.path.join(MT_MYGAME_MODS_PATH, MTMOD_DEST_NAME)

# if force_update_mtg_mods_enable:
#     for sub_name in os.listdir(folder_path):
#         sub_path = os.path.join(folder_path, sub_name)
#         dst_path = os.path.join(MT_MYGAME_DIR, sub_name)
#         if sub_name[:1]!="." and os.path.isdir(sub_path):
#             if os.path.isdir(dst_path):
#                 shutil.rmtree(dst_path)


if not os.path.isdir(GIT_REPOS_PATH):
    print("Cannot create " + GIT_REPOS_PATH + " so cannot continue.")
    input("press enter to close...")
    exit(8)

# TODO: actually install something (from spreadsheet maybe)

mtg_mods_list = list()
folder_path = MTG_MODS_PATH
if os.path.isdir(folder_path):
    for sub_name in os.listdir(folder_path):
        sub_path = os.path.join(folder_path, sub_name)
        if sub_name[:1] != "." and os.path.isdir(sub_path):
            mtg_mods_list.append(sub_name)

mods_installed_list = list()
mods_added_list = list()

folder_path = MT_MYGAME_MODS_PATH
if os.path.isdir(folder_path):
    for sub_name in os.listdir(folder_path):
        sub_path = os.path.join(folder_path, sub_name)
        if sub_name[:1] != "." and os.path.isdir(sub_path):
            mods_installed_list.append(sub_name)
            if sub_name not in mtg_mods_list:
                mods_added_list.append(sub_name)
else:
    print("Missing '" + folder_path + "'")

print("")
print("")
print("Installed " + str(len(mods_installed_list)) + " mod(s)" +
      " (" + str(len(mtg_mods_list)) + " from " + mtg_game_name + ").")
if len(mods_added_list) > 0:
    print("Added:")
    for mod_name in mods_added_list:
        print("  - " + mod_name)
print("")
input("press enter to close...")
# cd $TMP_DIR
# git clone https://github.com/tenplus1/mobs_redo.git
# git clone https://github.com/tenplus1/mobs_animal.git
# git clone https://github.com/tenplus1/mobs_monster.git
# git clone https://github.com/tenplus1/mobs_npc.git
# but not:
# git clone https://github.com/poikilos/minetest-minigamer.git
# git clone https://github.com/poikilos/birthstones.git

# Repo.clone_from(git_url, repo_dir)
