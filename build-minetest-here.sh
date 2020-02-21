#!/bin/bash
customDie(){
    echo "$1"
    exit 1
}
mybuild="minetest-built"
if [ ! -d $mybuild ]; then
    # mkdir $mybuild
    echo
fi
# cd $mybuild || customDie "$0: cd build failed in '`pwd`'."
if [ -f bin/minetest ]; then
    make clean || customDie "$0: make clean failed in '`pwd`'."
fi
RUN_IN_PLACE=0
cmake . -DENABLE_GETTEXT=1 -DENABLE_FREETYPE=1 -DENABLE_LEVELDB=1 -DENABLE_REDIS=1 -DRUN_IN_PLACE=$RUN_IN_PLACE && make -j$(grep -c processor /proc/cpuinfo)  || customDie "$0: Build failed in '`pwd`'."
echo
if [ "@$RUN_IN_PLACE" = "@1" ]; then
    echo "WARNING: do not do make install with -DRUN_IN_PLACE=$RUN_IN_PLACE!"
fi
if [ "@$RUN_IN_PLACE" = "@true" ]; then
    echo "WARNING: do not do make install with -DRUN_IN_PLACE=$RUN_IN_PLACE!"
fi
if [ "@$RUN_IN_PLACE" = "@on" ]; then
    echo "WARNING: do not do make install with -DRUN_IN_PLACE=$RUN_IN_PLACE!"
fi
echo
#/home/owner/git/EnlivenMinetest/install-minetest.sh says:
# NOTE: as long as -DRUN_IN_PLACE=off, above installs correctly without
# -DCMAKE_INSTALL_PREFIX=/usr which for some reason is used by
# https://aur.archlinux.org/minetest-git.git

