#!/bin/sh
cd $HOME
#rm -Rf $HOME/minetest-stuff/minetest-chunkymap
CHUNKYMAP_INSTALLER_DIR=$HOME/Downloads/minetest-chunkymap
if [ ! -d "$HOME/Downloads" ]; then
	mkdir "$HOME/Downloads"
fi

#cd $CHUNKYMAP_INSTALLER_DIR
chmod +x update-chunkymap-installer-only.sh
cd $HOME/Downloads
mv -f update-chunkymap-installer-only.sh "$CHUNKYMAP_INSTALLER_DIR/update-chunkymap-installer-only.sh"
sh "$CHUNKYMAP_INSTALLER_DIR/update-chunkymap-installer-only.sh"
#./install-chunkymap-on-ubuntu.sh
chmod +x "$CHUNKYMAP_INSTALLER_DIR/install-chunkymap-on-ubuntu.sh"
sh "$CHUNKYMAP_INSTALLER_DIR/install-chunkymap-on-ubuntu.sh"

MT_MY_WEBSITE_PATH=/var/www/html/minetest

if [ -f "$HOME/Downloads/minetest-chunkymap/web/chunkymap.php" ]; then
	if [ -f "$MT_MY_WEBSITE_PATH/chunkymap.php" ]; then
		sudo cp -f "$HOME/Downloads/minetest-chunkymap/web/chunkymap.php" "$MT_MY_WEBSITE_PATH/chunkymap.php"
		sudo cp --no-clobber "$HOME/Downloads/minetest-chunkymap/web/index_example.php" "$MT_MY_WEBSITE_PATH/viewchunkymap.php"
		sudo cp -R --no-clobber "$HOME/Downloads/minetest-chunkymap/web/images/*" "$MT_MY_WEBSITE_PATH/images/"
		#--no-clobber: do not overwrite existing
	fi
fi
