#!/bin/sh
USR_SHARE_MINETEST=/usr/share/games/minetest
#IF git version is installed:
if [ -d "/usr/local/share/minetest" ];
then
USR_SHARE_MINETEST=/usr/local/share/minetest
fi
#UNUSED (unknown use): MT_GAMES_DIR=$HOME/.minetest/mods
#intentionally skip the slash in the following line since $USR_SHARE_MINETEST already starts with one:

MT_BACKUP_GAMES_DIR=$HOME/Backup$USR_SHARE_MINETEST/games
MT_GAMES_DIR=$USR_SHARE_MINETEST/games
MT_MYGAME_NAME=ENLIVEN
MT_MYGAME_DIR=$MT_GAMES_DIR/$MT_MYGAME_NAME
MT_MYGAME_MODDIR=$MT_MYGAME_DIR/mods
MT_MYWORLD_NAME=FCAGameAWorld
MT_MYWORLD_DIR=$HOME/.minetest/worlds/$MT_MYWORLD_NAME
if [ ! -d "$MT_MYGAME_DIR" ]; then
	sudo mkdir "$MT_MYGAME_DIR"
fi


mtredisalize                               \
  -host=localhost                          \
  -interleaved=true                        \
  -change-url=http://localhost:8808/update \
  -change-duration=10s                     \
  $MT_MYWORLD_DIR/map.db

