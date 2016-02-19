#!/bin/sh
cd ~
rm -Rf ~/minetest-stuff/minetest-chunkymap
CHUNKYMAP_INSTALLER_DIR=~/Downloads/minetest-chunkymap
if [ ! -d "$HOME/Downloads" ]; then
	mkdir "$HOME/Downloads"
fi

cd ~/Downloads
rm master.zip
wget https://github.com/expertmm/minetest-chunkymap/archive/master.zip
rm -f minetest-chunkymap.zip
mv master.zip minetest-chunkymap.zip
rm -Rf minetest-chunkymap-master
unzip minetest-chunkymap.zip
#mv minetest-chunkymap-master minetest-chunkymap
rm -Rf "$CHUNKYMAP_INSTALLER_DIR"
mv minetest-chunkymap-master "$CHUNKYMAP_INSTALLER_DIR"
#cd minetest-chunkymap
chmod +x "$CHUNKYMAP_INSTALLER_DIR/install-chunkymap-on-ubuntu.sh"
chmod +x "$CHUNKYMAP_INSTALLER_DIR/update-chunkymap-installer-only.sh"
chmod +x "$CHUNKYMAP_INSTALLER_DIR/update-chunkymap-on-ubuntu-from-web.sh"

#mv -f "$CHUNKYMAP_INSTALLER_DIR/install-chunkymap-on-ubuntu.sh" "~/Downloads/"
mv -f "$CHUNKYMAP_INSTALLER_DIR/update-chunkymap-on-ubuntu-from-web.sh" "~/"

