#!/bin/sh
echo To reconnect with this screen type:
echo
echo sudo screen -r
echo
# -S names the socket (-t only sets the title)
#FAILS: flock -n /var/run/chunkymap-loop.lockfile -c "screen -S chunkymapregen python /home/owner/minetest/util/chunkymap-regen.py"
#FAILS: screen -S chunkymapregen flock -n /var/run/chunkymap-loop.lockfile -c python /home/owner/minetest/util/chunkymap-regen.py
sudo screen -S chunkymapregen python /home/owner/minetest/util/chunkymap-regen.py