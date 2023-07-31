#!/bin/bash
BIN_DIR=~/finetest/bin
TRY_BIN_DIR=~/finetest-220509/bin
if [ -d "$TRY_BIN_DIR" ]; then
    BIN_DIR=$TRY_BIN_DIR
fi
BIN=finetest
ERR=debug.txt
# OUT=out.txt
ERR_PATH=$BIN_DIR/$ERR
TAIL_PATH=$BIN_DIR/$ERR.tail.txt
cd $BIN_DIR && ./$BIN --quiet >& $ERR_PATH
if [ $? -ne 0 ]; then
    tail -n 100 $ERR_PATH > $TAIL_PATH
    # xmessage -file "$TAIL_PATH" -center
    xmessage -file "$TAIL_PATH" -nearmouse
fi
