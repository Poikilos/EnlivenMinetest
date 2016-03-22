#!/bin/sh
cd $HOME
if [ -d "$HOME/minetest-stuff/minetest-chunkymap" ]; then
  rm -Rf $HOME/minetest-stuff/minetest-chunkymap
fi
CHUNKYMAP_INSTALLER_DIR=$HOME/Downloads/minetest-chunkymap
CHUNKYMAP_DEST=$HOME/chunkymap
if [ ! -d "$HOME/Downloads" ]; then
	mkdir "$HOME/Downloads"
fi

#cd $CHUNKYMAP_INSTALLER_DIR
#chmod +x update-chunkymap-installer-only.sh
#cd $CHUNKYMAP_DEST
#if [ -f "update-chunkymap-installer-only.sh" ]; then
  # move misplaced file from older versions:
  #mv -f update-chunkymap-installer-only.sh "$CHUNKYMAP_INSTALLER_DIR/update-chunkymap-installer-only.sh"
#fi
#sh "$CHUNKYMAP_INSTALLER_DIR/update-chunkymap-installer-only.sh"
if [ -f "$CHUNKYMAP_DEST/update-chunkymap-installer-only.sh" ]; then
	sh "$CHUNKYMAP_DEST/update-chunkymap-installer-only.sh"
else
	sh "$CHUNKYMAP_INSTALLER_DIR/update-chunkymap-installer-only.sh"
fi
#./install-chunkymap-on-ubuntu.sh
cd $HOME/Downloads
chmod +x "$CHUNKYMAP_INSTALLER_DIR/install-chunkymap-on-ubuntu.sh"
echo ""
echo "running install-chunkymap-on-ubuntu.sh..."
sh "$CHUNKYMAP_INSTALLER_DIR/install-chunkymap-on-ubuntu.sh"
echo "...returned to update-chunkymap-on-ubuntu-from-web.sh"
echo ""
MT_MY_WEBSITE_PATH=/var/www/html/minetest

# IF already installed to default MT_MY_WEBSITE_PATH, update the files:
if [ -f "$HOME/Downloads/minetest-chunkymap/web/chunkymap.php" ]; then
	if [ -f "$MT_MY_WEBSITE_PATH/chunkymap.php" ]; then
		sudo cp -f "$HOME/Downloads/minetest-chunkymap/web/chunkymap.php" "$MT_MY_WEBSITE_PATH/"
		echo "updated $MT_MY_WEBSITE_PATH/chunkymap.php"
		#sudo cp --no-clobber "$HOME/Downloads/minetest-chunkymap/web/viewchunkymap.php" "$MT_MY_WEBSITE_PATH/viewchunkymap.php"
		sudo cp -f "$HOME/Downloads/minetest-chunkymap/web/viewchunkymap.php" "$MT_MY_WEBSITE_PATH/viewchunkymap.php"
		echo "updated $MT_MY_WEBSITE_PATH/viewchunkymap.php"
		# cannot put wildcard in quotes on unix
		#sudo cp -R --no-clobber $HOME/Downloads/minetest-chunkymap/web/images/* "$MT_MY_WEBSITE_PATH/images/"
		#--no-clobber: do not overwrite existing
	fi
fi
