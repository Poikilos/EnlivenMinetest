#!/bin/sh
# NOTE: only works since all scripts in /etc/cron.*/ or crontab run as root
python /home/owner/minetest/util/chunkymap-regen.py --skip-map=true

