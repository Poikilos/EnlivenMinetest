#!/bin/sh
cd $HOME
rm -Rf $HOME/minetest-stuff/minetest-chunkymap
CHUNKYMAP_INSTALLER_DIR=$HOME/Downloads/minetest-chunkymap
if [ ! -d "$HOME/Downloads" ]; then
	mkdir "$HOME/Downloads"
fi

MINETEST_UTIL=$HOME/minetest/util
CHUNKYMAP_DEST=$MINETEST_UTIL

#cd $HOME/Downloads
#rm -f $HOME/minetestmapper-numpy.py
#wget https://github.com/spillz/minetest/raw/master/util/minetestmapper-numpy.py
#since colors.txt is in $HOME/minetest/util:
cp -f "$CHUNKYMAP_INSTALLER_DIR/minetestmapper-numpy.py" "$HOME/minetest/util/minetestmapper-numpy.py"
if [ ! -d "$CHUNKYMAP_DEST" ]; then
  # Control will enter here if $DIRECTORY doesn't exist.
  mkdir "$CHUNKYMAP_DEST"
fi
cp -f "$CHUNKYMAP_INSTALLER_DIR/chunkymap-regen.py" "$CHUNKYMAP_DEST/"
#chmod +x "$CHUNKYMAP_DEST/chunkymap-regen.py"
cp -f "$CHUNKYMAP_INSTALLER_DIR/chunkymap-regen.sh" "$CHUNKYMAP_DEST/"
cp -f "$CHUNKYMAP_INSTALLER_DIR/chunkymap-regen-players.sh" "$CHUNKYMAP_DEST/"
cp -f "$CHUNKYMAP_INSTALLER_DIR/chunkymap-cronjob" "$CHUNKYMAP_DEST/"
cp -f "$CHUNKYMAP_INSTALLER_DIR/chunkymap-players-cronjob" "$CHUNKYMAP_DEST/"
cp -f "$CHUNKYMAP_INSTALLER_DIR/set-minutely-players-crontab-job.sh" "$CHUNKYMAP_DEST/"
cd "$CHUNKYMAP_INSTALLER_DIR"
python replace-with-current-user.py  # the py file only manipulates the minetest/util folder
# so chmod those files AFTER running the py above:
chmod +x "$CHUNKYMAP_DEST/chunkymap-regen.sh"
chmod +x "$CHUNKYMAP_DEST/chunkymap-regen-players.sh"
chmod +x "$CHUNKYMAP_DEST/chunkymap-cronjob"
chmod +x "$CHUNKYMAP_DEST/set-minutely-crontab-job.sh"

sudo apt-get install python-numpy python-pil
echo ""
echo "To learn about chunkymap:"
echo "cd $CHUNKYMAP_DEST"
echo ""
# NOTE: colors.txt should ALREADY be in $HOME/minetest/util
