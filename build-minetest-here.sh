#!/bin/bash
if [ -f bin/minetest ]; then
    make clean
fi
cmake . -DENABLE_GETTEXT=1 -DENABLE_FREETYPE=1 -DENABLE_LEVELDB=1 -DENABLE_REDIS=1 -DRUN_IN_PLACE=1 && make -j$(grep -c processor /proc/cpuinfo)
