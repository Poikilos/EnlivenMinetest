#!/bin/bash
# Copyright 2017 poikilos. License:
# Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:
# The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

#First make sure all folders in $HOME/.minetest are created (I am not sure whether this is required!):
# minetestserver
# Mods were found at https://forum.minetest.net/viewforum.php?f=11
# (Ubuntu 14.04 Trusty Tahr Server) folders were found using:
# cd /
# sudo find -name 'worlds' (worlds folder is in $HOME/.minetest)
# sudo find -name 'minimal' (stable build [such as 0.4.9 games folder is /usr/share/games/minetest/games, but git version games folder is /usr/local/share/minetest/games)

# ISSUES:
# * ERROR[Main]: Singleplayer mode says following mods could not be found: 3d_armor areas mobs mobs_animal mobs_monster protector technic treasurer unified_inventory xban2
# * update git discarding local changes:
#   (see https://stackoverflow.com/questions/4157189/git-pull-while-ignoring-local-changes)
#   git fetch --all
#   git reset --hard origin/master
#   git pull
#   #"even works when u have committed ur local changes, but still u want to revert" -agsachin
#
#   #git reset --hard
#   #git pull
#   #git clean -xdf
#   #-f remove untracked files, -d remove untracked directories, -x remove untracked OR ignored
sudo echo "starting ENLIVEN installer script..."




## this space was intentionally left blank


#region paste this part into terminal to get some great environment variables
if [ ! -f minetestenv.rc ]; then
  if [ -f "$HOME/GitHub/EnlivenMinetest" ]; then
    cd "$HOME/GitHub/EnlivenMinetest"
  elif [ -f "$HOME/git/EnlivenMinetest" ]; then
    cd "$HOME/git/EnlivenMinetest"
  elif [ -f "$HOME/Documents/GitHub/EnlivenMinetest" ]; then
    cd "$HOME/Documents/GitHub/EnlivenMinetest"
  fi
fi
if [ ! -f minetestenv.rc ]; then
  echo "ERROR: Nothing done since missing minetestenv.rc (must be in same directory)"
  sleep 1
  exit 1
fi
source minetestenv.rc
#endregion paste this part into terminal to get some great environment variables








## this space was intentionally left blank



if [ ! -f "`command -v minetestmapper`" ]; then
  if [ -f "`command -v apt`" ]; then
    sudo apt -y install libgd-dev libsqlite3-dev libleveldb-dev libhiredis-dev libpq-dev
  else
    if [ -f "`command -v pacman`" ]; then
      pacman -Syyu --noconfirm gd sqlite leveldb hiredis postgresql #postgresql-libs
    fi
  fi
  cd ~/Downloads
  if [ -d minetestmapper ]; then
    rm -Rf minetestmapper
  fi
  git clone https://github.com/minetest/minetestmapper.git
  cd minetestmapper
  cmake . -DENABLE_LEVELDB=1
  make -j2
  if [ -f minetestmapper ]; then
    sudo cp -f minetestmapper /usr/local/bin/
  else
    echo "FAILED to compile minetestmapper--python version will be used"
  fi
fi

if [ -d /tmp/local_mts_user ]; then
  # handle paranoia about directory with similar name
  rm -Rf /tmp/local_mts_user
fi
echo $USER > /tmp/local_mts_user
# BACKUP world.mt:
# workaround bug in earlier version of installer
sudo chown `cat /tmp/local_mts_user` "$MT_MYWORLD_DIR/world.mt"
if [ -f "$MT_MYWORLD_DIR/world.mt.1st" ]; then
  # workaround bug in earlier version of installer
  sudo chown `cat /tmp/local_mts_user` "$MT_MYWORLD_DIR/world.mt.1st"
fi
if [ ! -d "$MT_MYGAME_DIR" ]; then
  sudo mkdir "$MT_MYGAME_DIR"
else
  # workaround bug in earlier version of installer
  sudo chown -R `cat /tmp/local_mts_user` "$MT_MYGAME_DIR"
fi
if [ -f "$MT_MYWORLD_DIR/world.mt.1st" ]; then
  echo "Already backed up world.mt to $MT_MYWORLD_DIR/world.mt.1st"
else
  cp "$MT_MYWORLD_DIR/world.mt" "$MT_MYWORLD_DIR/world.mt.1st"
  echo "The original world.mt is now backed up at $MT_MYWORLD_DIR/world.mt.1st"
fi
if [ -f "$MT_MYWORLD_DIR/world.mt" ]; then
  mv -f "$MT_MYWORLD_DIR/world.mt" "$MT_MYWORLD_DIR/world.mt.bak"
fi




