#!/usr/bin/env python

#region options
force_update_mtg_enable = False  # first delete subgametest then remake
#endregion options

try:
    input = raw_input
except NameError:
    pass

try:
    from git import Repo
except:
    print("You do not have gitpython installed.\n"
          "Please run the following commands in terminal\n"
          "For installing Python in Windows, the most usable option\n"
          " is CUSTOM install, then change System Path to\n"
          " 'install to hard drive'"
          " (otherwise first cd C:\Python27 [or your Python folder],\n"
          " but if in *nix-like environment first 'su -', and if no\n"
          " pip, use your software manager to install:\n"
          "   python-pip or python2-pip or python3-pip)\n"
          "python -m pip install --upgrade pip\n"
          "python -m pip install --upgrade pip wheel\n"
          "python -m pip install gitpython\n")
          #Possible commands:
          # pkg install -y python3-pip python2-pip
          # apt-get install -y python3-pip python2-pip
          # pacman -Syuu python2-pip python-pip
          #("Passing two --refresh or -y flags forces pacman to refresh
          # all package lists even if they are considered to be up to
          # date.")
    print("")
    input("press enter to close...")
    exit(1)


import os
import shutil
import sys
from winclient.forwardfilesync import *

profile_path = None
if 'HOME' in os.environ:  # if os_name=="windows":
    profile_path = os.environ['HOME']
else:
    profile_path = os.environ['USERPROFILE']

if not os.path.isdir(profile_path):
    print("")
    print("Failed to get existing home path--tried HOME & USERPROFILE")
    print("")
    input("press enter to close")
    exit(2)

USR_SHARE_MINETEST="/usr/share/games/minetest"
if not os.path.isdir(USR_SHARE_MINETEST):
    if os.path.isdir("/usr/local/share/minetest"):
        #IF git version is installed:
        USR_SHARE_MINETEST="/usr/local/share/minetest"
    if os.path.isdir("/usr/share/minetest"):
        USR_SHARE_MINETEST="/usr/share/minetest"

    if not os.path.isdir(USR_SHARE_MINETEST):
        print("Minetest could not be found in any known location. Try installing minetest or compiling from source or editing value of USR_SHARE_MINETEST in this script. Script ended early.")
        input("press enter to close...")
        exit(3)


MT_GAMES_DIR = os.path.join(USR_SHARE_MINETEST,"games")
MT_MYGAME_NAME = "subgametest"
MT_MYGAME_DIR=os.path.join(MT_GAMES_DIR,MT_MYGAME_NAME)

folder_path = os.path.join(MT_GAMES_DIR, "minetest_game")

if not os.path.isdir(folder_path):
    print("Could not find \"" + folder_path + "\". Script ended early.")
    input("press enter to close...")
    exit(4)

if force_update_mtg_enable:
    shutil.rmtree(MT_MYGAME_DIR)

#yes | cp -rf $MT_GAMES_DIR/minetest_game/* MT_MYGAME_DIR"
#sudo rsync -a $MT_GAMES_DIR/minetest_game/* MT_MYGAME_DIR"

try:
    #DOES update minetest_game, but does NOT delete extra mods:
    update_tree(folder_path, MT_MYGAME_DIR)
    print("Updated \"" + MT_MYGAME_DIR + "\"...")
except:
    print(str(sys.exc_info()))
    print("")
    print("You must run " + __file__ + " as a user that can write to "
          "\"" + MT_MYGAME_DIR + "\"")
    print("")
    input("press enter to close...")
    exit(5)

try:
    #cd $HOME
    #tmp_game_conf_path = os.path.join(profile_path, "game.conf")
    outs = open(os.path.join(MT_MYGAME_DIR, "game.conf"), 'w')
    outs.write("name = subgametest")
    outs.close()
except:
    print(str(sys.exc_info()))
    print("")
    print("You must run " + __file__ + " as a user that can write to "
          "\"" + MT_MYGAME_DIR + "\"")
    print("")
    input("press enter to close...")
    exit(6)
#cmd_string = "sudo mv -f game.conf \MT_MYGAME_DIR\""
#shutil.move(tmp_game_conf_path, os.path.join(MT_MYGAME_DIR, "game.conf"))

if os.path.isdir(os.path.join(MT_MYGAME_DIR,"mods")):
    print("Copied subgame to " + MT_MYGAME_DIR)
else:
    print("FAILED to copy subgame to " + MT_MYGAME_DIR)
    input("press enter to close...")
    exit(7)


MT_MYGAME_MODS_PATH = os.path.join(MT_MYGAME_DIR,"mods")
MTMOD_DEST_NAME = "minigamer"
MTMOD_DEST_PATH = os.path.join(MT_MYGAME_MODS_PATH, MTMOD_DEST_NAME)

#if force_update_mtg_mods_enable:
#    for sub_name in os.listdir(folder_path):
#        sub_path = os.path.join(folder_path, sub_name)
#        dst_path = os.path.join(MT_MYGAME_DIR, sub_name)
#        if sub_name[:1]!="." and os.path.isdir(sub_path):
#            if os.path.isdir(dst_path):
#                shutil.rmtree(dst_path)


if not os.path.isdir(os.path.join(profile_path,"Downloads")):
    os.makedirs(os.path.join(profile_path,"Downloads"))

if not os.path.isdir(os.path.join(profile_path,"Downloads")):
    print("Cannot create " + os.path.join(profile_path,"Downloads") + " so cannot continue.")
    input("press enter to close...")
    exit(8)

mods_installed_list = list()

TMP_DIR=os.path.join(os.path.join(profile_path,"Downloads"),"minetest-mods")

if not os.path.isdir(TMP_DIR):
    os.makedirs(TMP_DIR)

if not os.path.isdir(TMP_DIR):
    print("Cannot create " + TMP_DIR + " so cannot continue.")
    input("press enter to close...")
    exit(9)


print("")
print("")
print("Installed " + str(len(mods_installed_list)) + " mod(s).")
print("")
input("press enter to close...")
#cd $TMP_DIR
#git clone https://github.com/tenplus1/mobs_redo.git
#git clone https://github.com/tenplus1/mobs_animal.git
#git clone https://github.com/tenplus1/mobs_monster.git
#git clone https://github.com/tenplus1/mobs_npc.git
#but not:
#git clone https://github.com/expertmm/minetest-minigamer.git
#git clone https://github.com/expertmm/minetest-birthstones.git

#Repo.clone_from(git_url, repo_dir)


