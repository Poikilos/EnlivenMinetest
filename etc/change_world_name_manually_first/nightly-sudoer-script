#!/bin/sh
#run this as sudoer
killall --signal SIGINT minetestserver
sudo python chunkymap/singleimage.py
./archive-mts-debug
./backup-mts-world
./mts-ENLIVEN
#su - owner /home/owner/mts-ENLIVEN
if [ -f "log_clear_mysql" ]; then
./log_clear_mysql
fi

#also try:
#cd /var/log
#sudo du -hsx .[^.]* * | sort -rh | head -20

#automatically done by chunkymap now:
#sudo rm /var/www/html/minetest/chunkymapdata/worlds/FCAGameAWorld/singleimage.png
