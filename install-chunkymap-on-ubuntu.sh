#!/bin/sh
cd ~
rm -Rf ~/minetest-stuff/minetest-chunkymap
CHUNKYMAP_INSTALLER_DIR=~/Downloads/minetest-chunkymap
if [ ! -d "~/Downloads" ]; then
	mkdir "~/Downloads"
fi

MINETEST_UTIL=$HOME/minetest/util
CHUNKYMAP_DEST=$MINETEST_UTIL

#cd ~/Downloads
#rm -f ~/minetestmapper-numpy.py
#wget https://github.com/spillz/minetest/raw/master/util/minetestmapper-numpy.py
#since colors.txt is in ~/minetest/util:
cp -f "$CHUNKYMAP_INSTALLER_DIR/minetestmapper-numpy.py" "$HOME/minetest/util/minetestmapper-numpy.py"
if [ ! -d "$CHUNKYMAP_DEST" ]; then
  # Control will enter here if $DIRECTORY doesn't exist.
  mkdir "$CHUNKYMAP_DEST"
fi
cp -f "$CHUNKYMAP_INSTALLER_DIR/chunkymap-regen.py" "$CHUNKYMAP_DEST/"
#chmod +x "$CHUNKYMAP_DEST/chunkymap-regen.py"
cp -f "$CHUNKYMAP_INSTALLER_DIR/chunkymap-regen.sh" "$CHUNKYMAP_DEST/"
chmod +x "$CHUNKYMAP_DEST/chunkymap-regen.sh"
cp -f "$CHUNKYMAP_INSTALLER_DIR/chunkymap-cronjob" "$CHUNKYMAP_DEST/"
chmod +x "$CHUNKYMAP_DEST/chunkymap-cronjob"
cp -f "$CHUNKYMAP_INSTALLER_DIR/set-minutely-crontab-job.sh" "$CHUNKYMAP_DEST/"
chmod +x "$CHUNKYMAP_DEST/set-minutely-crontab-job.sh"
cd "$CHUNKYMAP_INSTALLER_DIR"
python replace-with-current-user.py  # the py file only manipulates the minetest/util folder

sudo apt-get install python-numpy python-pil

echo "To check out chunkymap, run:"
echo "cd $CHUNKYMAP_DEST"
# NOTE: colors.txt should ALREADY be in ~/minetest/util