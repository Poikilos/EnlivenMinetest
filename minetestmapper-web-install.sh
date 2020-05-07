#!/bin/bash

customExit() {
    echo
    echo
    echo "ERROR:"
    echo "$1"
    echo
    echo
    exit 1
}

_REPO_NAME=minetestmapper
if [ -z "$_INSTALL_PATH" ]; then
    _INSTALL_PATH="$HOME/$_REPO_NAME"
fi
_EXE_NAME=minetestmapper
_REPO_URL="https://github.com/minetest/$_REPO_NAME.git"
if [ -z "$REPOS_PATH" ]; then
    REPOS_PATH=~/Downloads/git
fi
mkdir -p $REPOS_PATH

REPO_PATH="$REPOS_PATH/$_REPO_NAME"

if [ ! -d "$REPOS_PATH" ]; then
    mkdir -p "$REPOS_PATH" || customExit "mkdir -p \"$REPOS_PATH\" failed."
fi

cd "$REPOS_PATH" || customExit "cd \"$REPOS_PATH\" failed."
if [ -d "$REPO_PATH" ]; then
    cd "$REPO_PATH" || customExit "cd \"$REPO_PATH\" failed."
    git pull || customExit "git pull failed in `pwd`."
else
    git clone "$_REPO_URL" "$REPO_PATH" || customExit "git clone \"$_REPO_URL\" \"$REPO_PATH\" failed."
fi
echo "* compiling in `pwd`..."
cmake . -DENABLE_LEVELDB=1 -DENABLE_POSTGRES=1 -DENABLE_REDIS=1 || customExit "cmake . failed in `pwd`."
make -j$(nproc) || customExit "make failed in `pwd`."
_EXE_PATH="`pwd`/$_EXE_NAME"
if [ -f "$_EXE_PATH" ]; then
    echo "* finished compiling \"$_EXE_PATH\""
    mkdir -p "$_INSTALL_PATH" || "mkdir -p \"$_INSTALL_PATH\" failed."
    #cp "$_EXE_PATH" "$_INSTALL_PATH" || "cp \"$_EXE_PATH\" \"$_INSTALL_PATH\" failed."
    rsync -rtu "`pwd`/" "$_INSTALL_PATH" || "rsync -rtu \"`pwd`/\" \"$_INSTALL_PATH\" failed."
    # -u: skip files that are newer on the receiver
    EXE_DEST_PATH="$_INSTALL_PATH/$_EXE_NAME"
    if [ -f "$EXE_DEST_PATH" ]; then
        echo "* installed \"$EXE_DEST_PATH\""
    else
        customExit "* installing \"$EXE_DEST_PATH\" failed."
    fi
else
    echo "* finished compiling in `pwd` (but $_EXE_PATH was not detected)"
fi
