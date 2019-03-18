#!/bin/sh
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
MT_MYGAME_MODDIR=$MT_MYGAME_DIR/mods
MT_MYWORLD_NAME=FCAGameAWorld
MT_MYWORLD_DIR=$HOME/.minetest/worlds/$MT_MYWORLD_NAME
#sudo mkdir "$MT_MYGAME_DIR"

if [ -d "$MT_MYGAME_DIR/mods" ]; then
	cd "$MT_MYGAME_DIR/mods"
	MT_VANILLA_PATH="$USR_SHARE_MINETEST/games/minetest_game"

	MT_VANILLA_MODS_PATH=$MT_VANILLA_PATH/mods
	if [ ! -d "$MT_VANILLA_MODS_PATH" ]; then
		echo "missing $MT_VANILLA_MODS_PATH"
	else
	ls "$MT_VANILLA_MODS_PATH" | xargs rm -Rf
	#ls "$MT_VANILLA_MODS_PATH" | xargs echo
	fi
fi
