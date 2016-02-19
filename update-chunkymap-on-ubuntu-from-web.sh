#!/bin/sh
CHUNKYMAP_INSTALLER_DIR=~/minetest-stuff/minetest-chunkymap
./update-chunkymap-installer-only.sh
#./install-chunkymap-on-ubuntu.sh


cp -f "$CHUNKYMAP_INSTALLER_DIR/minetestmapper-numpy.py" "$HOME/minetest/util/minetestmapper-numpy.py"
mkdir "$CHUNKYMAP_DEST"
cp -f "$CHUNKYMAP_INSTALLER_DIR/chunkymap-regen.py" "$CHUNKYMAP_DEST/"
#chmod +x "$CHUNKYMAP_DEST/chunkymap-regen.py"
cp -f "$CHUNKYMAP_INSTALLER_DIR/chunkymap-regen.sh" "$CHUNKYMAP_DEST/"
chmod +x "$CHUNKYMAP_DEST/chunkymap-regen.sh"
cp -f "$CHUNKYMAP_INSTALLER_DIR/chunkymap-cronjob" "$CHUNKYMAP_DEST/"
chmod +x "$CHUNKYMAP_DEST/chunkymap-cronjob"
cp -f "$CHUNKYMAP_INSTALLER_DIR/set-minutely-crontab-job.sh" "$CHUNKYMAP_DEST/"
chmod +x "$CHUNKYMAP_DEST/set-minutely-crontab-job.sh"

python replace-with-current-user.py