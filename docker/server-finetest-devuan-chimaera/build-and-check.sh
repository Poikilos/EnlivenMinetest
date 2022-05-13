#!/bin/bash
./mtcompile-program.pl build --finetest --server
echo "Done './mtcompile-program.pl build --finetest --server' (returned $?)"
good_flag_file_name=finetestserver
good_flag_file=minetest/bin/$good_flag_file_name
if [ -f "$good_flag_file" ]; then
    echo "* forcing OK return since found \"$good_flag_file\" in `pwd`"
    exit 0
else
    echo "* forcing FAILED return since \"$good_flag_file\" doesn't exist in `pwd`"
    echo "* searching..."
    find /opt -name "minetest*" | grep -v "minetest\.mo" | grep -v "minetest\.po"
    find /opt -name "multicraft*"
    echo "* searching for $good_flag_file_name..."
    find /opt -name $good_flag_file_name
    exit 1
fi