#process conf file (account for spaces around equal sign and variable names containing name of other variable name)
shopt -s extglob
configfile="$WORLD_MT_PATH" # set the actual path name of your (DOS or Unix) config file
tr -d '\r' < $configfile > $configfile.unix
while IFS='= ' read -r lhs rhs
do
    if [[ ! $lhs =~ ^\ *# && -n $lhs ]]; then
        rhs="${rhs%%\#*}"    # Del in line right comments
        rhs="${rhs%%*( )}"   # Del trailing spaces
        rhs="${rhs%\"*}"     # Del opening string quotes
        rhs="${rhs#\"*}"     # Del closing string quotes
        declare world_mt_var_$lhs="$rhs"
    fi
done < $configfile.unix




# REMAKE world.mt
cd
if [ -f "$WORLD_MT_PATH" ]; then
  # workaround bug in earlier version of installer
  sudo chown `cat /tmp/local_mts_user` "$WORLD_MT_PATH"
  sudo chgrp `cat /tmp/local_mts_user` "$WORLD_MT_PATH"
fi
echo "gameid = $MT_MYGAME_NAME" > "$WORLD_MT_PATH"
#if ! grep -q "backend =" "$WORLD_MT_PATH"; then
if [ -z "$world_mt_var_backend" ]; then
  echo "has no backend, setting leveldb..."
  echo "backend = leveldb" >> "$WORLD_MT_PATH"
fi
#if ! grep -q "backend" "$WORLD_MT_PATH"; then
if [ -z "$world_mt_var_player_backend" ]; then
 echo "has no player_backend, setting sqlite3..."
 echo "player_backend = sqlite3" >> "$WORLD_MT_PATH"
fi
echo "teleport_perms_to_build = false" >> "$WORLD_MT_PATH"
echo "teleport_perms_to_configure = false" >> "$WORLD_MT_PATH"
echo "teleport_requires_pairing = true" >> "$WORLD_MT_PATH"
echo "teleport_pairing_check_radius = 2" >> "$WORLD_MT_PATH"
echo "teleport_default_coordinates = 0,0,0" >> "$WORLD_MT_PATH"

#MT_MYGAME_DIR (a Minetest "game") is the equivalent of a Minecraft modpack, however, in this case it is actually a collection of mods and modpacks, either of which can be in the mods folder

#cd
if [ ! -d "$HOME/Downloads" ]; then
  mkdir "$HOME/Downloads"
fi
cd "$HOME/Downloads"

if [ -d "$MT_MYGAME_BAK" ];
then
  echo "already backed up to $MT_MYGAME_BAK"
else
  sudo mv "$MT_MYGAME_DIR" "$MT_MYGAME_BAK"
  if [ ! -d "$MT_MYGAME_DIR" ]; then
    sudo mkdir "$MT_MYGAME_DIR"
  fi
fi

#sudo mkdir "$MT_MYGAME_DIR"
#sudo mkdir "$MT_MYGAME_MODS_PATH"
if [ ! -d "$MT_MYGAME_DIR/" ]; then
  echo "ERROR: failed to create $MT_MYGAME_DIR, so cannot continue." > $err_txt
  cat $err_txt
  echo "  press Ctrl C to cancel ENLIVEN install or this terminal will close..."
  sleep 1
  echo " 3..."
  sleep 1
  echo " 2..."
  sleep 1
  echo " 1..."
  sleep 1
  exit 1
fi
#sudo cp -R $USR_SHARE_MINETEST/games/$mtgame_name/mods/* "$MT_MYGAME_DIR/mods/"
sudo cp -Rf $MT_MINETEST_GAME_PATH/* "$MT_MYGAME_DIR/"



#sudo su -
#WRITEABLE_MINETEST_CONF=$USR_SHARE_MINETEST/games/$MT_MYGAME_NAME/minetest.conf
WRITEABLE_MINETEST_CONF=$HOME/minetest.conf
rm -f "$HOME/minetest.conf"
if [ ! -f "$USR_SHARE_MINETEST/games/$MT_MYGAME_NAME/minetest.conf" ]; then
  sudo cp "$USR_SHARE_MINETEST/games/$mtgame_name/minetest.conf" "$USR_SHARE_MINETEST/games/$MT_MYGAME_NAME/minetest.conf.1st"
fi
cp "$USR_SHARE_MINETEST/games/$mtgame_name/minetest.conf" "$WRITEABLE_MINETEST_CONF"
touch "$WRITEABLE_MINETEST_CONF"
#4080 since boundaries in chunkymap/singleimage.py (to be compatible with approximate browser max image size) are -4096 to 4096
echo "map_generation_limit = 4096" >> "$WRITEABLE_MINETEST_CONF"
#NOTE: map_generation_limit (aka world boundary, world border, or world limit) must be divisible by 64, so for example, 5000 results in invisible wall at 4928
echo "protector_radius = 7" >> "$WRITEABLE_MINETEST_CONF"
echo "protector_flip = true" >> "$WRITEABLE_MINETEST_CONF"
echo "protector_pvp = true" >> "$WRITEABLE_MINETEST_CONF"
echo "protector_pvp_spawn = 10" >> "$WRITEABLE_MINETEST_CONF"
echo "protector_drop = false" >> "$WRITEABLE_MINETEST_CONF"
echo "protector_hurt = 3" >> "$WRITEABLE_MINETEST_CONF"
echo "#optional:" >> "$WRITEABLE_MINETEST_CONF"
echo "map_generation_limit = 5000" >> "$WRITEABLE_MINETEST_CONF"
echo "#only for worldedge mod:" >> "$WRITEABLE_MINETEST_CONF"
echo "world_edge = 5000" >> "$WRITEABLE_MINETEST_CONF"
echo "default_privs = interact,shout,home" >> "$WRITEABLE_MINETEST_CONF"
echo "max_users = 50" >> "$WRITEABLE_MINETEST_CONF"
echo "motd = \"Actions and chat messages are logged. Use inventory to see recipes (use web for live map if available).\""  >> "$WRITEABLE_MINETEST_CONF"
echo "disallow_empty_passwords = true" >> "$WRITEABLE_MINETEST_CONF"
echo "secure.trusted_mods = advanced_npc" >> "$WRITEABLE_MINETEST_CONF"
echo "server_dedicated = false" >> "$WRITEABLE_MINETEST_CONF"
#echo "hudbars_bar_type = statbar_modern" >> "$WRITEABLE_MINETEST_CONF"  #TODO: remove this after fully deprecated
echo "sprint_speed = 2.25" >> "$WRITEABLE_MINETEST_CONF"  # default is 1.3
echo "sprint_jump = 1.25" >> "$WRITEABLE_MINETEST_CONF"  # default is 1.1
echo "sprint_stamina_drain = .5" >> "$WRITEABLE_MINETEST_CONF"  # default is 2
echo "bones_position_message = true" >> "$WRITEABLE_MINETEST_CONF"  # default is false--this is for client-side chat message (server-side logging always on though)
#no longer needed since these mods check for player_api to determine whether v3 model is used:
if [ "$version_0_5_enable" = "true" ]; then
#  echo "player_model_version = default_character_v3" >> "$WRITEABLE_MINETEST_CONF"  # used by playeranim
   echo "using version 5 branch of mods..."
else
#  echo "player_model_version = default_character_v2" >> "$WRITEABLE_MINETEST_CONF"  # used by playeranim
   echo "using stable (minetest 0.4) branch of mods..."
   echo "3..."
   sleep 1
   echo "2..."
   sleep 1
   echo "1..."
   sleep 1
fi
sudo mv -f $HOME/minetest.conf "$USR_SHARE_MINETEST/games/$MT_MYGAME_NAME/minetest.conf"

if [ -f "$MT_MYGAME_DIR/game.conf.1st" ]; then
  echo "Already backed up $MT_MYGAME_DIR/game.conf to $MT_MYGAME_DIR/game.conf.1st"
else
  sudo cp "$MT_MYGAME_DIR/game.conf" "$MT_MYGAME_DIR/game.conf.1st"
fi
echo "name = $MT_MYGAME_NAME" > "$HOME/game.conf"
sudo mv -f "$HOME/game.conf" "$MT_MYGAME_DIR/game.conf"
#su -
#FAILS: echo "name = $MT_MYGAME_NAME" > "$MT_MYGAME_DIR/game.conf"
#sudo nano "$MT_MYGAME_DIR/game.conf"
echo ""
echo "You should see $MT_MYGAME_NAME in the list below if the game was configured properly:"
if [ -f "`command -v minetestserver`" ]; then
  minetestserver --gameid list
elif [ -f "`command -v minetest`" ]; then
  minetest --gameid list
else
  echo "WARNING: neither minetestserver nor minetest is in the system path"
fi
echo ""


#region UTILITY MODS
# https://forum.minetest.net/viewtopic.php?f=11&t=12440&p=310915#p310915
# wget https://forum.minetest.net/download/file.php?id=6140
# file.php?id=6140 forum dl changed, so use salahzar's GitHub upload instead:
add_git_mod invhack minetest-invhack https://github.com/salahzar/minetest-invhack.git
# add_zip_mod worldedit Uberi-Minetest-WorldEdit-* https://github.com/Uberi/MineTest-WorldEdit/zipball/master
# add_zip_mod worldedit Minetest-WorldEdit-* https://github.com/Uberi/MineTest-WorldEdit/zipball/master
echo "Installing Uberi's worldedit..."
add_git_mod worldedit Minetest-WorldEdit https://github.com/Uberi/Minetest-WorldEdit.git
# metatools: poikilos fork of LeMagnesium's minetest-mod-metatools
add_git_mod metatools minetest-mod-metatools https://github.com/poikilos/minetest-mod-metatools.git
# forum_url="https://forum.minetest.net/viewtopic.php?f=11&t=9376"
# author="tenplus1"
# description="not the original 2012 protector or 2012 fork of 2012 protector; must be logged in to download protector.zip release version at https://forum.minetest.net/download/file.php?id=5046"
add_git_mod protector protector https://notabug.org/TenPlus1/protector.git
#formerly https://github.com/kaeza/minetest-xban2/archive/master.tar.gz
#add_git_mod xban2 xban2 https://github.com/minetest-mods/xban2.git
remove_mod xban2

#https://forum.minetest.net/viewtopic.php?t=10823
echo "Installing Advanced Ban, so make sure your server is whitelisted (otherwise use xban2)!"
echo "(whitelist + xban is recommended, so that you get true user access control."
echo "If you have a mechanism to automatically whitelist people, you'll probably"
echo "want to have no priveleges by default, and have an in-game mechanism to get them)"
add_git_mod advancedban advancedban https://github.com/srifqi/advancedban

echo "Installing ShadowNinja's <https://forum.minetest.net/viewtopic.php?t=7239>"
echo "Installing ShadowNinja's <https://forum.minetest.net/viewtopic.php?t=7239>" >> $MTMOD_SRC_ZIP.txt
# areas: ShadowNinja rewrite of node ownership
# forum_url="https://forum.minetest.net/viewtopic.php?t=7239"
add_git_mod areas areas https://github.com/ShadowNinja/areas.git
# author="ShadowNinja"
# forum_url="https://forum.minetest.net/viewtopic.php?id=8434"
add_git_mod whitelist whitelist https://github.com/ShadowNinja/whitelist.git
add_git_mod vote vote https://github.com/minetest-mods/vote.git
#endregion UTILITY MODS

#region MOB AND WORLDGEN MODS
# forum_url="https://forum.minetest.net/viewtopic.php?id=7263"
# TESTED: with mg, tsm_railcorridors sometimes have chests with loot (using seed BagEnd; /teleport 188,-304.5,-120)
#add_git_mod mg mg https://github.com/minetest-mods/mg.git
add_git_mod worldedge worldedge https://github.com/minetest-mods/worldedge.git
#wget https://github.com/BlockMen/cme/releases/download/v2.3/cme-2_3-BlockMen.zip
#unzip cme-2_3-BlockMen.zip
#sudo mv cme "$MT_MYGAME_MODS_PATH/cme"
# description="(must be logged in to forum to download release version at https://forum.minetest.net/download/file.php?id=5282)"
# author="TenPlus1"
add_git_mod mobs mobs_redo https://notabug.org/TenPlus1/mobs_redo.git
add_git_mod mobs_monster mobs_monster https://notabug.org/TenPlus1/mobs_monster.git
add_git_mod mobs_animal mobs_animal https://notabug.org/TenPlus1/mobs_animal.git
add_git_mod mob_horse mob_horse https://notabug.org/tenplus1/mob_horse.git
# mobs_sky: (requires mobs redo) [mod-pack] sky critters (for mobs_redo) [mobs_sky] <https://forum.minetest.net/viewtopic.php?f=9&t=12688>
# add_git_mod mobs_sky mobs_sky https://github.com/blert2112/mobs_sky.git
add_git_mod mobs_sky mobs_sky https://github.com/poikilos/mobs_sky.git

spawners_enable="true"
if [ "$spawners_enable" = "true" ]; then
  # forum_url: https://forum.minetest.net/viewtopic.php?f=11&t=13857
    # description:
    # * NO LONGER REPLACES pyramids.
    # * Works with mobs_redo and creatures.
    # * optionally makes use of fire (in minetest_game; only uses fire:flint_and_steel), mobs, creatures, bones, xpanes (now part of minetest_game)
    # * only RECIPES require fake_fire and xpanes
    # * NOW (2017-2018) IS A MODPACK: formerly was a mod named spawners, now is a modpack containing:
    #   * spawners_env: appears in Dungeons and Temples (the pink stone ones); spawns hostile mobs; has small chance of spawning a spawner
    #   * spawners_mobs: spawns non-hostile mobs
    #   * spawners_ores: spawns ores
    #add_zip_mod spawners minetest_gamers-spawners-* https://bitbucket.org/minetest_gamers/spawners/get/master.zip
    add_git_mod spawners spawners https://bitbucket.org/minetest_gamers/spawners.git
    MTMOD_DEST_NAME=spawners/spawners_ores
    MTMOD_DEST_PATH=$MT_MYGAME_MODS_PATH/$MTMOD_DEST_NAME
    if [ -d "$MTMOD_DEST_PATH" ]; then
      echo "removing $MTMOD_DEST_NAME..."
      sudo rm -Rf "$MTMOD_DEST_PATH"
    else
      echo "ERROR: could not find $MTMOD_DEST_PATH for removal, so cancelling ENLIVEN install"
      echo "  press Ctrl C to cancel ENLIVEN install or this terminal will close..."
      sleep 1
      echo " 3..."
      sleep 1
      echo " 2..."
      sleep 1
      echo " 1..."
      sleep 1
      exit 1
    fi
    if [ -d "$MTMOD_DEST_PATH" ]; then
      echo "ERROR: could not remove $MTMOD_DEST_PATH for removal, so cancelling ENLIVEN install"
      echo "  press Ctrl C to cancel ENLIVEN install or this terminal will close..."
      sleep 1
      echo " 3..."
      sleep 1
      echo " 2..."
      sleep 1
      echo " 1..."
      sleep 1
      exit 1
    fi

    #defaults are:
    #SPAWN_PYRAMIDS = false
    #SPAWNERS_GENERATE = true
    #CHESTS_GENERATE = false
    MTMOD_DEST_NAME=spawners/spawners_env
    MTMOD_DEST_PATH=$MT_MYGAME_MODS_PATH/$MTMOD_DEST_NAME
    cd /tmp
    echo "SPAWN_PYRAMIDS = true" > settings.txt
    echo "SPAWNERS_GENERATE = true" >> settings.txt
    echo "CHESTS_GENERATE = false" >> settings.txt
    sudo mv settings.txt "$MTMOD_DEST_PATH/"  # formerly $MT_MYGAME_MODS_PATH/spawners/, now is spawners/spawners_env/
    echo "NOTE: in spawners, only SPAWNERS_GENERATE or CHESTS_GENERATE, not both (chests seem to override) spawn in world for now. See thread for updated info: https://forum.minetest.net/viewtopic.php?f=11&t=13857&start=25"
    echo "see also poikilos's game-install-enliven-testing-SPAWNERS_BOTH_DEBUG.txt"

    # dungeon_loot is part of default game, but I haven't created loot tables for this subgame yet, so remove:
    remove_mod "dungeon_loot"

    # NOTE: tsm_chests_dungeon supercedes dungeon_loot, but dungeon_loot :
    if [ -d "$MT_MYGAME_MODS_PATH/dungeon_loot" ]; then
      echo "WARNING: tsm_chests_dungeon may not be compatible with dungeon_loot"
      if [ -d "$MT_MYGAME_MODS_PATH/tsm_chests_dungeon" ]; then
        echo "so removing tsm_chests_dungeon"
      else
        echo "so skipping tsm_chests_dungeon"
      fi
      echo "press Ctrl C to cancel installing ENLIVEN"
      sleep 2
      echo "4..."
      sleep 1
      echo "3..."
      sleep 1
      echo "2..."
      sleep 1
      echo "1..."
      sleep 1
      if [ -d "$MT_MYGAME_MODS_PATH/tsm_chests_dungeon" ]; then
        remove_mod tsm_chests_dungeon
      fi
    else
      add_git_mod tsm_chests_dungeon minetest_tsm_chests_dungeon http://repo.or.cz/minetest_tsm_chests_dungeon.git
    fi
  # NOTE: spawners no longer adds pyramids, so:
  # add_git_mod tsm_pyramids tsm_pyramids http://repo.or.cz/minetest_pyramids/tsm_pyramids.git
  # Wuzzy's doesn't account for 5.0.0-dev yet (nodeupdate is now minetest.check_for_falling) so use custom fork:
  add_git_mod tsm_pyramids tsm_pyramids https://github.com/poikilos/tsm_pyramids.git

else
  remove_mod tsm_chests_dungeon
  remove_mod spawners
  # tsm_pyramids: NOTE: results in "tsm_pyramids:mummy" not defined, but xisd fork allows configuring mummy so MAY NEED spawners_mobs:mummy (or original pyramids mod?)
  add_git_mod tsm_pyramids tsm_pyramids http://repo.or.cz/minetest_pyramids/tsm_pyramids.git
  add_git_mod loot loot https://github.com/minetest-mods/loot.git
  # TEST LOOT: use seed "BigIdea" (without mg mod installed) then:
  # * teleport to dungeon: -332,-1483,272
  # * for more, turn on noclip&freemove and teleport to -339,-1462,289 and look around
  # RESULTS: "loot" (with loot_dungeons=true option in world.mt or not set which defaults to true)
  # seems to provide too much loot--has mese crystals (blocks in one of the chests), loads of iron and many other minerals -- many chests in same dungeon and no enemies
  # other items: cotton seed, several gold ingot, some diamonds
  # other items in nearby dungeon: bread, wheat seeds, apples, several gold ingot, some diamonds
  # * teleport to nearby dungeons:
  #   * -328,-1468.5,289
  #   * -355,-1470,312
  #   * -420,-1493,267
  #   * -432,-1556,329
  # * other dungeons:
  #   * -531,-1402,-143 (several other dungeons are near it)
  # * caverealm at:
  #   * -511,-1893,111
  # * humid desert (small) at:
  #   * -538,2.5,-82.4
  # * amazing mountain jungle view from:
  #   * 2499,6.5,2404
  # * magma_conduits vs water at:
  #   * 2686,2.5,-2595
  # * amazing savannah view at:
  #   * 2175,3.5,-2714
  # * tsm_pyramids:
  #   * 1252,6.5,-847
fi

add_git_mod treasurer minetest_treasurer http://repo.or.cz/minetest_treasurer.git

cd "$HOME/Downloads"
MTMOD_DEST_NAME=trm_pyramids
MTMOD_UNZ_NAME=trm_pyramids
MTMOD_DEST_PATH=$MT_MYGAME_MODS_PATH/$MTMOD_DEST_NAME
if [ ! -z "`ls | grep $MTMOD_UNZ_NAME`" ]; then  # works with wildcard in variable
  rm -Rf "$MTMOD_UNZ_NAME"
fi
mkdir "$MTMOD_UNZ_NAME"
cd "$MTMOD_UNZ_NAME"
wget https://github.com/MinetestForFun/server-minetestforfun/raw/master/mods/trm_pyramids/depends.txt
wget https://github.com/MinetestForFun/server-minetestforfun/raw/master/mods/trm_pyramids/init.lua
wget https://github.com/MinetestForFun/server-minetestforfun/raw/master/mods/trm_pyramids/more_trms.lua
wget https://github.com/MinetestForFun/server-minetestforfun/blob/master/LICENSE
if [ -d "$MTMOD_DEST_PATH" ]; then
  sudo rm -Rf "$MTMOD_DEST_PATH"
fi
sudo mkdir "$MTMOD_DEST_PATH"
sudo mv -f depends.txt "$MTMOD_DEST_PATH/"
sudo mv -f init.lua "$MTMOD_DEST_PATH/"
sudo mv -f more_trms.lua "$MTMOD_DEST_PATH/"
sudo mv -f LICENSE "$MTMOD_DEST_PATH/"
cd ..
rmdir "$MTMOD_UNZ_NAME"
if [ ! -z "`ls "$MTMOD_DEST_PATH"`" ]; then
  echo "  [ + ] added as $MTMOD_DEST_PATH"
else
  echo "  [ ! ] failed to install files to $MTMOD_DEST_PATH"
  sleep 4
fi

add_git_mod moreblocks moreblocks https://github.com/minetest-mods/moreblocks.git
# plantlife_modpack: includes bushes:* with fruit and fruit recipes
add_git_mod plantlife_modpack plantlife_modpack https://github.com/minetest-mods/plantlife_modpack.git
add_git_mod bushes_soil bushes_soil https://github.com/poikilos/bushes_soil.git

# forum_url="https://forum.minetest.net/viewtopic.php?f=9&t=12368"
# description="Installing Napiophelios's lapis fork since has blocks, but minetest-mods has a version as well, with dye (not used): https://forum.minetest.net/viewtopic.php?f=9&t=11287"
add_git_mod lapis LapisLazuli https://github.com/Napiophelios/LapisLazuli.git
echo "patching lapis (Napiophelios's fork) to enable columns..."
cd $HOME/Downloads
if [ -f "init.lua" ]; then
  sudo rm init.lua
fi
MTMOD_DEST_NAME=lapis
MTMOD_DEST_PATH=$MT_MYGAME_MODS_PATH/$MTMOD_DEST_NAME
head -3 "$MTMOD_DEST_PATH/init.lua" > init.lua
if [ -f "$MTMOD_DEST_PATH/init.lua" ]; then
  if [ ! -f "$MTMOD_DEST_PATH/columns_enabled" ]; then
    # cat starting at line after head command above to not skip any
    # lines, in case later version changes position of lines
    echo 'dofile(minetest.get_modpath("lapis").."/columns.lua")' >> init.lua
    tail -n +4 "$MTMOD_DEST_PATH/init.lua" >> init.lua
    echo "true" > "columns_enabled"
    sudo mv -f columns_enabled "$MTMOD_DEST_PATH/"
    sudo mv -f init.lua "$MTMOD_DEST_PATH/"
    echo "PATCHED $MTMOD_DEST_PATH/init.lua to enable columns"
  else
    echo "WARNING: not enabling columns since $MTMOD_DEST_PATH/columns_enabled file exists"
  fi
else
  echo "FAILED to patch lapis since no $MTMOD_DEST_PATH/init.lua"
  echo "  press Ctrl C to cancel ENLIVEN install or this terminal will close..."
  sleep 1
  echo " 3..."
  sleep 1
  echo " 2..."
  sleep 1
  echo " 1..."
  sleep 1
  exit 1
fi

echo "not installing helicopter--crashes 0.4.14-git, but was updated on 2017-06-08 and was not tested since then"
# add_git_mod helicopter helicopter https://github.com/SokolovPavel/helicopter.git
add_git_mod biome_lib biome_lib https://github.com/minetest-mods/biome_lib.git
add_git_mod moretrees moretrees https://github.com/minetest-mods/moretrees.git

# in order of dependency (also, clicking armor in unified inventory crashes the game without technic installed since checks radation):
add_git_mod mesecons mesecons https://github.com/minetest-mods/mesecons
add_git_mod pipeworks pipeworks https://github.com/minetest-mods/pipeworks.git
add_git_mod technic technic https://github.com/minetest-mods/technic.git
add_git_mod technic_armor technic_armor https://github.com/stujones11/technic_armor.git
# NOTE: load_mod is not a thing for subgames (all mods in subgame are loaded if subgame is loaded)
#add_git_mod caverealms minetest-caverealms https://github.com/HeroOfTheWinds/minetest-caverealms
# FaceDeer's caverealms REQUIRES subterrane:
add_git_mod subterrane subterrane https://github.com/minetest-mods/subterrane.git
echo "Installing FaceDeer's v7-biome-integrated fork of HeroOfTheWinds' caverealms"
add_git_mod caverealms minetest-caverealms https://github.com/FaceDeer/minetest-caverealms.git
#if [ -f "master.zip" ]; then
  #rm master.zip
#fi
#wget https://github.com/Splizard/minetest-mod-snow/archive/master.zip
#mv master.zip snow.zip
#unzip snow.zip
#mv minetest-mod-snow-master snow
#sudo mv snow "$MT_MYGAME_MODS_PATH/snow"
# (since snow prevents server 0.4.13 git 2016-02-16 from starting):
#sudo mv $MT_MYGAME_MODS_PATH/snow $HOME/Downloads/snow

# formerly https://github.com/Calinou/moreores.git
add_git_mod moreores moreores https://github.com/minetest-mods/moreores.git
#the following is NOT needed, since one of the mods above adds the home gui and home permission (but no /home or /sethome command)
#if [ -f "master.zip" ]; then
  #rm master.zip
#fi
#wget https://github.com/cornernote/minetest-home_gui/archive/master.zip
#mv master.zip minetest-home_gui.zip
#unzip minetest-home_gui.zip
#sudo mv minetest-home_gui-master/home_gui "$MT_MYGAME_MODS_PATH/home_gui"
#echo "snow:snow 255 255 255" >> $HOME/minetest/util/colors.txt
#echo "snow:snow_block 255 255 255" >> $HOME/minetest/util/colors.txt
#echo "snow:ice 144 217 234" >> $HOME/minetest/util/colors.txt
#sh chunkymap/install-ubuntu.sh
#remove_mod tsm_mines
#remove_mod tsm_railcorridors
add_git_mod tsm_mines tsm_mines http://repo.or.cz/tsm_mines.git
add_git_mod tsm_railcorridors tsm_railcorridors http://repo.or.cz/RailCorridors/tsm_railcorridors.git


############ BOOST CARTS REQUIRES MESECONS ############
##### NEEDED since carts in minetest_game added much of this functionality but not yet startstoprail nor detectorrail #####
#See also carts plus, a fork of carts (the PilzAdam one later added to minetest_game) https://github.com/Kilarin/minetest-mod-carts-plus which adds touring rails, a hand break, switching, and view locking
#NOTE: boost_cart has handbrake (back key), Rail junction switching with the 'right-left' walking keys
#So either install this mod or do (less functionality):
#minetest.register_alias("boost_cart:detectorrail", "carts:rail")
#minetest.register_alias("boost_cart:startstoprail", "carts:powerrail")
#-- carts:brakerail
#-- carts:cart
#-- carts:powerrail
#-- carts:rail
# forum_url="https://forum.minetest.net/viewtopic.php?f=11&t=10172&hilit=boost+cart"
# birthstones: poikilos fork of a rather non-maintained mod--forum link is at https://forum.minetest.net/viewtopic.php?id=3663 (original mod was at https://github.com/Doc22/birthstones-mod.git)
add_git_mod birthstones minetest-birthstones https://github.com/poikilos/minetest-birthstones.git
add_git_mod bakedclay bakedclay https://notabug.org/tenplus1/bakedclay.git
add_git_mod quartz quartz https://github.com/minetest-mods/quartz
add_git_mod magma_conduits magma_conduits https://github.com/FaceDeer/magma_conduits.git
# dynamic_liquid: makes suspended source blocks move down until supported--therefore improves the underground especially when using mods like magma_conduits
remove_mod dynamic_liquid
#add_git_mod dynamic_liquid dynamic_liquid https://github.com/minetest-mods/dynamic_liquid.git
#endregion MOB AND WORLDGEN MODS



#region NON-WORLDGEN NODE/ITEM MODS
#add_git_mod mapfix mapfix https://github.com/minetest-mods/mapfix
add_git_mod boost_cart boost_cart https://github.com/SmallJoker/boost_cart.git
echo "Installing minetest-mods' (NOT MinetestForFun's PvP fork of Echoes91's, NOT Echoes91's Throwing enhanced NOT PilzAdam's NOT Jeija's) Throwing <https://forum.minetest.net/viewtopic.php?f=11&t=11437>"
add_git_mod throwing throwing https://github.com/minetest-mods/throwing.git
add_git_mod throwing_arrows throwing_arrows https://github.com/minetest-mods/throwing_arrows.git
echo "Installing Minetestforfun's (NOT wulfsdad's) fishing <https://forum.minetest.net/viewtopic.php?f=11&t=13659>"
echo "Installing Minetestforfun's (NOT wulfsdad's) fishing <https://forum.minetest.net/viewtopic.php?f=11&t=13659>" > ~/Downloads/fishing.txt
add_git_mod fishing fishing https://github.com/MinetestForFun/fishing.git
cd "$HOME/Downloads"
echo "Installing AntumMT's modernized fork of Kilarin's compassgps (NOT TeTpaAka, nor Echo, nor PilzAdam compass) <https://forum.minetest.net/viewtopic.php?t=9373>"
echo "Installing AntumMT's modernized fork of Kilarin's compassgps (NOT TeTpaAka, nor Echo, nor PilzAdam compass) <https://forum.minetest.net/viewtopic.php?t=9373>" > ~/Downloads/compassgps.txt
# https://github.com/Kilarin/compassgps.git
#add_git_mod compassgps mod-compassgps https://github.com/AntumMT/mod-compassgps.git
add_git_mod compassgps compassgps https://github.com/poikilos/compassgps.git

remove_mod helicopter
add_git_mod sounding_line sounding_line https://github.com/minetest-mods/sounding_line.git
add_git_mod mywalls mywalls https://github.com/minetest-mods/mywalls.git
add_git_mod mymasonhammer mymasonhammer https://github.com/minetest-mods/mymasonhammer.git
add_git_mod ts_furniture ts_furniture https://github.com/minetest-mods/ts_furniture.git
# Git 1.7.10 need `--single-branch` option to prevent getting all branches (see https://stackoverflow.com/questions/1911109/how-to-clone-a-specific-git-branch)
#git clone -b MT_0.5.0-dev --single-branch https://git@github.com/stujones11/minetest-3d_armor.git
#see also 0.5 branch https://github.com/stujones11/minetest-3d_armor/tree/MT_0.5.0-dev
#"stable" version is at https://github.com/stujones11/minetest-3d_armor/archive/version-0.4.11.zip
#add_zip_mod 3d_armor minetest-3d_armor-MT_0.5.0-dev https://github.com/stujones11/minetest-3d_armor/archive/MT_0.5.0-dev.zip
# git clone -b MT_0.5.0-dev --single-branch https://git@github.com/stujones11/minetest-3d_armor.git
if [ "$version_0_5_enable" = "true" ]; then
  echo "  trying to get 3d_armor 0.5.0-dev branch..."
  add_git_mod 3d_armor minetest-3d_armor https://github.com/stujones11/minetest-3d_armor.git "MT_0.5.0-dev"
else
  echo "  trying to get 3d_armor main branch..."
  add_git_mod 3d_armor minetest-3d_armor https://github.com/stujones11/minetest-3d_armor.git
fi
#mv minetest-3d_armor-master minetest-3d_armor_MODPACK
#sudo mv minetest-3d_armor_MODPACK/wieldview $MT_MYGAME_MODS_PATH/wieldview
#sudo mv minetest-3d_armor_MODPACK/3d_armor $MT_MYGAME_MODS_PATH/3d_armor
#sudo mv minetest-3d_armor_MODPACK/shields $MT_MYGAME_MODS_PATH/shields

add_git_mod homedecor_modpack homedecor_modpack https://github.com/minetest-mods/homedecor_modpack.git
add_git_mod unifieddyes unifieddyes https://github.com/minetest-mods/unifieddyes.git
#Sokomine's original version has no security ( https://forum.minetest.net/viewtopic.php?id=4877 )
#  https://github.com/Sokomine/travelnet/archive/master.zip
add_git_mod travelnet travelnet https://github.com/poikilos/travelnet.git
add_git_mod anvil anvil https://github.com/minetest-mods/anvil.git
add_git_mod sling sling https://github.com/minetest-mods/sling.git
#REPLACES PilzAdam's, modified by kaeza, maintained by VenessaE; FORMERLY in homedecor_modpack
#forum post: https://forum.minetest.net/viewtopic.php?t=13762
# kaeza's signs_lib (forked from PilzAdam's and TheXYZ's code) was moved here from: https://github.com/kaeza/minetest-signs_lib-extrafonts/archive/master.zip
add_git_mod signs_lib signs_lib https://github.com/minetest-mods/signs_lib.git

farming_redo_enable="false"
if [ -f "$MT_MYWORLD_DIR/farming_redo_enable" ]; then
  farming_redo_enable="true"
else
  echo "$MT_MYWORLD_DIR/farming_redo_enable not found (may contain anything or nothing to enable), so not using farming_redo"
fi
if [ "$farming_redo_enable" = "true" ]; then
  remove_mod crops
  add_git_mod farming farming https://notabug.org/tenplus1/farming.git
else
  remove_mod farming
  sudo cp -R $USR_SHARE_MINETEST/games/$mtgame_name/mods/farming $MT_MYGAME_MODS_PATH/
  if [ -d "$MT_MYGAME_MODS_PATH/farming" ]; then
    echo "  [ + ] reinstalled minetest_game farming."
  else
    echo "ERROR: failed to install $USR_SHARE_MINETEST/games/$mtgame_name/mods/farming to $MT_MYGAME_MODS_PATH/farming, so cannot continue." > $err_txt
    cat $err_txt
    echo "  press Ctrl C to cancel ENLIVEN install or this terminal will close..."
    sleep 1
    echo " 3..."
    sleep 1
    echo " 2..."
    sleep 1
    echo " 1..."
    sleep 1
    exit 1
  fi
  add_git_mod crops crops https://github.com/minetest-mods/crops
fi
# forum_url="https://forum.minetest.net/viewtopic.php?f=11&t=10423"
# Wuzzy's slimenodes mod (only available via /give command).
# web view: http://repo.or.cz/w/minetest_slimenodes.git
# add_git_mod slimenodes minetest_slimenodes http://repo.or.cz/minetest_slimenodes.git
# use poikilos fork instead:
add_git_mod slimenodes slimenodes https://github.com/poikilos/slimenodes.git
# ropes: adds rope spools that are mounted to the side or bottom of a node and can be cut with any choppy tool while someone lower is climbing; doesn't lower into protected areas; also has rope ladders
add_git_mod ropes ropes https://github.com/minetest-mods/ropes.git
add_git_mod digilines digilines https://github.com/minetest-mods/digilines.git
# treasurer forum post here: https://forum.minetest.net/viewtopic.php?t=7292
# (this trmp is linked from there)
#(a trmp is just a modpack of TRMs for treasurer. At least one trm must be installed for treasurer to to anything)
# MTMOD_DL_ZIP=file.php?id=1301
# Copied to GitHub by ClockGen (I posted the link below on the forum page)
# wget -O $MTMOD_SRC_ZIP https://forum.minetest.net/download/file.php?id=1301
#add_git_mod trmp_minetest_game trmp_minetest_game https://github.com/ClockGen/trmp_minetest_game.git
#fixed version with correct dye list for 0.4.16 (submitted pull request to ClockGen 2018-02-08):
add_git_mod trmp_minetest_game trmp_minetest_game https://github.com/poikilos/trmp_minetest_game.git

#forum_url = "http://minetest.org/forum/viewtopic.php?f=11&t=4870&sid=3ccbe3a667c6201075fc475ef7dc7cea"
#see also minetest-mods version:
add_git_mod awards awards https://github.com/minetest-mods/awards.git
#xisd is GONE from GitHub:
#add_git_mod awards_board awards_board https://github.com/xisd/awards_board.git
add_git_mod awards_board awards_board https://gitlab.com/poikilos/awards_board.git
#endregion NON-WORLDGEN NODE/ITEM MODS






#region PLAYER UX MODS
echo "Adding TenPlus1's money (BARTER-ONLY fork of kotolegokot's minetest-mod-money):"
add_git_mod money money https://notabug.org/TenPlus1/money
add_git_mod lightning lightning https://github.com/minetest-mods/lightning.git
add_git_mod unified_inventory unified_inventory https://github.com/minetest-mods/unified_inventory.git

# Byakuren. <https://forum.minetest.net/viewtopic.php?f=9&t=13941>.
# add_git_mod monoidal_effects monoidal_effects https://github.com/minetest-mods/monoidal_effects.git
# monoidal_effects by Byakuren [raymoo on GitHub] is deprecated by player_monoids by Byakuren [raymoo on GitHub] +playereffects by Wuzzy
# according to the author https://forum.minetest.net/viewtopic.php?t=13941
add_git_mod player_monoids player_monoids https://github.com/minetest-mods/player_monoids.git

# forum_url="https://forum.minetest.net/viewtopic.php?f=11&t=11153&hilit=hunger"
# description="Wuzzy's hudbars (no builtin bars; used by sprint, hbhunger, and hbarmor)"
# not git://repo.or.cz/minetest_hudbars.git
# add_git_mod hudbars minetest_hudbars http://repo.or.cz/minetest_hudbars.git
# hudbars doesn't work with 5.0.0-dev so instead revert to GunshipPenguin sprint
# and use hunger_ng where hudbars is optional
# TODO: find non-hudbars armor for hud [maybe strength, not wear like hbarmor):

# forum_url="https://forum.minetest.net/viewtopic.php?f=9&t=9650"
add_git_mod sprint sprint https://github.com/GunshipPenguin/sprint.git
#remove_mod sprint
add_git_mod hunger_ng hunger_ng https://gitlab.com/4w/hunger_ng.git

remove_mod hudbars
remove_mod hbsprint
# NOTE: hbsprint bar is on auto-hide by default (world.mt can set hudbars_autohide_stamina to true or false)
#add_git_mod hbsprint hbsprint https://github.com/minetest-mods/hbsprint.git
# armor_monoid: an api for creating multipliers for damage types (used by 3d_armor)
add_git_mod armor_monoid armor_monoid https://github.com/minetest-mods/armor_monoid.git

# author="Wuzzy"
# forum_url="https://forum.minetest.net/viewtopic.php?f=11&t=11153&hilit=hunger"
# not git://repo.or.cz/minetest_hbarmor.git
add_git_mod hbarmor minetest_hbarmor http://repo.or.cz/minetest_hbarmor.git
# author="Wuzzy
# description="hbhunger for hudbars https://forum.minetest.net/viewtopic.php?f=11&t=11153&hilit=hunger"
# forum_url="https://forum.minetest.net/viewtopic.php?f=9&t=11336"
# not git://repo.or.cz/minetest_hbhunger.git
add_git_mod hbhunger minetest_hbhunger http://repo.or.cz/minetest_hbhunger.git
add_git_mod playereffects minetest_playereffects http://repo.or.cz/minetest_playereffects.git
#MarkBu's ambience/ambiance ambient sounds (burli on https://forum.minetest.net/viewtopic.php?f=9&t=14814 )
#add_git_mod ambianceplus ambianceplus https://github.com/MarkuBu/ambianceplus.git
# tenplus1's ambience/ambiance ambient sounds (fork linked at original's thread at https://forum.minetest.net/viewtopic.php?f=11&t=2807&start=275 )
add_git_mod ambience ambience https://notabug.org/tenplus1/ambience.git
# forum_url: https://forum.minetest.net/viewtopic.php?t=12189
# description: ISSUE ON 0.5.0: player halfway into ground; Adds animations to the players' head
if [ "$version_0_5_enable" != "true" ]; then
  # see https://github.com/minetest-mods/playeranim/issues/14 (fixed)
  # add_git_mod playeranim playeranim https://github.com/poikilos/playeranim.git
  add_git_mod playeranim playeranim https://github.com/minetest-mods/playeranim.git
else
  #must also set player_model_version = default_character_v3 in minetest.conf (see above for when set in subgame folder's minetest.conf)
  add_git_mod playeranim playeranim https://github.com/minetest-mods/playeranim.git "v5.0"
fi
#add_git_mod stamina stamina https://github.com/minetest-mods/stamina
remove_mod stamina
# NOTE: a skin database is at http://minetest.fensta.bplaced.net/
# bell07's 2016 (FORK of Krock's fork of dmonty's) u_skins (u_skins is a skin GUI that works with unified_inventory, whereas other skin GUIs often use inventory++)
# Krock's is outdated and has remaining bugs such as in updater: wget https://github.com/SmallJoker/minetest-u_skinsdb/archive/master.zip
# bell07's no longer exists
# wget https://github.com/bell07/minetest-u_skinsdb/archive/master.zip
# add_git_mod u_skins minetest-u_skinsdb https://github.com/dmonty2/minetest-u_skinsdb.git
# add_git_mod skinsdb minetest-u_skinsdb https://github.com/dmonty2/minetest-u_skinsdb.git
# forked and is now a part of minetest-mods thanks to bell07
MATCHING_MODS_BEFORE="`ls $MT_MYGAME_MODS_PATH | grep skin`"
remove_mod u_skinsdb
remove_mod u_skins
PATCH_SKINS_MOD_NAME="skinsdb"  # used further down too!
add_git_mod $PATCH_SKINS_MOD_NAME skinsdb https://github.com/minetest-mods/skinsdb.git
if [ ! -z "$MATCHING_MODS_BEFORE" ]; then
  echo "Removed $MATCHING_MODS_BEFORE then installed $PATCH_SKINS_MOD_NAME (this output is shown on purpose)"
fi
# Update skins database (WARNING: skin numbering affects chosen player skin):
# (jq is a json processor, required for the updater bash script:)
# sudo apt -y install jq
# cd "$MTMOD_DEST_PATH"
# cd u_skins  #bell07's version is a mod, not a modpack
# cd updater
# NOTE:
# Only download entire skins database if you
# REALLY, REALLY MEAN IT:
# ./update_skins_db.sh
# (note, bell07 has the fixed bash script, but the python3 script is still bugged as of 2016-01-29, and includes a .NET assembly that seems to only work for Windows (has meta directory not found error on mono for Linux)
# PATCH FURTHER DOWN WILL REMOVE EXISTING SKINS AND ONLY ADD EnlivenMinetest skins from patches folder
# woodcutting: sneek click to start auto-harvest tree, sneak again to cancel
add_git_mod woodcutting woodcutting https://github.com/minetest-mods/woodcutting.git
#endregion PLAYER UX MODS
add_git_mod homedecor_ua homedecor_ua https://github.com/poikilos/homedecor_ua.git


echo
echo
echo
if [ -d "$PATCHES_PATH" ]; then
  echo "adding the following necessary integration mods:"
  ls $PATCHES_PATH/mods-integration/
  sudo cp -R $PATCHES_PATH/mods-integration/* "$MT_MYGAME_MODS_PATH/"
  echo
  echo "adding the following multiplayer mods:"
  ls $PATCHES_PATH/mods-multiplayer/
  sudo cp -R $PATCHES_PATH/mods-multiplayer/* "$MT_MYGAME_MODS_PATH/"
  echo "adding non-manual patches to subgame (vs minetest_game and downloaded mods):"
  echo "patching $MT_MYGAME_DIR (files only, so 'omitting directory' warnings are ok)..."
  sudo cp -f $PATCHES_PATH/subgame/* "$MT_MYGAME_DIR/"
  echo "patching $MT_MYGAME_DIR (files only, so 'omitting directory' warnings are ok)..."
  sudo cp -f $PATCHES_PATH/subgame/menu/* "$MT_MYGAME_DIR/menu/"
  echo "patching $MT_MYGAME_DIR (files only, so 'omitting directory' warnings are ok)..."
  sudo cp -f $PATCHES_PATH/subgame/mods/mobs/textures/* "$MT_MYGAME_DIR/mods/mobs/textures/"
  echo "patching $MT_MYGAME_DIR (files only, so 'omitting directory' warnings are ok)..."
  sudo cp -f $PATCHES_PATH/subgame/mods/mobs_monster/textures/* "$MT_MYGAME_DIR/mods/mobs_monster/textures/"

# REMOVE EXISTING SKINS AND ONLY ADD poikilos skins:
MTMOD_DEST_PATH=$MT_MYGAME_MODS_PATH/$PATCH_SKINS_MOD_NAME
SUB_NAME="textures"  # include u_skins since u_skins/u_skins IS THE MOD in the modpack
SUB_PATH="$MTMOD_DEST_PATH/$SUB_NAME"
if [ -d "$SUB_PATH" ]; then
  echo "removing original $SUB_PATH/character_*..."
  rm -Rf $SUB_PATH/character_*  # cannot have quotes if using wildcards
fi
sudo cp -f $PATCHES_PATH/mods-multiplayer/$PATCH_SKINS_MOD_NAME/$SUB_NAME/* "$SUB_PATH"
if [ ! -d "$SUB_PATH" ]; then
  echo "ERROR: failed to install poikilos's skins to $SUB_PATH, so cannot continue." > $err_txt
  cat $err_txt
  echo "  press Ctrl C to cancel ENLIVEN install or this terminal will close..."
  sleep 1
  echo " 3..."
  sleep 1
  echo " 2..."
  sleep 1
  echo " 1..."
  sleep 1
  exit 1
else
  echo "installed poikilos's skins to $SUB_PATH"
fi
SUB_NAME="meta"  # include u_skins since u_skins/u_skins IS THE MOD in the modpack
SUB_PATH="$MTMOD_DEST_PATH/$SUB_NAME"
if [ -d "$SUB_PATH" ]; then
  echo "removing original $SUB_PATH/character_*..."
  rm -Rf $SUB_PATH/character_*  # cannot have quotes if using wildcards
fi
sudo cp -f $PATCHES_PATH/mods-multiplayer/$PATCH_SKINS_MOD_NAME/$SUB_NAME/* "$SUB_PATH"
if [ ! -d "$SUB_PATH" ]; then
  echo "ERROR: failed to install poikilos's skins to $SUB_PATH, so cannot continue." > $err_txt
  cat $err_txt
  echo "  press Ctrl C to cancel ENLIVEN install or this terminal will close..."
  sleep 1
  echo " 3..."
  sleep 1
  echo " 2..."
  sleep 1
  echo " 1..."
  sleep 1
  exit 1
else
  echo "installed metadata for poikilos's skins to $SUB_PATH"
fi



  echo "mods affected: mobs mobs_monsters $PATCH_SKINS_MOD_NAME"
  # poikilos bones PR was merged with minetest_game, so below is not needed
  #PATCHED_FLAG=""
  #BASIS_PATH=$PATCHES_PATH/subgame-basis/mods/bones/init.lua
  #MODIFIED_PATH=$PATCHES_PATH/subgame/mods/bones/init.lua
  #MTMOD_DEST_NAME=bones
  #MTMOD_DEST_PATH=$MT_MYGAME_MODS_PATH/bones
  #TARGET_PATH=$MTMOD_DEST_PATH/init.lua
  #TRY_DIFF="`diff $BASIS_PATH $TARGET_PATH`"
  #if [ -z "$TRY_DIFF" ]; then
  #  sudo cp -f $MODIFIED_PATH "$MT_MYGAME_DIR/mods/bones/"
  #  echo "done attempting to patch $MTMOD_DEST_PATH/ with $MODIFIED_PATH"
  #else
  #  BASIS_PATH=$PATCHES_PATH/subgame-basis/mods/bones/init-0.5.0-dev.lua
  #  MODIFIED_PATH=$PATCHES_PATH/subgame/mods/bones/init-0.5.0-dev.lua
  #  TRY_DIFF="`diff $BASIS_PATH $TARGET_PATH`"
  #  if [ -z "$TRY_DIFF" ]; then
  #    sudo cp -f $MODIFIED_PATH "$MT_MYGAME_DIR/mods/bones/init.lua"
  #    echo "patched $MT_MYGAME_DIR/mods/bones/init.lua"
  #  else
  #    TRY_DONE_DIFF="`diff $MODIFIED_PATH $TARGET_PATH`"
  #    echo "ALREADY patched $MTMOD_DEST_NAME with $MODIFIED_PATH."
  #  fi
  #fi
  #homedecor: see homedecor_ua (underage) instead ABOVE
  #BASIS_PATH=$PATCHES_PATH/subgame-basis/mods/homedecor_modpack/homedecor/gastronomy.lua
  #MODIFIED_PATH=$PATCHES_PATH/subgame/mods/homedecor_modpack/homedecor/gastronomy.lua
  #TARGET_PATH=$MT_MYGAME_MODS_PATH/homedecor_modpack/homedecor/gastronomy.lua
  #MTMOD_DEST_NAME=homedecor_modpack
  #MTMOD_DEST_PATH=$MT_MYGAME_MODS_PATH/homedecor_modpack/homedecor
  #TRY_DIFF="`diff $BASIS_PATH $TARGET_PATH`"
  #if [ -z "$TRY_DIFF" ]; then
  #  sudo cp -f $MODIFIED_PATH "$MTMOD_DEST_PATH/"
  #  echo "done attempting to patch $MTMOD_DEST_PATH/"
  #else
  #  if [ -z `diff $MODIFIED_PATH $TARGET_PATH` ];  then
  #    echo "ALREADY patched $TARGET_PATH with $MODIFIED_PATH"
  #  else
  #    echo "FAILED to patch $MTMOD_DEST_NAME since $TARGET_PATH differs from known version."
  #    sleep 4
  #  fi
  #fi
  #BASIS_PATH=$PATCHES_PATH/subgame-basis/mods/homedecor_modpack/homedecor/crafts.lua
  #MODIFIED_PATH=$PATCHES_PATH/subgame/mods/homedecor_modpack/homedecor/crafts.lua
  #TARGET_PATH=$MT_MYGAME_MODS_PATH/homedecor_modpack/homedecor/crafts.lua
  #MTMOD_DEST_NAME=homedecor_modpack
  #TRY_DIFF="`diff $BASIS_PATH $TARGET_PATH`"
  #if [ -z "$TRY_DIFF" ]; then
  #  sudo cp -f $MODIFIED_PATH "$MTMOD_DEST_PATH/"
  #  echo "done attempting to patch $MTMOD_DEST_PATH/"
  #else
  #  if [ -z `diff $MODIFIED_PATH $TARGET_PATH` ];  then
  #    echo "ALREADY patched $TARGET_PATH with $MODIFIED_PATH"
  #  else
  #    echo "FAILED to patch $MTMOD_DEST_NAME since $TARGET_PATH differs from known version."
  #    sleep 4
  #  fi
  #fi
  #if [ -d "$PATCHES_PATH/subgame/mods/homedecor_modpack/homedecor/models" ]; then
  #  # deprecated, but copy in case gets un-deprecated
  #  cp -f $PATCHES_PATH/subgame/mods/homedecor_modpack/homedecor/models/* "$MTMOD_DEST_PATH/models/"
  #fi
  # NOTE: quotes don't work with wildcard
  #cp -f $PATCHES_PATH/subgame/mods/homedecor_modpack/homedecor/textures/* "$MTMOD_DEST_PATH/textures/"
  echo "# not recommended:"
  echo "sudo cp -Rf $PATCHES_PATH/mods-stopgap/* $MT_MYGAME_MODS_PATH/"
  #echo "sudo rm -Rf $MT_MYGAME_MODS_PATH/1.nonworking  # leftovers from deprecated ENLIVEN installer"
else
  echo "did not find $PATCHES_PATH, so skipped automatic patching which is partially implemented"
fi
echo
if [ "$version_0_5_enable" != "true" ]; then
  echo "# remove not available on 0.4.16 stable (is only avail on 0.4.16-dev or higher)"
  sudo rm -Rf $MT_MYGAME_MODS_PATH/worldedit/worldedit_brush
else
  if [ -d "$MT_MYGAME_MODS_PATH/worldedit/worldedit_brush" ]; then
    echo "worldedit_brush (minetest 0.5+ only) is enabled."
  fi
fi
echo
echo
echo
echo "#### $WORLD_MT_PATH: ####"
cat "$WORLD_MT_PATH"
echo "### end $WORLD_MT_PATH ##"
echo ""
echo ""
echo ""
##echo "Remember, if you are using Better HUD + Hunger, add the values for the new meat to hunger.lua"
##echo "--see <https://forum.minetest.net/viewtopic.php?f=11&t=9917&hilit=mobs>"
#echo "NOTE: hud_hunger/hunger/food.lua now comes with values for food from mobs."
##hud_hunger now includes mobs food (see /usr/local/share/minetest/games/enliven/mods/hud_hunger/hunger/food.lua )
echo ""
echo "NOW MAKE SURE YOU EDIT $MT_MYGAME_MODS_PATH/protector/init.lua near line 325 to block comment ( --[[ then afterward --]]) the on_rightclick registration (since protection block right-clicked by its owner crashes server)"
echo "Then make sure you login, REMEMBERING to put a password in second box, then logout then:"
echo "  nano $MT_MYWORLD_DIR/players/username where username is YOUR username, give yourself the following permissions to edit areas, edit protector blocks (and other protector nodes), and do other things: areas,delprotect,home,noclip,fly,rollback,settime,teleport,bring,fast,password,give,ban,privs,kick,worldedit"
echo "  bring: allows to you teleport other players"
echo "  ban: allows /ban ip and /unban ip (and /whitelist add player and /whitelist remove player commands if whitelist mod is installed)"
echo "  kick: allows /kick player"
echo "  privs: allows grant and revoke commands"
echo "  delprotect: circumvents protector blocks, including allowing removing them"
echo "  invhack: editing player inventories as moderator"
echo ""
echo "  * for invhack, remember to do: /giveme invhack:tool"
echo "  * uncomment columns in lapis mod"
echo "  * Make sure client (server done already above) minetest.conf has secure.trusted_mods = advanced_npc"
#echo "  * Make sure writable minetest conf was successfully written"
#echo "    over $MT_MYGAME_DIR/minetest.conf with (NOTE: protector_drop is deprecated):"
echo "protector_radius = 7"
echo "protector_pvp = true"
echo "protector_pvp_spawn = 10"
echo "protector_drop = false"
echo "protector_hurt = 3"
echo ""
echo "default_privs = interact,shout,home"
echo "max_users = 50"
echo "motd = \"Actions and chat messages are logged. Visit fcacloud.com/minetest for recipes and live map.\""
echo "disallow_empty_passwords = true"
echo ""
echo "#more minetest.conf settings for hbsprint can be found at https://github.com/minetest-mods/hbsprint/blob/master/settingtypes.txt"
echo "#not all settings can be changed in this minetest.conf (see minetest.conf.example in THIS folder)"
echo "#some settings can only be changed in client's local copy of minetest.conf (see or login scripts in network)"
if [ "$version_0_5_enable" = "true" ]; then
  echo "The 0.5 version of mods was installed."
else
  echo "The non-0.5 version of mods was installed (if you have installed a development version of minetest to /usr/share such as via an AUR package, you must instead run:"
  echo "./game-install-ENLIVEN version_0_5_enable"
fi
echo "(used $MT_MINETEST_GAME_PATH as base)"
echo "spawners_enable: $spawners_enable"
echo
echo "As for world.mt, the following WORLD_MT_PATH was used: $WORLD_MT_PATH"
echo "  content:"
cat "$WORLD_MT_PATH"
echo
echo

if [ -f "`command -v blender`" ]; then
  BLENDER_CURRENT_VERSION=`blender --version | cut -d " " -f 2`
  if [ ! -f "" ]; then
    cd ~
    if [ ! -d Downloads ]; then
      mkdir Downloads
    fi
    cd Downloads
    git clone https://github.com/minetest/B3DExport.git
    echo "WARNING: you have to manually install $HOME/Downloads/B3DExport/B3DExport.py using Blender's File Menu, User Preferences, Add-ons, 'Install Add-on from File...', press OK, then check the 'Import-Export B3D' box in the Add-ons list, then Save User Settings"
    sleep 3
    cd
  fi
fi
