#!/bin/bash
echo "functionality of this script is replaced by scripts in /webapp/"
exit 1
src=WIP/ENLIVEN
if [ ! -d "$src" ]; then
    echo "ERROR: missing $src"
    exit 1
fi

dst="$HOME/EnlivenMinetest/webapp/linux-minetest-kit/minetest/games"
echo "transferring to $dst..."
rsync -rt WIP/ENLIVEN $dst
#OLD: dst="192.168.1.5:/home/owner/git/EnlivenMinetest/webapp/linux-minetest-kit/minetest/games"
dst="192.168.1.5:$HOME/minetest/games"
echo "transferring to $dst..."
rsync -rt WIP/ENLIVEN $dst
echo "Done."
