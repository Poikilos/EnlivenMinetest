#!/bin/sh
CHUNKYMAP_INSTALLER_DIR=~/minetest-stuff/minetest-chunkymap
cd $CHUNKYMAP_INSTALLER_DIR
chmod +x update-chunkymap-installer-only.sh
./update-chunkymap-installer-only.sh
#./install-chunkymap-on-ubuntu.sh
chmod +x "$CHUNKYMAP_INSTALLER_DIR/install-chunkymap-on-ubuntu.sh"
./install-chunkymap-on-ubuntu.sh