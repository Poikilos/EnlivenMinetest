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
    echo "Compiling via perl..."
    perl mtcompile-program.pl build --server >& program.log
else
    # NOTE: no pl in $extracted_name, assuming bash:
    echo "Compiling via bash..."
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
    echo "name = ENLIVEN" > "$HOME/games/ENLIVEN/game.conf"
else
    mod_name=coderbuild
    echo "updating $mod_name..."
    rsync -rt "$flag_dir/mods/$mod_name" "$HOME/games/ENLIVEN/mods"
    mod_name=codercore
    echo "updating $mod_name..."
    rsync -rt "$flag_dir/mods/$mod_name" "$HOME/games/ENLIVEN/mods"
    mod_name=coderedit
    echo "updating $mod_name..."
    rsync -rt "$flag_dir/mods/$mod_name" "$HOME/games/ENLIVEN/mods"
    mod_name=coderfood
    echo "updating $mod_name..."
    rsync -rt "$flag_dir/mods/$mod_name" "$HOME/games/ENLIVEN/mods"
    mod_name=codermobs
    echo "updating $mod_name..."
    rsync -rt "$flag_dir/mods/$mod_name" "$HOME/games/ENLIVEN/mods"
    mod_name=decorpack
    echo "updating $mod_name..."
    rsync -rt "$flag_dir/mods/$mod_name" "$HOME/games/ENLIVEN/mods"
    mod_name=mtmachines
    echo "updating $mod_name..."
    rsync -rt "$flag_dir/mods/$mod_name" "$HOME/games/ENLIVEN/mods"
    # cp -f "$flag_dir/mods/LICENSE" "$HOME/games/ENLIVEN/mods/LICENSE"
fi
