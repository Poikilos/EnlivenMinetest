#!/bin/sh
CHUNKYMAP_INSTALLER_DIR=~/minetest-stuff/minetest-chunkymap

MINETEST_UTIL=$HOME/minetest/util
CHUNKYMAP_DEST=$MINETEST_UTIL

sudo apt-get install python-numpy python-pil
#cd ~
#rm -f ~/minetestmapper-numpy.py
#wget https://github.com/spillz/minetest/raw/master/util/minetestmapper-numpy.py
#since colors.txt is in ~/minetest/util:
cp -f "$CHUNKYMAP_INSTALLER_DIR/minetestmapper-numpy.py" "$HOME/minetest/util/minetestmapper-numpy.py"
mkdir "$CHUNKYMAP_DEST"
cp -f "$CHUNKYMAP_INSTALLER_DIR/chunkymap-regen.py" "$CHUNKYMAP_DEST/"
#chmod +x "$CHUNKYMAP_DEST/chunkymap-regen.py"
cp -f "$CHUNKYMAP_INSTALLER_DIR/chunkymap-regen.sh" "$CHUNKYMAP_DEST/"
chmod +x "$CHUNKYMAP_DEST/chunkymap-regen.sh"
cp -f "$CHUNKYMAP_INSTALLER_DIR/chunkymap-cronjob" "$CHUNKYMAP_DEST/"
chmod +x "$CHUNKYMAP_DEST/chunkymap-cronjob"
cp -f "$CHUNKYMAP_INSTALLER_DIR/set-minutely-crontab-job.sh" "$CHUNKYMAP_DEST/"
chmod +x "$CHUNKYMAP_DEST/set-minutely-crontab-job.sh"
cd "$CHUNKYMAP_INSTALLER_DIR"
python replace-with-current-user.py

# NOTE: colors.txt should ALREADY be in ~/minetest/util