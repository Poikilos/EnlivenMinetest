#!/bin/bash
MODS_DIR="`pwd`"
TRY_MODS_DIR="/opt/minebest/mtworlds/center/ENLIVEN/mods"
GOOD_FLAG_DIR="metatools"
if [ ! -d "$MODS_DIR/$GOOD_FLAG_DIR" ]; then
    if [ -d "$TRY_MODS_DIR/$GOOD_FLAG_DIR" ]; then
        echo "* changing to '$TRY_MODS_DIR' (detected; changing since no $GOOD_FLAG_DIR in $MODS_DIR)"
        MODS_DIR="$TRY_MODS_DIR"
    fi
fi
if [ ! -d "$MODS_DIR/$GOOD_FLAG_DIR" ]; then
    echo "Error: You must run this from the mods directory such as \"$TRY_MODS_DIR\"."
    exit 1
fi

update_mod(){
    if [ -z "$1" ]; then
        echo "Error: update_mod expects a mod name."
        exit 1
    fi
    MOD="$1"
    if [ ! -d "$MODS_DIR/$MOD" ]; then
        echo "Error: update_mod expects a mod name but \"$MODS_DIR/$MOD\" doesn't exist."
        exit 1
    fi
    printf "* cd \"$MODS_DIR/$MOD\"..."
    cd "$MODS_DIR/$MOD"
    if [ $? -ne 0 ]; then
        echo "FAILED"
    else
        echo "OK"
    fi
    printf "* git pull..."
    sudo -u minebest git pull
    if [ $? -ne 0 ]; then
        echo "FAILED"
    else
        echo "OK"
    fi
}

update_mod metatools
