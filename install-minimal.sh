#!/bin/bash

customExit() {
    errorCode=1
    if [ ! -z "$2" ]; then
        errorCode="$2"
    fi
    echo
    echo "ERROR:"
    echo "$1"
    echo
    echo
    exit $errorCode
}

countDown(){
    echo "Press Ctrl-C to cancel..."
    echo "3..."
    sleep 1
    echo "2..."
    sleep 1
    echo "1..."
    sleep 1
}

echo "This will DELETE ~/minetest/games/minimal and remake it!"
countDown
#> You'll need minimum git 1.9 for this to work. Tested it myself only with 2.2.0 and 2.2.2.
#-<https://stackoverflow.com/questions/600079/how-do-i-clone-a-subdirectory-only-of-a-git-repository/52269934#52269934>
REPO_URL=https://github.com/minetest/minetest
# REPO_URL=http://git.minetest.org:3000/minetest/minetest.git
DEST_REPO=~/Downloads/git/minetest_minimal
DEST_GAMES=~/minetest/games
if [ ! -d $DEST_GAMES ]; then
    echo "ERROR: You must first install Minetest and have the $DEST_GAMES directory."
    exit 1
fi
if [ -e $DEST_GAMES/minimal ]; then
    rm $DEST_GAMES/minimal || customExit "$DEST_GAMES/minimal should be either a symlink to $DEST_REPO/games/minimal or not present, but right now it is a directory. Move or delete it then try this script again."
fi

if [ ! -d "$DEST_REPO" ]; then
    mkdir -p ~/Downloads/git \
        && git init "$DEST_REPO" \
        && cd "$DEST_REPO" \
        && git remote add origin $REPO_URL \
        && git config core.sparsecheckout true \
        && echo "games/minimal/*" >> .git/info/sparse-checkout \
        && git pull origin master
    if [ ! -d "$DEST_REPO" ]; then
        echo "ERROR: Cloning $REPO_URL did not result in $DEST_REPO."
        exit 1
    fi
else
    cd "$DEST_REPO" || customExit "cd \"$DEST_REPO\" failed."
    echo "Updating $DEST_REPO..."
    git pull origin master || echo "WARNING: git pull failed in `pwd`."
    if [ ! -d "$DEST_REPO/games/minimal" ]; then
        customExit "$DEST_REPO/games/minimal is missing."
    fi
fi
#    && rm -Rf $DEST_REPO
#    && git pull --depth=1 origin master
ln -s "$DEST_REPO/games/minimal" "$DEST_GAMES/"
