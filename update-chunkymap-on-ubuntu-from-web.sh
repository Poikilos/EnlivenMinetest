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
