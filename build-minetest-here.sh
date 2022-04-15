#!/bin/bash
customExit(){
    echo "$1"
    exit 1
}
#mybuild="minetest-built"
#if [ ! -d $mybuild ]; then
    # mkdir $mybuild
    # echo
#fi
# cd $mybuild || customExit "$0: cd build failed in '`pwd`'."

for var in "$@"
do
    if [ "@$var" = "@--run-in-place" ]; then
        RUN_IN_PLACE=true
    fi
done

usage(){
cat <<END
Set RUN_IN_PLACE to true:
$0 --run-in-place
# or
# env RUN_IN_PLACE=1 $0
END
}

printf "* detecting EnlivenMinetest..."
if [ -z "$ENLIVEN_REPO" ]; then
    try_default_enliven_repo="$HOME/git/EnlivenMinetest"
    for try_enliven_repo in "$HOME/Downloads/poikilos/EnlivenMinetest" "$HOME/Downloads/EnlivenMinetest" "$try_default_enliven_repo"
    do
        if [ -d "$try_enliven_repo" ]; then
            ENLIVEN_REPO="$try_enliven_repo"
            echo "Detected ENLIVEN_REPO=\"$try_enliven_repo\""
        else
            echo "Tried \"$try_enliven_repo\" (not found)"
        fi
    done
fi
source mtbuild.rc
if [ $? -ne 0 ]; then
    printf "* trying \"$ENLIVEN_REPO/mtbuild.rc\"..."
    source "$ENLIVEN_REPO/mtbuild.rc"
    if [ $? -ne 0 ]; then
        echo "FAILED"
        echo "Error:"
        echo "source mtbuild.rc failed. Try adding it to the path or $try_default_enliven_repo (or set ENLIVEN_REPO)"
        exit 1
    else
        echo "OK"
    fi
fi


if [ -z "$KEEP_MAKE" ]; then
    KEEP_MAKE=0
fi
INSTALL_DEPS=
if [ ! -f "`command -v cmake`" ]; then
    INSTALL_DEPS="$INSTALL_DEPS cmake"
fi
if [ ! -f "`command -v make`" ]; then
    INSTALL_DEPS="$INSTALL_DEPS make"
fi

if [ ! -z "$INSTALL_DEPS" ]; then
    echo "* missing $INSTALL_DEPS"
    if [ ! -z "$REFRESH_OS_INSTALLER_CMD" ]; then
        echo "  * Running '$REFRESH_OS_INSTALLER_CMD'"
    fi
    echo "  * Running '$DEPS_INSTALL'..."
    $DEPS_INSTALL
    if [ $? -ne 0 ]; then
        echo "Installing dependencies failed."
        exit 1
    fi
fi

if [ -f bin/minetest ]; then
    if [ "$KEEP_MAKE" != "1" ]; then
        echo "* [build-minetest-here.sh] running 'make clean' in `pwd`..."
        make clean || customExit "$0: make clean failed in '`pwd`'."
    else
        echo "* [build-minetest-here.sh] keeping existing intermediate build files in `pwd` (KEEP_MAKE=$KEEP_MAKE)..."
    fi
else
    echo "* [build-minetest-here.sh] There is no bin/minetest in `pwd`."
fi
# echo "BREAKPOINT 20s..."
# sleep 20
if [ -z "$RUN_IN_PLACE" ]; then
    RUN_IN_PLACE=0
fi

if [ "@$RUN_IN_PLACE" = "@true" ]; then
    RUN_IN_PLACE=1
elif [ "@$RUN_IN_PLACE" = "@on" ]; then
    RUN_IN_PLACE=1
elif [ "@$RUN_IN_PLACE" = "@yes" ]; then
    RUN_IN_PLACE=1
elif [ "@$RUN_IN_PLACE" = "@1" ]; then
    RUN_IN_PLACE=1
elif [ "@$RUN_IN_PLACE" = "@off" ]; then
    RUN_IN_PLACE=0
elif [ "@$RUN_IN_PLACE" = "@false" ]; then
    RUN_IN_PLACE=0
elif [ "@$RUN_IN_PLACE" = "@no" ]; then
    RUN_IN_PLACE=0
elif [ "@$RUN_IN_PLACE" = "@0" ]; then
    RUN_IN_PLACE=0
else
    echo "[build-minetest-here.sh] ERROR: There is an unknown value for RUN_IN_PLACE: '$RUN_IN_PLACE'"
    exit 1
fi
echo
echo "RUN_IN_PLACE=$RUN_IN_PLACE"
if [ "$RUN_IN_PLACE" = "0" ]; then
    echo "^ To change this, press Ctrl+C and use:"
    usage
    echo
    echo "3..."
    sleep 1
    echo "2..."
    sleep 1
    echo "1..."
    sleep 1
fi

if [ ! -z "$BUILD_CLIENT" ]; then
    client_line="-DBUILD_CLIENT=$BUILD_CLIENT"
fi
if [ ! -z "$BUILD_SERVER" ]; then
    server_line="-DBUILD_SERVER=$BUILD_SERVER"
fi
echo "* [build-minetest-here.sh] running cmake in `pwd`..."
cmake . $server_line $client_line -DOpenGL_GL_PREFERENCE=GLVND -DENABLE_GETTEXT=1 -DENABLE_FREETYPE=1 -DENABLE_LEVELDB=1 -DENABLE_REDIS=1 -DRUN_IN_PLACE=$RUN_IN_PLACE && make -j$(grep -c processor /proc/cpuinfo)  || customExit "$0: Build failed in '`pwd`'."
if [ $? -ne 0 ]; then
    echo
    echo "cmake failed. Try:"
    echo "$DEPS_INSTALL"
fi
echo
echo "RUN_IN_PLACE=$RUN_IN_PLACE"
if [ "@$RUN_IN_PLACE" = "@1" ]; then
    echo "[build-minetest-here.sh] WARNING: do NOT run make install: -DRUN_IN_PLACE=$RUN_IN_PLACE!"
else
    echo "^ If you didn't intend for this,"
    usage
fi
echo
#/home/owner/git/EnlivenMinetest/install-minetest.sh says:
# NOTE: as long as -DRUN_IN_PLACE=off, above installs correctly without
# -DCMAKE_INSTALL_PREFIX=/usr which for some reason is used by
# https://aur.archlinux.org/minetest-git.git

