#!/bin/bash
echo
echo

customDie() {
    echo
    echo "ERROR:"
    echo "$1"
    echo
    echo
}

if [ ! -f deer.lua ]; then
  customDie "No deer.lua, so can't patch."
fi
my_bucket_game=$HOME/minetest/games/Bucket_Game
my_codermobs_codermobs=$my_bucket_game/mods/codermobs/codermobs
my_codermobs_init=$my_codermobs_codermobs/init.lua
if [ ! -f "$my_codermobs_init" ]; then
    customDie "$my_codermobs_init does not exist."
fi
echo "* patching $my_codermobs_init..."
if [ -z "`cat $my_codermobs_init | grep deer.lua`" ]; then
    echo 'dofile (mp .. "/deer.lua"          )' >> "$my_codermobs_init"
else
    echo "  Your codermobs/codermobs/init.lua already loads deer.lua."
fi
if [ -f "$my_codermobs_codermobs/deer.lua" ]; then
    echo "* removing old $my_codermobs_codermobs/deer.lua..."
    rm $my_codermobs_codermobs/deer.lua || customDie "Cannot remove old $my_codermobs_codermobs/deer.lua"
fi
echo "* copying to $my_codermobs_codermobs/deer.lua..."
cp deer.lua "$my_codermobs_codermobs/" || customDie "Cannot copy to $my_codermobs_codermobs/deer.lua"
echo "* copying over $my_codermobs_codermobs/textures/..."
cp textures/* "$my_codermobs_codermobs/textures/" || customDie "Cannot copy to $my_codermobs_codermobs/textures/"
echo "* copying over $my_codermobs_codermobs/models/..."
cp models/* "$my_codermobs_codermobs/models/" || customDie "Cannot copy to $my_codermobs_codermobs/textures/"
echo "Done."
echo
echo

