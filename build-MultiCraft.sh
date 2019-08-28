#!/bin/bash

#two-line version:
# if [! -f CMakeLists.txt ]; then git clone https://github.com/MultiCraft/MultiCraft.git && cd MultiCraft || exit 1; fi
# cmake . -DOpenGL_GL_PREFERENCE=GLVND && make

me="$0"
customDie() {
    echo
    echo
    echo "$me ERROR:"
    echo $1
    echo
    exit 1
}
goodFlagFile=MultiCraft/CMakeLists.txt
if [ -f "`which git`" ]; then
    if [ ! -d MultiCraft ]; then
        git clone https://github.com/MultiCraft/MultiCraft.git || customDie "Cannot clone MultiCraft from `pwd`"
        cd MultiCraft || customDie "Cannot cd MultiCraft from `pwd`"
    else
        cd MultiCraft || customDie "Cannot cd MultiCraft from `pwd`"
        git pull || customDie "Cannot pull MultiCraft from `pwd`"
    fi
else
    if [ ! -f "$goodFlagFile" ]; then
        customDie "You are missing git, and offline install is not possible without in current directory (`pwd`)"
    else
        cd MultiCraft || customDie "Cannot cd MultiCraft from `pwd`"
    fi
fi
srcPath=.
flag1="-DOpenGL_GL_PREFERENCE=GLVND"
echo
echo "Running cmake srcPath..."
cmake $srcPath $flag1 || customDie "cmake failed. See any messages above for more information."
echo
echo "Running make..."
make
echo "Done."
