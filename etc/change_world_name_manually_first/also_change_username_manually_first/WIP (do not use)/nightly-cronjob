#!/bin/sh
#To add this, type:
# sudo crontab -e
# #Go to bottom, then to run at 9pm daily:
# * 21 * * * /home/owner/nightly-cronjob
# #Press Ctrl-X
# #Press y
killall --signal SIGINT minetestserver
#chunkymap, if present, must run as root.
python chunkymap/singleimage.py
cd /home/owner
# NOTE: sudo -u owner doesn't work, since $HOME is still root in that case ($HOME is used extensively by the scripts and programs below)
su - owner ./archive-mts-debug
su - owner ./backup-mts-world
su - owner /home/owner/mts-ENLIVEN
