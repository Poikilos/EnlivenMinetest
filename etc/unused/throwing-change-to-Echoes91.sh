#!/bin/sh

#First make sure all folders in $HOME/.minetest are created (I am not sure whether this is required!):
# minetestserver
# Mods were found at https://forum.minetest.net/viewforum.php?f=11


# * Git version uses /home/*/minetest/games and /usr/local/share/minetest/games but the latter is used for minetestserver (minetest-server package)


#(Ubuntu 14.04 Trusty Tahr Server) folders were found using:
# cd /
# sudo find -name 'worlds' (worlds folder is in $HOME/.minetest)
# sudo find -name 'minimal' (stable build [such as 0.4.9 games folder is /usr/share/games/minetest/games, but git version games folder is /usr/local/share/minetest/games)

#NOTE: minetest mods are ALWAYS ONLY installed on server

USR_SHARE_MINETEST=/usr/share/games/minetest
#IF git version is installed:
if [ -d "/usr/local/share/minetest" ]; then
  USR_SHARE_MINETEST=/usr/local/share/minetest
fi
#UNUSED (unknown use): MT_GAMES_DIR=$HOME/.minetest/mods
#intentionally skip the slash in the following line since $USR_SHARE_MINETEST already starts with one:
MT_BACKUP_GAMES_DIR=$HOME/Backup$USR_SHARE_MINETEST/games
MT_GAMES_DIR=$USR_SHARE_MINETEST/games
MT_MYGAME_NAME=ENLIVEN
MT_MYGAME_DIR=$MT_GAMES_DIR/$MT_MYGAME_NAME
#formerly MT_MYGAME_MODDIR:
MT_MYGAME_MODS_PATH=$MT_MYGAME_DIR/mods
MT_MYWORLD_NAME=FCAGameAWorld
MT_MYWORLD_DIR=$HOME/.minetest/worlds/$MT_MYWORLD_NAME


cd "$HOME/Downloads"
MTMOD_DL_ZIP=archive.zip
MTMOD_SRC_ZIP=throwing_Echoes91.zip
MTMOD_UNZ_NAME=throwing-master-*
MTMOD_DEST_NAME=throwing
MTMOD_DEST_PATH=$MT_MYGAME_MODS_PATH/$MTMOD_DEST_NAME
if [ -d "$MTMOD_DEST_PATH" ]; then
  echo "Removing old version of throwing..."
  sudo rm -Rf $MTMOD_DEST_PATH
fi
echo "Installing Echoes91's (NOT PilzAdam's NOT Jeija's) Throwing enhanced <https://forum.minetest.net/viewtopic.php?f=11&t=11437>"
#if [ -d "$MTMOD_UNZ_NAME" ]; then
rm -Rf $MTMOD_UNZ_NAME
#fi
if [ -f "$MTMOD_DL_ZIP" ]; then
  rm "$MTMOD_DL_ZIP"
fi
if [ -f "$MTMOD_SRC_ZIP" ]; then
  rm "$MTMOD_SRC_ZIP"
fi
#wget https://github.com/PilzAdam/throwing/zipball/master
wget https://gitlab.com/echoes91/throwing/repository/archive.zip
mv $MTMOD_DL_ZIP "$MTMOD_SRC_ZIP"
unzip "$MTMOD_SRC_ZIP"
sudo mv $MTMOD_UNZ_NAME "$MTMOD_DEST_PATH"
if [ ! -d "$MTMOD_DEST_PATH" ]; then
  echo "ERROR: failed to unzip $MTMOD_DEST_PATH, so cannot continue."
  exit 1  
fi