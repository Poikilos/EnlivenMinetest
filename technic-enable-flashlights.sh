#!/bin/sh


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
  echo "ERROR: Nothing done since missing minetestenv.rc (must be in same directory). Press Ctrl-C or allow this session to exit."
  sleep 5
  exit 1
fi
source minetestenv.rc
#endregion paste this part into terminal to get some great environment variables


#enable flashlights by replacing
#enable_flashlight = "false",
#with
#enable_flashlight = "true",
#such as in: /usr/local/share/minetest/games/ENLIVEN/mods/technic/technic/config.lua
patch_dest="$MT_MINETEST_GAME_PATH/mods/technic/technic/config.lua"
if [ -f "$patch_dest" ]; then
  sudo sed -i '/enable_flashlight/c\\tenable_flashlight = "true",' "$patch_dest"
else
  echo "ERROR: cannot enable flashlight since missing $patch_dest"
fi
#as per Todd's answer on https://stackoverflow.com/questions/11245144/replace-whole-line-containing-a-string-using-sed
