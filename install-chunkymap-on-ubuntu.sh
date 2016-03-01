#!/bin/sh
cd $HOME
MT_MY_WEBSITE_PATH=/var/www/html/minetest
if [ -d "$HOME/minetest-stuff/minetest-chunkymap" ]; then
  rm -Rf $HOME/minetest-stuff/minetest-chunkymap
fi
CHUNKYMAP_INSTALLER_PATH=$HOME/Downloads/minetest-chunkymap
if [ ! -d "$HOME/Downloads" ]; then
  mkdir "$HOME/Downloads"
fi

MINETEST_UTIL=$HOME/minetest/util
CHUNKYMAP_DEST=$MINETEST_UTIL

#cd $HOME/Downloads
#rm -f $HOME/minetestmapper-numpy.py
#wget https://github.com/spillz/minetest/raw/master/util/minetestmapper-numpy.py
#since colors.txt is in $HOME/minetest/util:
cp -f "$CHUNKYMAP_INSTALLER_PATH/minetestmapper-numpy.py" "$HOME/minetest/util/minetestmapper-numpy.py"
if [ ! -d "$CHUNKYMAP_DEST" ]; then
  # Control will enter here if $DIRECTORY doesn't exist.
  mkdir "$CHUNKYMAP_DEST"
fi
if [ ! -d "$CHUNKYMAP_DEST/unused/" ]; then
  mkdir "$CHUNKYMAP_DEST/unused/"
fi
cp -f "$CHUNKYMAP_INSTALLER_PATH/chunkymap-regen.py" "$CHUNKYMAP_DEST/"
#chmod +x "$CHUNKYMAP_DEST/chunkymap-regen.py"

cp -f "$CHUNKYMAP_INSTALLER_PATH/README.md" "$CHUNKYMAP_DEST/"
#remove files place in dest by old version of installer script:
rm -f "$CHUNKYMAP_DEST/chunkymap-regen.sh"
rm -f "$CHUNKYMAP_DEST/chunkymap-regen-players.sh"
rm -f "$CHUNKYMAP_DEST/chunkymap-cronjob"
rm -f "$CHUNKYMAP_DEST/chunkymap-players-cronjob"
rm -f "$CHUNKYMAP_DEST/set-minutely-players-crontab-job.sh"
rm -f "$CHUNKYMAP_DEST/set-minutely-crontab-job.sh"
#install scripts:
cp -f "$CHUNKYMAP_INSTALLER_PATH/chunkymap-regen-loop.sh" "$CHUNKYMAP_DEST/"
#install not-recommended scripts:
cp -f "$CHUNKYMAP_INSTALLER_PATH/unused/chunkymap-regen.sh" "$CHUNKYMAP_DEST/unused/"
cp -f "$CHUNKYMAP_INSTALLER_PATH/unused/chunkymap-regen-players.sh" "$CHUNKYMAP_DEST/unused/"
cp -f "$CHUNKYMAP_INSTALLER_PATH/unused/chunkymap-cronjob" "$CHUNKYMAP_DEST/unused/"
cp -f "$CHUNKYMAP_INSTALLER_PATH/unused/chunkymap-players-cronjob" "$CHUNKYMAP_DEST/unused/"
cp -f "$CHUNKYMAP_INSTALLER_PATH/unused/set-minutely-players-crontab-job.sh" "$CHUNKYMAP_DEST/unused/"
cp -f "$CHUNKYMAP_INSTALLER_PATH/unused/set-minutely-crontab-job.sh" "$CHUNKYMAP_DEST/unused/"
if [ ! -d "$CHUNKYMAP_DEST/chunkymap" ]; then
  mkdir "$CHUNKYMAP_DEST/chunkymap"
fi
cp -f "$CHUNKYMAP_INSTALLER_PATH/minetestmapper.py" "$CHUNKYMAP_DEST/chunkymap/"
cp --no-clobber $CHUNKYMAP_INSTALLER_PATH/chunkymap-signals* "$CHUNKYMAP_DEST/"
cd "$CHUNKYMAP_INSTALLER_PATH"
python replace-with-current-user.py  # the py file only manipulates the minetest/util directory
# so chmod those files AFTER running the py above (since it rewrites them and therefore removes x attribute if present):
chmod +x  "$CHUNKYMAP_DEST/chunkymap-regen-loop.sh"
chmod -x "$CHUNKYMAP_DEST/unused/chunkymap-regen.sh"
chmod -x "$CHUNKYMAP_DEST/unused/chunkymap-regen-players.sh"
chmod -x "$CHUNKYMAP_DEST/unused/chunkymap-cronjob"
chmod -x "$CHUNKYMAP_DEST/unused/set-minutely-crontab-job.sh"
chmod -x "$CHUNKYMAP_DEST/unused/set-minutely-players-crontab-job.sh"

sudo apt-get install python-numpy python-pil python-leveldb
echo ""
echo "To see what needs to be in your $MT_MY_WEBSITE_PATH directory (if you don't use that directory, modify chunkymap-regen.py to use your directory):"
echo "cd $CHUNKYMAP_DEST/web"
echo ""
echo "To view helpful scripts:"
echo "cd $CHUNKYMAP_DEST"
echo ""
echo "To learn more about chunkymap:"
echo "nano $CHUNKYMAP_DEST/README.md"
echo
echo "To start now assuming configuration matches yours (see $CHUNKYMAP_INSTALLER_PATH/README.md before this):"
echo sh minetest/util/chunkymap-regen-loop.sh
echo
# NOTE: colors.txt should ALREADY be in $HOME/minetest/util



