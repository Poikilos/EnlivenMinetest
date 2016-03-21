#!/bin/sh
cd $HOME
if [ -d "$HOME/minetest-stuff/minetest-chunkymap" ]; then
  rm -Rf $HOME/minetest-stuff/minetest-chunkymap
fi
CHUNKYMAP_INSTALLER_DIR=$HOME/Downloads/minetest-chunkymap
if [ ! -d "$HOME/Downloads" ]; then
	mkdir "$HOME/Downloads"
fi

cd $HOME/Downloads
if [ -f master.zip ]; then
  rm master.zip
fi
if [ -d "$HOME/Downloads/minetest-chunkymap" ]; then
  rm -Rf "$HOME/Downloads/minetest-chunkymap"
fi
if [ -d "$HOME/Downloads/minetest-chunkymap-master" ]; then
  rm -Rf "$HOME/Downloads/minetest-chunkymap-master"
fi
wget https://github.com/expertmm/minetest-chunkymap/archive/master.zip
if [ -f minetest-chunkymap.zip ]; then
  rm -f minetest-chunkymap.zip
fi
mv master.zip minetest-chunkymap.zip
unzip minetest-chunkymap.zip
if [ -d "$CHUNKYMAP_INSTALLER_DIR" ]; then
  rm -Rf "$CHUNKYMAP_INSTALLER_DIR"
fi
mv "$HOME/Downloads/minetest-chunkymap-master" "$CHUNKYMAP_INSTALLER_DIR"
#cd minetest-chunkymap
chmod +x "$CHUNKYMAP_INSTALLER_DIR/install-chunkymap-on-ubuntu.sh"
chmod +x "$CHUNKYMAP_INSTALLER_DIR/update-chunkymap-installer-only.sh"
chmod +x "$CHUNKYMAP_INSTALLER_DIR/update-chunkymap-on-ubuntu-from-web.sh"

#mv -f "$CHUNKYMAP_INSTALLER_DIR/install-chunkymap-on-ubuntu.sh" "$HOME/Downloads/"
cp -f "$CHUNKYMAP_INSTALLER_DIR/update-chunkymap-on-ubuntu-from-web.sh" "$HOME/"
