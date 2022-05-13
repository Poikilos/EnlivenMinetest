#!/bin/bash
./mtcompile-program.pl --build --finetest --server
echo "Returned $1"
good_flag_file=minetest/bin/multicraftserver
if [ -f "$good_flag_file" ]; then
    echo "* forcing OK return since found \"$good_flag_file\""
    exit 0
else
    echo "* forcing OK return since \"$good_flag_file\" doesn't exist"
    exit 1
fi
