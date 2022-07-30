#!/usr/bin/env python

import os
import shutil
import sys
from forwardfilesync import *

# region options
force_update_mtg_enable = False  # first delete subgametest then remake
# endregion options

'''
if sys.version_info.major >= 3:
    pass
else:
    input = raw_input
'''

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
    sys.exit(1)

from pyenliven import (
    echo0,
)
from mtanalyze import(
    TRY_SHARE_MT_DIRS,
    get_var_and_check,
)


profile_path = None
if 'HOME' in os.environ:
    profile_path = os.environ['HOME']
else:  # if platform.system() == "Windows"
    profile_path = os.environ['USERPROFILE']


def main():
    if not os.path.isdir(profile_path):
        echo0("")
        echo0("Failed to get existing home path--tried HOME & USERPROFILE")
        echo0("")
        return 2

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

    '''
    USR_SHARE_MINETEST = None
    for try_share_mt in TRY_SHARE_MT_DIRS:
        if os.path.isdir(try_share_mt):
            USR_SHARE_MINETEST = try_share_mt
            break
    if USR_SHARE_MINETEST is None:
        echo0("Minetest could not be found in any known location ({})."
              " Try installing minetest or compiling from source or"
              " editing value of USR_SHARE_MINETEST in this script."
              " The script ended early.".format(TRY_SHARE_MT_DIRS))
        return 3
    '''
    USR_SHARE_MINETEST, code = get_var_and_check('shared_minetest_path', 3)
    if code != 0:
        return code

    MT_GAMES_DIR = os.path.join(USR_SHARE_MINETEST, "games")
    MT_MYGAME_NAME = "subgametest"
    MT_MYGAME_DIR = os.path.join(MT_GAMES_DIR, MT_MYGAME_NAME)

    MTG_PATH = None
    mtg_game_name = None
    base_game_path = None
    base_games = ["amhi_game", "minetest_game"]
    for try_game_name in base_games:
        MTG_PATH = os.path.join(MT_GAMES_DIR, try_game_name)
        base_game_path = MTG_PATH
        if os.path.isdir(base_game_path):
            mtg_game_name = try_game_name

    if mtg_game_name is None:
        echo0("Could not find \"" + base_game_path + "\". Script ended early.")
        echo0("Set shared_minetest_path to the path containing a")
        echo0(" games folder with one of the following: {}".format(base_games))
        return 4

    MTG_MODS_PATH = os.path.join(MTG_PATH, "mods")

    if force_update_mtg_enable:
        shutil.rmtree(MT_MYGAME_DIR)

    # yes | cp -rf $MT_GAMES_DIR/minetest_game/* MT_MYGAME_DIR"
    # sudo rsync -a $MT_GAMES_DIR/minetest_game/* MT_MYGAME_DIR"

    try:
        # DOES update minetest_game, but does NOT delete extra mods:
        update_tree(base_game_path, MT_MYGAME_DIR)
        echo0("Updated \"" + MT_MYGAME_DIR + "\"...")
    except PermissionError:
        echo0(str(sys.exc_info()))
        echo0("")
        echo0("You must run " + __file__ + " as a user that can write to "
              "\"" + MT_MYGAME_DIR + "\"")
        echo0("")
        return 5

    try:
        # cd $HOME
        # tmp_game_conf_path = os.path.join(profile_path, "game.conf")
        outs = open(os.path.join(MT_MYGAME_DIR, "game.conf"), 'w')
        outs.write("name = subgametest")
        outs.close()
    except PermissionError:
        echo0(str(sys.exc_info()))
        echo0("")
        echo0("You must run " + __file__ + " as a user that can write to "
              "\"" + MT_MYGAME_DIR + "\"")
        echo0("")
        return 6
    # cmd_string = "sudo mv -f game.conf \MT_MYGAME_DIR\""
    # shutil.move(tmp_game_conf_path, os.path.join(MT_MYGAME_DIR, "game.conf"))

    good_dir = os.path.join(MT_MYGAME_DIR, "mods")
    if os.path.isdir(good_dir):
        echo0("Copied subgame to " + MT_MYGAME_DIR)
    else:
        echo0('FAILED to copy subgame to "{}" ("{}" is missing)'
              ''.format(MT_MYGAME_DIR, good_dir))
        return 7

    MT_MYGAME_MODS_PATH = os.path.join(MT_MYGAME_DIR, "mods")
    MTMOD_DEST_NAME = "minigamer"
    MTMOD_DEST_PATH = os.path.join(MT_MYGAME_MODS_PATH, MTMOD_DEST_NAME)

    # if force_update_mtg_mods_enable:
    #     for sub_name in os.listdir(base_game_path):
    #         sub_path = os.path.join(base_game_path, sub_name)
    #         dst_path = os.path.join(MT_MYGAME_DIR, sub_name)
    #         if sub_name[:1]!="." and os.path.isdir(sub_path):
    #             if os.path.isdir(dst_path):
    #                 shutil.rmtree(dst_path)

    if not os.path.isdir(GIT_REPOS_PATH):
        echo0("Cannot create " + GIT_REPOS_PATH + " so cannot continue.")
        return 8

    # TODO: actually install something (from spreadsheet maybe)

    mtg_mods_list = list()
    src_mods_path = MTG_MODS_PATH
    if os.path.isdir(src_mods_path):
        for sub_name in os.listdir(src_mods_path):
            sub_path = os.path.join(src_mods_path, sub_name)
            if sub_name[:1] != "." and os.path.isdir(sub_path):
                mtg_mods_list.append(sub_name)

    mods_installed_list = list()
    mods_added_list = list()

    dst_mods_path = MT_MYGAME_MODS_PATH
    if os.path.isdir(dst_mods_path):
        for sub_name in os.listdir(dst_mods_path):
            sub_path = os.path.join(dst_mods_path, sub_name)
            if sub_name[:1] != "." and os.path.isdir(sub_path):
                mods_installed_list.append(sub_name)
                if sub_name not in mtg_mods_list:
                    mods_added_list.append(sub_name)
    else:
        echo0("Missing '" + dst_mods_path + "'")

    echo0("")
    echo0("")
    echo0("Installed " + str(len(mods_installed_list)) + " mod(s)" +
          " (" + str(len(mtg_mods_list)) + " from " + mtg_game_name + ").")
    if len(mods_added_list) > 0:
        print("Added:")
        for mod_name in mods_added_list:
            print("  - " + mod_name)
    echo0("")
    # cd $TMP_DIR
    # git clone https://github.com/tenplus1/mobs_redo.git
    # git clone https://github.com/tenplus1/mobs_animal.git
    # git clone https://github.com/tenplus1/mobs_monster.git
    # git clone https://github.com/tenplus1/mobs_npc.git
    # but not:
    # git clone https://github.com/poikilos/minetest-minigamer.git
    # git clone https://github.com/poikilos/birthstones.git

    # Repo.clone_from(git_url, repo_dir)
    return 0


if __name__ == "__main__":
    code = main()
    # if code != 0:
    # input("press enter to close...")
    sys.exit(code)
