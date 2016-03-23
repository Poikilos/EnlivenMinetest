#!/bin/sh
cd $HOME
CHUNKYMAP_INSTALLER_DIR=$HOME/Downloads/minetest-chunkymap
CHUNKYMAP_DEST=$HOME/chunkymap
if [ ! -d "$HOME/Downloads" ]; then
	mkdir "$HOME/Downloads"
fi

cd "$CHUNKYMAP_DEST"
rm update-chunkymap-installer-only.sh
wget https://github.com/expertmm/minetest-chunkymap/blob/master/update-chunkymap-installer-only.sh
#Wait to make sure nothing weirdly not finished downloading:
sleep .2
cd $HOME
#cd $CHUNKYMAP_INSTALLER_DIR
#chmod +x update-chunkymap-installer-only.sh
#cd $CHUNKYMAP_DEST
#if [ -f "update-chunkymap-installer-only.sh" ]; then
  # move misplaced file from older versions:
  #mv -f update-chunkymap-installer-only.sh "$CHUNKYMAP_INSTALLER_DIR/update-chunkymap-installer-only.sh"
#fi
#sh "$CHUNKYMAP_INSTALLER_DIR/update-chunkymap-installer-only.sh"
#if [ -f "$CHUNKYMAP_DEST/update-chunkymap-installer-only.sh" ]; then
#  sh "$CHUNKYMAP_DEST/update-chunkymap-installer-only.sh"
#  #further instructions are in separate file in case updater was updated (sleep first otherwise file won't be finished writing):
#  sleep .25
#  sh "$CHUNKYMAP_INSTALLER_DIR/post-update.sh"
#else
  sh "$CHUNKYMAP_INSTALLER_DIR/update-chunkymap-installer-only.sh"
  #further instructions are in separate file in case updater was updated (sleep first otherwise file won't be finished writing):
  sleep .2
  sh "$CHUNKYMAP_INSTALLER_DIR/post-update.sh"
#fi
