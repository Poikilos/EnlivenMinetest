#!/bin/sh
flock -n /var/run/chunkymap-loop.lockfile -c screen -t chunkymapregen python /home/owner/minetest/util/chunkymap-regen.py
