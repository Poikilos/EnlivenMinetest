#!/bin/sh
cd $HOME
#rm -Rf $HOME/minetest-stuff/minetest-chunkymap
CHUNKYMAP_INSTALLER_DIR=$HOME/Downloads/minetest-chunkymap
if [ ! -d "$HOME/Downloads" ]; then
	mkdir "$HOME/Downloads"
fi

#cd $CHUNKYMAP_INSTALLER_DIR
#chmod +x update-chunkymap-installer-only.sh
cd $HOME/Downloads
if [ -f "update-chunkymap-installer-only.sh" ]; then
  # move misplaced file from older versions:
  mv -f update-chunkymap-installer-only.sh "$CHUNKYMAP_INSTALLER_DIR/update-chunkymap-installer-only.sh"
fi
sh "$CHUNKYMAP_INSTALLER_DIR/update-chunkymap-installer-only.sh"
#./install-chunkymap-on-ubuntu.sh
chmod +x "$CHUNKYMAP_INSTALLER_DIR/install-chunkymap-on-ubuntu.sh"
sh "$CHUNKYMAP_INSTALLER_DIR/install-chunkymap-on-ubuntu.sh"

MT_MY_WEBSITE_PATH=/var/www/html/minetest

# IF already installed to default MT_MY_WEBSITE_PATH, update the files:
if [ -f "$HOME/Downloads/minetest-chunkymap/web/chunkymap.php" ]; then
	if [ -f "$MT_MY_WEBSITE_PATH/chunkymap.php" ]; then
		sudo cp -f "$HOME/Downloads/minetest-chunkymap/web/chunkymap.php" "$MT_MY_WEBSITE_PATH/"
		sudo cp --no-clobber "$HOME/Downloads/minetest-chunkymap/web/example.php" "$MT_MY_WEBSITE_PATH/map.php"
		# cannot put wildcard in quotes on unix
		sudo cp -R --no-clobber $HOME/Downloads/minetest-chunkymap/web/images/* "$MT_MY_WEBSITE_PATH/images/"
		#--no-clobber: do not overwrite existing
	fi
fi
