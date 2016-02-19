#!/bin/sh
CHUNKYMAP_INSTALLER_DIR=~/minetest-stuff/minetest-chunkymap

cd ~/minetest-stuff
rm master.zip
wget https://github.com/expertmm/minetest-chunkymap/archive/master.zip
mv master.zip minetest-chunkymap.zip
unzip minetest-chunkymap.zip
#mv minetest-chunkymap-master minetest-chunkymap
mv minetest-chunkymap-master "$CHUNKYMAP_INSTALLER_DIR"
#cd minetest-chunkymap
chmod +x "$CHUNKYMAP_INSTALLER_DIR/install-chunkymap-on-ubuntu.sh"
chmod +x "$CHUNKYMAP_INSTALLER_DIR/update-chunkymap-on-ubuntu-from-web.sh"