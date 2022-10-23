#!/bin/bash
EX_PATH="`realpath .`"
EX_NAME="`basename $EX_PATH`"
REPACK_TMP=~/tmp
mkdir -p "$REPACK_TMP"
REPACK_TMP_MT="$REPACK_TMP/minetest"

SRC_GAMES="$EX_PATH/games"
DST_GAMES="$REPACK_TMP_MT/games"
SRC_BIN="$EX_PATH/bin/minetest"

if [ ! -f "$SRC_BIN" ]; then
    printf "Error: You must run this from a compiled minetest directory (There is no file '$SRC_BIN'"
    if [ -d "$SRC_BIN" ]; then
        echo ": It is a directory)."
    else
        echo ")."
    fi
    exit 5
fi

verb="making"
if [ -d "$REPACK_TMP_MT" ]; then
    verb="remaking"
fi
echo "* $verb $REPACK_TMP_MT from parts of $EX_PATH..."
rsync \
    -rtv \
    --delete \
    --exclude mods \
    --exclude worlds \
    --exclude games \
    --exclude cache \
    --exclude ENLIVEN \
    --exclude minetest.ENLIVEN \
    --exclude minetest.conf.zip \
    --exclude tmp \
    --exclude CenterOfTheSun.blank \
    --exclude deploy.sh \
    --exclude bin/AMHI \
    --exclude "bin/*.txt" \
    --exclude "bin/*screenshot*" \
    "$EX_PATH/" \
    "$REPACK_TMP_MT" \
;
code=$?
if [ $code -ne 0 ]; then exit $code; fi

cd "$REPACK_TMP"
code=$?
if [ $code -ne 0 ]; then exit $code; fi



add_game(){
    GAME_ID="$1"
    if [ "x$GAME_ID" = "x" ]; then
        echo "[$0] [add_game] Error: You must specify a GAME_ID."
        exit 2
    fi
    if [ "x$SRC_GAMES" = "x" ]; then
        echo "[$0] [add_game] Error: SRC_GAMES is blank."
        exit 3
    fi
    if [ "x$DST_GAMES" = "x" ]; then
        echo "[$0] [add_game] Error: DST_GAMES is blank."
        exit 4
    fi
    SRC_GAME="$SRC_GAMES/$GAME_ID"
    DST_GAME="$DST_GAMES/$GAME_ID"
    if [ ! -d "$DST_GAMES" ]; then mkdir -p "$DST_GAMES"; fi
    if [ -d "$SRC_GAME" ]; then
        printf "* adding $SRC_GAME as $DST_GAME..."
        rsync -rtv --delete "$SRC_GAME/" "$DST_GAME"
        code=$?
        if [ $code -ne 0 ]; then
            echo "  FAILED"
            exit $code
        else
            echo "  OK"
            echo
            echo
            echo
            echo
        fi
    else
        echo "* There is nothing to do for $GAME_ID (There is no '$SRC_GAME')."
    fi
}

if [ -d "$SRC_GAMES/bucket_game" ]; then
    add_game bucket_game
elif [ -d "$SRC_GAMES/Bucket_Game" ]; then
    add_game Bucket_Game
else
    echo "* There is nothing to do for bucket_game (There is no bucket_game nor Bucket_Game in '$SRC_GAMES')."
fi

add_game amhi_game
add_game ENLIVEN


#region LAST
REPACK_NAME="$EX_NAME-linux64+Poikilos_repack.tar.gz"
if [ -f "$REPACK_NAME" ]; then
    echo "* removing old '`pwd`/$REPACK_NAME'"
    rm -f "$REPACK_NAME"
fi
echo "* creating '`pwd`/$REPACK_NAME' from '$REPACK_TMP_MT'"
tar czvf "$REPACK_NAME" "$REPACK_TMP_MT"
REPACK_PATH="`realpath $REPACK_NAME`"
if [ $code -ne 0 ]; then exit $code; fi
echo "* $REPACK_PATH is complete."
echo "* next consider: rsync -tv /home/owner/tmp/minetest-linux64-200527+Poikilos_repack.tar.gz minetest.io:/home/owner/final-minetest-releases"
echo "  "
echo Done
#endregion LAST
