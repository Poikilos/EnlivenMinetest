cd "$HOME/Downloads"
MTMOD_DL_ZIP=teleporter_badCommand_jkedit.zip
MTMOD_SRC_ZIP=teleporter.zip
MTMOD_UNZ_NAME=teleporter-master/teleporter
MTMOD_DEST_NAME=teleporter
MTMOD_DEST_PATH=$MT_MYGAME_MODS_PATH/$MTMOD_DEST_NAME
echo "Installing TenPlus1's (NOT Bad_Command_'s) teleporter <https://forum.minetest.net/viewtopic.php?f=11&t=2149>"
echo "Installing TenPlus1's (NOT Bad_Command_'s) teleporter <https://forum.minetest.net/viewtopic.php?f=11&t=2149>" >> $MTMOD_SRC_ZIP.txt
if [ -d "teleporter-master" ]; then
  rm -Rf "teleporter-master"
fi
#if [ -d "$MTMOD_UNZ_NAME" ]; then
rm -Rf $MTMOD_UNZ_NAME
#fi
if [ -f $MTMOD_DL_ZIP ]; then
  rm $MTMOD_DL_ZIP
fi
if [ -f $MTMOD_SRC_ZIP ]; then
  rm $MTMOD_SRC_ZIP
fi
#wget https://github.com/Bad-Command/teleporter/archive/master.zip
#TODO:
MTMOD_UNZ_NAME=teleporter
wget http://axlemedia.net/abiyahh/users/TenPlus1/downloads/teleporter_badCommand_jkedit.zip
mv $MTMOD_DL_ZIP $MTMOD_SRC_ZIP
unzip $MTMOD_SRC_ZIP
sudo mv $MTMOD_UNZ_NAME "$MTMOD_DEST_PATH"
if [ ! -d "$MTMOD_DEST_PATH" ]; then
  echo "ERROR: failed to unzip $MTMOD_DEST_PATH, so cannot continue."
  #exit 1
fi
rm -Rf teleporter-master


echo "teleport_perms_to_build = false" >> "$MT_MYWORLD_DIR/world.mt"
#When true, a player has to have the teleport permission to build a teleporter. When false, anyone can build a new teleporter.
echo "teleport_perms_to_configure = false" >> "$MT_MYWORLD_DIR/world.mt"
#When true, a player has to have the teleport permission to configure a teleporter. Players can still build teleporters without this, however the teleporter will be locked to the default location.
echo "teleport_requires_pairing = true" >> "$MT_MYWORLD_DIR/world.mt"
#When true, a teleporter can only be configured to teleport to a location near an existing teleporter. This prevents players from pointing teleporters in to unexplored terrain.
echo "teleport_pairing_check_radius = 2" >> "$MT_MYWORLD_DIR/world.mt"
#Specifies the size of the volume to scan when looking for a paired teleporter. Do not set this to a large value; the number of nodes scanned increases by a power of 3.
echo "teleport_default_coordinates = 0,0,0" >> "$MT_MYWORLD_DIR/world.mt"
#Allows for the default coordinates for new a teleporter to be specified. This is useful when players can build new teleporters, but can't configure them.