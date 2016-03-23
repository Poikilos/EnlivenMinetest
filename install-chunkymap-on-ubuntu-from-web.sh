#!/bin/sh
cd $HOME
CHUNKYMAP_INSTALLER_DIR=$HOME/Downloads/minetest-chunkymap
if [ ! -d "$HOME/Downloads" ]; then
	mkdir "$HOME/Downloads"
fi

#chmod +x update-chunkymap-installer-only.sh

#./update-chunkymap-installer-only.sh:
cd $HOME/Downloads
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
chmod +x "$CHUNKYMAP_INSTALLER_DIR/install-chunkymap-on-ubuntu-from-web.sh"

#mv -f "$CHUNKYMAP_INSTALLER_DIR/install-chunkymap-on-ubuntu.sh" "$HOME/Downloads/"
mv -f "$CHUNKYMAP_INSTALLER_DIR/update-chunkymap-on-ubuntu-from-web.sh" "$HOME/Downloads/"
mv -f "$CHUNKYMAP_INSTALLER_DIR/install-chunkymap-on-ubuntu-from-web.sh" "$HOME/Downloads/"


chmod +x "$CHUNKYMAP_INSTALLER_DIR/install-chunkymap-on-ubuntu.sh"
sh "$CHUNKYMAP_INSTALLER_DIR/install-chunkymap-on-ubuntu.sh"
