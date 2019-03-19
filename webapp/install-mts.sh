#!/bin/bash
extracted_name=linux-minetest-kit
flag_dir="$extracted_name/mtsrc"
if [ ! -d "$flag_dir" ]; then
    echo "ERROR: missing $flag_dir"
    exit 1
fi
cd "$extracted_name"
extra_options=""
if [ "@$1" = "@--client" ]; then
    extra_options="--client"
fi
flag_icon="$HOME/Desktop/org.minetest.minetest.desktop"
flag_file="minetest/bin/minetestserver"
if [ -f "$flag_icon" ]; then
    extra_options="--client"
    echo "automatically adding --client to compile since detected"
    echo "'$flag_icon'--press Ctrl C to cancel..."
    flag_file="minetest/bin/minetest"
    sleep 2
fi
#if [ -f "$flag_file" ]; then
    #rm -f "$flag_file"
#fi
#if [ -f "$flag_file" ]; then
    #echo "ERROR: Nothing done since can't remove old '$flag_file'"
    #exit 1
#fi
if [ -d minetest ]; then
    echo "using existing minetest..."
else
    if [ -f "mtcompile-program.pl" ]; then
        # perl mtcompile-program.pl build >& program.log
        echo "Compiling via perl..."
        perl mtcompile-program.pl build --server $extra_options >& program.log
    else
        # NOTE: no pl in $extracted_name, assuming bash:
        echo "Compiling via bash..."
        bash -e mtcompile-program.sh build --server $extra_options >& program.log
    fi
fi
if [ ! -f "$flag_file" ]; then
    echo "ERROR: Build did not complete--missing '$flag_file'"
    exit 1
fi
dest_flag_file="$HOME/$flag_file"
if [ -f "$dest_flag_file" ]; then
    mv -f "$dest_flag_file" "$dest_flag_file.bak"
fi
if [ -f "$dest_flag_file" ]; then
    echo "ERROR: not complete since can't move old '$dest_flag_file'"
    exit 1
fi
if [ ! -d minetest ]; then
    echo "ERROR: can't install since missing `pwd`/minetest"
    exit 1
fi
echo "Installing minetest to '$HOME'..."
rsync -rt minetest $HOME
if [ ! -f "$dest_flag_file" ]; then
    echo "ERROR: not complete--couldn't create '$dest_flag_file'"
    exit 1
fi
flag_dir="$HOME/minetest/games/Bucket_Game"
if [ ! -d "$flag_dir" ]; then
    echo "ERROR: missing $flag_dir"
    exit 1
fi
if [ ! -d "$HOME/minetest/games/ENLIVEN" ]; then
    cp -R "$flag_dir" "$HOME/minetest/games/ENLIVEN"
    echo "name = ENLIVEN" > "$HOME/minetest/games/ENLIVEN/game.conf"
else
    mod_name=coderbuild
    echo "updating $mod_name..."
    rsync -rt "$flag_dir/mods/$mod_name" "$HOME/minetest/games/ENLIVEN/mods"
    mod_name=codercore
    echo "updating $mod_name..."
    rsync -rt "$flag_dir/mods/$mod_name" "$HOME/minetest/games/ENLIVEN/mods"
    mod_name=coderedit
    echo "updating $mod_name..."
    rsync -rt "$flag_dir/mods/$mod_name" "$HOME/minetest/games/ENLIVEN/mods"
    mod_name=coderfood
    echo "updating $mod_name..."
    rsync -rt "$flag_dir/mods/$mod_name" "$HOME/minetest/games/ENLIVEN/mods"
    mod_name=codermobs
    echo "updating $mod_name..."
    rsync -rt "$flag_dir/mods/$mod_name" "$HOME/minetest/games/ENLIVEN/mods"
    mod_name=decorpack
    echo "updating $mod_name..."
    rsync -rt "$flag_dir/mods/$mod_name" "$HOME/minetest/games/ENLIVEN/mods"
    mod_name=mtmachines
    echo "updating $mod_name..."
    rsync -rt "$flag_dir/mods/$mod_name" "$HOME/minetest/games/ENLIVEN/mods"
    # cp -f "$flag_dir/mods/LICENSE" "$HOME/minetest/games/ENLIVEN/mods/LICENSE"
fi
