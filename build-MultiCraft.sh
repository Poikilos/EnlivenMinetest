#!/bin/bash

#two-line version:
# if [! -f CMakeLists.txt ]; then git clone https://github.com/MultiCraft/MultiCraft.git && cd MultiCraft || exit 1; fi
# cmake . -DOpenGL_GL_PREFERENCE=GLVND && make

me="$0"
OFFLINE=false
if [ "@$1" = "@--offline" ]; then
    OFFLINE=true
fi
if [ "@$2" = "@--offline" ]; then
    OFFLINE=true
fi
customDie() {
    echo
    echo
    echo "$me ERROR:"
    echo $1
    echo
    exit 1
}
dieIfOnline() {
    echo
    echo
    if [ "@$OFFLINE" = "@false" ]; then
        echo "$me ERROR:"
        echo $1
        echo
        exit 1
    else
        echo "$me WARNING:"
        echo $1
        echo
    fi
}
GIT_USER_DIR="$HOME/Downloads/git/MultiCraft"
if [ ! -d "$GIT_USER_DIR" ]; then
    mkdir -p "$GIT_USER_DIR"
fi
cd $GIT_USER_DIR || customDie "cd $GIT_USER_DIR FAILED"
goodFlagFile=MultiCraft/CMakeLists.txt
if [ -f "`which git`" ]; then
    echo "In `pwd`..."
    if [ ! -d MultiCraft ]; then
        if [ "@$OFFLINE" = "@false" ]; then
            git clone https://github.com/MultiCraft/MultiCraft.git || customDie "Cannot clone MultiCraft from `pwd`"
        fi
        cd MultiCraft || customDie "Cannot cd MultiCraft from `pwd`"
    else
        cd MultiCraft || customDie "Cannot cd MultiCraft from `pwd`"
        git pull || dieIfOnline "WARNING: Cannot pull MultiCraft from `pwd`"
    fi
else
    if [ ! -f "$goodFlagFile" ]; then
        customDie "You are missing git, and offline install is not possible without in current directory (`pwd`)"
    else
        cd MultiCraft || customDie "Cannot cd MultiCraft from `pwd`"
    fi
fi
cd games || customDie "cd games FAILED in `pwd`"
rmdir default
if [ ! -d "default" ]; then
    if [ "@$OFFLINE" = "@false" ]; then
        git clone https://github.com/MultiCraft/MultiCraft_game default || customDie "Cannot "
    else
        echo
        echo
        echo
        echo "ERROR: default is not in `pwd`--worlds cannot load without a game."
        echo
        echo
        sleep 2
    fi
else
    if [ "@$OFFLINE" = "@false" ]; then
        cd default || customDie "cd default FAILED in `pwd`"
        git pull || customDie "git pull FAILED in `pwd`"
        cd .. || customDie "cd .. FAILED in `pwd`"
    fi
fi
cd .. || customDie "cd .. FAILED in `pwd`"
srcPath=.
flag1="-DOpenGL_GL_PREFERENCE=GLVND"
echo
echo "Running cmake srcPath..."
cmake $srcPath $flag1 -DRUN_IN_PLACE=1 -DENABLE_GETTEXT=1 -DENABLE_FREETYPE=1 -DENABLE_LEVELDB=1 || customDie "cmake failed. See any messages above for more information. Run ./install-minetest-build-deps.sh if you did not."
echo
echo "Running make..."
make -j$(nproc) || customDie "make failed. See any messages above for more information. Run ./install-minetest-build-deps.sh if you did not."
if [ -f "`pwd`/bin/MultiCraft" ]; then
    echo "`pwd`/bin/MultiCraft"
else
    echo "`pwd`"
fi
if [ -d "$GIT_USER_DIR/MultiCraft-poikilos" ]; then
    rsync -rt --info=progress2 --exclude 'multicraft.conf' "$GIT_USER_DIR/MultiCraft/" "$GIT_USER_DIR/MultiCraft-poikilos"
fi
echo "Done."
