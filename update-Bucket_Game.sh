#!/bin/bash
UPD_BG_SCRIPT_NAME=update-Bucket_Game.sh
source minetestenv-in-place.rc
if [ $? -ne 0 ]; then
    source ~/git/EnlivenMinetest/minetestenv-in-place.rc
fi
if [ $? -ne 0 ]; then
    source ~/Downloads/git/EnlivenMinetest/minetestenv-in-place.rc
fi
if [ $? -ne 0 ]; then
    source ~/EnlivenMinetest/minetestenv-in-place.rc
fi
if [ $? -ne 0 ]; then
    cat <<END
minetest-in-place.rc is not present here or in the path, and
EnlivenMinetest (directory containing that rc file)
is not in ~/git nor ~/Downloads/git nor ~.
END
    exit 1
fi
if [ ! -f "`command -v unzip`" ]; then
    echo "ERROR: You must have unzip to use $UPD_BG_SCRIPT_NAME."
    exit 1
fi
if [ ! -d "$INSTALL_PATH/games" ]; then
    echo "$INSTALL_PATH/games is missing."
    exit 1
fi
DL_NAME=Bucket_Game.zip
BG_URL="https://downloads.minetest.org/$DL_NAME"
EM_TMP=/tmp/EnlivenMinetest
DLS_PATH=$EM_TMP
DL_PATH=$DLS_PATH/$DL_NAME
TRY_PATH="$HOME/Downloads/$DL_NAME"
EXTRACTED_NAME=Bucket_Game
EXTRACTED_PATH=$EM_TMP/Bucket_Game
ORIG_SRC="$BG_URL"
if [ -f "$TRY_PATH" ]; then
    DL_PATH="$TRY_PATH"
fi
if [ ! -d "$EM_TMP" ]; then
    mkdir -p "$EM_TMP"
fi
ENABLE_DL=false
if [ ! -f "$DL_PATH" ]; then
    ENABLE_DL=true
    DL_BIN_NAME="wget"
    if [ -f "`command -v wget`" ]; then
        wget -O $DL_PATH $BG_URL
    elif [ -f "`command -v curl`" ]; then
        curl $BG_URL -o $DL_PATH
        DL_BIN_NAME="curl"
    else
        echo "ERROR: You need curl or wget to use $UPD_BG_SCRIPT_NAME."
        exit 1
    fi
    if [ ! -f "$DL_PATH" ]; then
        echo "ERROR: $DL_BIN_NAME could not create $DL_PATH from $BG_URL."
        exit 1
    fi
else
    echo "* using existing $DL_PATH..."
    ORIG_SRC="$DL_PATH"
fi

if [ -d "$EXTRACTED_PATH" ]; then
    rm -Rf "$EXTRACTED_PATH"
    if [ $? -ne 0 ]; then
        echo "ERROR: Deleting the old \"$EXTRACTED_PATH\" failed."
        # if [ "@$ENABLE_DL" = "@true" ]; then
        #     rm "$DL_PATH"
        # fi
        exit 1
    fi
fi

cd "$EM_TMP"
if [ $? -ne 0 ]; then
    echo "ERROR: cd \"$EM_TMP\" failed."
    exit 1
fi

unzip "$DL_PATH"
if [ $? -ne 0 ]; then
    echo "ERROR: unzip \"$DL_PATH\" failed."
    exit 1
fi
RMDIR_PATH=
if [ ! -d "$EXTRACTED_PATH/mods" ]; then
    if [ -d "$EXTRACTED_PATH/$EXTRACTED_NAME/mods" ]; then
        RMDIR_PATH="$EXTRACTED_PATH"
        EXTRACTED_PATH="$EXTRACTED_PATH/$EXTRACTED_NAME"
    else
        echo "ERROR: unzip \"$DL_PATH\" did not produce $EXTRACTED_PATH/mods nor $EXTRACTED_PATH/$EXTRACTED_NAME/mods."
        exit 1
    fi
fi
DEST_BG="$INSTALL_PATH/games/Bucket_Game"
if [ -d "$DEST_BG" ]; then
    echo "* removing the old \"$DEST_BG\"..."
    rm -Rf "$DEST_BG"
    if [ $? -ne 0 ]; then
        echo "ERROR: rm -Rf \"$DEST_BG\" failed."
        exit 1
    fi
fi

echo "* mv $EXTRACTED_PATH $DEST_BG..."
mv "$EXTRACTED_PATH" "$DEST_BG"
if [ $? -ne 0 ]; then
    echo "ERROR: mv \"$EXTRACTED_PATH\" \"$DEST_BG\" failed."
    exit 1
fi

echo "* Updating \"$DEST_BG\" from \"$ORIG_SRC\" completed successfully."

if [ ! -z "$RMDIR_PATH" ]; then
    rmdir "$RMDIR_PATH"
fi

if [ "$DL_PATH" != "$TRY_PATH" ]; then
    rm "$DL_PATH"
#else it is where the user Downloaded it themselves, so don't delete it.
fi
cd $DLS_PATH
