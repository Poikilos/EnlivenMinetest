#!/bin/sh
if [ -f "`command -v screen`"]; then
    screen -S EnlivenMinetest node server.js
else
    nohup node server.js &
fi
