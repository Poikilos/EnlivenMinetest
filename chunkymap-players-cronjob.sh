#!/bin/sh
# NOTE: only works since all scripts in /etc/cron.*/ or crontab run as root
#python /home/owner/minetest/util/chunkymap-regen.py
#-1 FOR LESS THAN ONE MINUTE AGO:
#lol won't work because if the py doesn't run the players won't be updated
#MT_PLAYERS_ACTIVE_COUNT=$(find /var/www/html/minetest/chunkymapdata/players -type f -mmin -1 | wc -l)
#if[ $MT_PLAYERS_ACTIVE_COUNT -gt 0 ]; then
flock -n /var/run/chunkymap-regen.lockfile -c /home/owner/minetest/util/chunkymap-regen-players.sh
#fi