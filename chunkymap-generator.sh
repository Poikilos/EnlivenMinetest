#!/bin/sh
echo To reconnect with this screen type:
echo
echo sudo screen -r chunkymapgen
echo
# -S names the socket (-t only sets the title)
#FAILS: flock -n /var/run/chunkymap-regen.lockfile -c "screen -S chunkymapregen python /home/owner/chunkymap/unused/chunkymap-regen.py"
#FAILS: screen -S chunkymapregen flock -n /var/run/chunkymap-regen.lockfile -c python /home/owner/chunkymap/unused/chunkymap-regen.py
sudo screen -S chunkymapgen python /home/owner/chunkymap/generator.py
