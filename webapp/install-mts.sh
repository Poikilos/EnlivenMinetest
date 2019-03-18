#!/bin/bash
extracted_name=linux-minetest-kit
flag_dir="$extracted_name/mtsrc"
if [ ! -d "$flag_dir" ]; then
    echo "ERROR: missing $flag_dir"
    exit 1
fi
cd "$extracted_name"
flag_file="minetest/bin/minetestserver"
if [ -f "$flag_file" ]; then
    rm -f "$flag_file"
fi
if [ -f "$flag_file" ]; then
    echo "ERROR: Nothing done since can't remove old '$flag_file'"
    exit 1
fi
if [ -f "mtcompile-program.pl" ]; then
    # perl mtcompile-program.pl build >& program.log
    perl mtcompile-program.pl build --server >& program.log
else
    # NOTE: no pl in $extracted_name, assuming bash:
    bash -e mtcompile-program.sh build >& program.log
fi
if [ ! -f "$flag_file" ]; then
    echo "ERROR: Build did not complete--missing '$flag_file'"
    exit 1
fi
flag_file="$HOME/minetest/bin/minetestserver"
if [ -f "$flag_file" ]; then
    mv -f "$flag_file" "$flag_file.bak"
fi
if [ -f "$flag_file" ]; then
    echo "ERROR: not complete since can't move old '$flag_file'"
    exit 1
fi
rsync -rt minetest $HOME
if [ ! -f "$flag_file" ]; then
    echo "ERROR: not complete--couldn't create '$flag_file'"
    exit 1
fi
flag_dir="$HOME/games/Bucket_Game"
if [ ! -d "$flag_dir" ]; then
    echo "ERROR: missing $flag_dir"
    exit 1
fi
if [ ! -d "$HOME/games/ENLIVEN" ]; then
    cp -R "$flag_dir" "$HOME/games/ENLIVEN"
    echo
else
    rsync -rt "$flag_dir/mods/coderbuild/" "$HOME/games/ENLIVEN/mods/coderbuild"
    rsync -rt "$flag_dir/mods/codercore/" "$HOME/games/ENLIVEN/mods/codercore"
    rsync -rt "$flag_dir/mods/coderedit/" "$HOME/games/ENLIVEN/mods/coderedit"
    rsync -rt "$flag_dir/mods/coderfood/" "$HOME/games/ENLIVEN/mods/coderfood"
    rsync -rt "$flag_dir/mods/codermobs/" "$HOME/games/ENLIVEN/mods/codermobs"
    rsync -rt "$flag_dir/mods/decorpack/" "$HOME/games/ENLIVEN/mods/decorpack"
    rsync -rt "$flag_dir/mods/mtmachines/" "$HOME/games/ENLIVEN/mods/mtmachines"
    # cp -f "$flag_dir/mods/LICENSE" "$HOME/games/ENLIVEN/mods/LICENSE"
fi
