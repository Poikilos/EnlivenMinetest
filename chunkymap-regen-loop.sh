#!/bin/sh
echo type screen -r  to reconnect with this screen
# -S names the socket (-t only sets the title)
#FAILS: flock -n /var/run/chunkymap-loop.lockfile -c "screen -S chunkymapregen python /home/owner/minetest/util/chunkymap-regen.py"
#FAILS: screen -S chunkymapregen flock -n /var/run/chunkymap-loop.lockfile -c python /home/owner/minetest/util/chunkymap-regen.py
screen -S chunkymapregen python /home/owner/minetest/util/chunkymap-regen.py