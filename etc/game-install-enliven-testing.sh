echo "Installing Enliven TESTING patch (run this after game-install-enliven.sh)"
echo "* You have to manually paste the environment variable settings from the beginning of game-install-enliven.sh here, so you have them."
echo "* Only install these mods if you know what you are doing! These mods may become part of enliven later, but are not thoroughly tested for stability and compatibility. Thanks, expertmm."
echo "Known issues:"
echo "* advanced_npc: 0.4.15 git (Jan 2017) has error with advanced_npc even with secure.enable_security = false ()"
echo "* torches: removes ceiling torches"

#TODO:
# * possibly add aliases for mobf_traders--Sokomine seems to indicate that this worldgen mod spawns the villagers manually: https://github.com/Sokomine/mg_villages/issues/5
# * add splash icon AND splash background for Enliven subgame
# * clicking barrel just rotates it (destroying watever you had left in it)
# * try https://github.com/Sokomine/mines_with_shafts and see if has treasure
# * try https://github.com/Sokomine/village_gambit additional village type for mg_villages
# * merge /home and unifiedinventory home (and make both require home priv)

#TODO for enliven main branch:
# * shift click to pull out maximum number of items you can create (such as multiple stacks of stairs from wood)
# * kick players at certain time intervals (if play span when logged in is not current play span, then kick) such as for schools
# * remove recipe for flint&steel (obsidian shard+Wrought Iron Ingot [default:steel_ingot])
# * detect whether tnt is disabled, and make obtaining it obtain a note or something (or somehow disable spawning of item in rail corridor chests where I found some)
# * rename minetest-chunkymap to minetestoffline or something
# * add recommended minetest.conf settings (provide python script to test, requiring minetestoffline)
# * analyze game-install-enliven-testing-FULLDEBUG.txt
# * possibly disable fire:flint_and_steel usage other than fake fire (fake fire fork used is in homedecor_modpack)
# * make spawners have drops -- similar drops as [cme] creatures:*_spawner
# * test whether abandoned mines will still be littered with empty chests if CHESTS_GENERATE or SPAWNERS_GENERATE instead of both are on in settings.txt in spawners mod folder (mine chests had stuff before adding spawners mod [mobs mod had been added])
# * make bones write where&whose bones were placed to log (see "dungeon spawner placed at" in spawners for lua example)
# * resolve mg_villages error:
#2017-01-30 03:08:37: ERROR[Main]: ServerError: AsyncErr: ServerThread::run Lua: Runtime error from mod 'default' in callback item_OnPlace(): ...e/minetest/games/enliven/mods/mg_villages/protection.lua:215: attempt to concatenate field 'mts_path' (a nil value)
#2017-01-30 03:08:37: ERROR[Main]: stack traceback:
#2017-01-30 03:08:37: ERROR[Main]:  ...e/minetest/games/enliven/mods/mg_villages/protection.lua:215: in function 'on_rightclick'
#2017-01-30 03:08:37: ERROR[Main]:  ...ocal/share/minetest/games/enliven/mods/default/torch.lua:67: in function <...ocal/share/minetest/games/enliven/mods/default/#torch.lua:61>
#2017-01-30 03:08:37: ACTION[Server]: singleplayer leaves game. List of players:
#2017-01-30 03:08:37: ACTION[Main]: [fishing] Server shuts down. saving trophies table
# * resolve issue where signslib uses small Helvetica Narrow font even if extrafonts is used properly by 31px/* (largest) being copied to signslib/textures/ (see below)
# * check whether special_picks large picks can break protection
# * change uses of maxwear=x to uses=1/x as per minetest server startup warnings: plantlife_modpack/vines/shear.lua and worldedit_commands/wand.lua
# * sometimes sorting compassgps by location crashes (only on the included user file named yelby in the etc folder)
if [ ! -d "$MT_MYGAME_MODS_PATH" ]; then
  echo "bad MT_MYGAME_MODS_PATH=$MT_MYGAME_MODS_PATH, so you must be doing it wrong."
  exit 1
fi
#used by mg_villages fork by Sokomine
cd $HOME/Downloads
MTMOD_SRC_ZIP=handle_schematics.zip
MTMOD_UNZ_NAME=handle_schematics-master
MTMOD_DEST_NAME=handle_schematics
MTMOD_DEST_PATH=$MT_MYGAME_MODS_PATH/$MTMOD_DEST_NAME
if [ ! -z "`ls | grep $MTMOD_UNZ_NAME`" ]; then  # works with wildcard in variable
  rm -Rf $MTMOD_UNZ_NAME
fi
if [ -f $MTMOD_SRC_ZIP ]; then
  rm -f $MTMOD_SRC_ZIP
fi
if [ -d "$MTMOD_DEST_PATH" ]; then
  sudo rm -Rf "$MTMOD_DEST_PATH"
fi
wget -O $MTMOD_SRC_ZIP https://github.com/Sokomine/handle_schematics/archive/master.zip
unzip "$MTMOD_SRC_ZIP"
sudo mv $MTMOD_UNZ_NAME "$MTMOD_DEST_PATH"
if [ ! -d "$MTMOD_DEST_PATH" ]; then
  echo "ERROR: failed to unzip $MTMOD_DEST_PATH, so cannot continue."
  exit 1
fi


#https://forum.minetest.net/viewtopic.php?t=14359
#This mod is part of minetest_game 0.4.15!
#With exception of the wieldlight
#cd $HOME/Downloads
#MTMOD_SRC_ZIP=torches.zip
#MTMOD_UNZ_NAME=torches-master
#MTMOD_DEST_NAME=torches
#MTMOD_DEST_PATH=$MT_MYGAME_MODS_PATH/$MTMOD_DEST_NAME
#if [ ! -z "`ls | grep $MTMOD_UNZ_NAME`" ]; then  # works with wildcard in variable
#  rm -Rf $MTMOD_UNZ_NAME
#fi
#if [ -f $MTMOD_SRC_ZIP ]; then
#  rm -f $MTMOD_SRC_ZIP
#fi
#if [ -d "$MTMOD_DEST_PATH" ]; then
#  sudo rm -Rf "$MTMOD_DEST_PATH"
#fi
#wget -O $MTMOD_SRC_ZIP https://github.com/BlockMen/torches/archive/master.zip
#unzip "$MTMOD_SRC_ZIP"
#sudo mv $MTMOD_UNZ_NAME "$MTMOD_DEST_PATH"
#if [ ! -d "$MTMOD_DEST_PATH" ]; then
#  echo "ERROR: failed to unzip $MTMOD_DEST_PATH, so cannot continue."
#  exit 1
#fi


cd $HOME/Downloads
MTMOD_SRC_ZIP=moresnow.zip
MTMOD_UNZ_NAME=moresnow-master
MTMOD_DEST_NAME=moresnow
MTMOD_DEST_PATH=$MT_MYGAME_MODS_PATH/$MTMOD_DEST_NAME
if [ ! -z "`ls | grep $MTMOD_UNZ_NAME`" ]; then  # works with wildcard in variable
  rm -Rf $MTMOD_UNZ_NAME
fi
if [ -f $MTMOD_SRC_ZIP ]; then
  rm -f $MTMOD_SRC_ZIP
fi
if [ -d "$MTMOD_DEST_PATH" ]; then
  sudo rm -Rf "$MTMOD_DEST_PATH"
fi
wget -O $MTMOD_SRC_ZIP https://github.com/Sokomine/moresnow/archive/master.zip
unzip "$MTMOD_SRC_ZIP"
sudo mv $MTMOD_UNZ_NAME "$MTMOD_DEST_PATH"
if [ ! -d "$MTMOD_DEST_PATH" ]; then
  echo "ERROR: failed to unzip $MTMOD_DEST_PATH, so cannot continue."
  exit 1
fi



echo "Installing adrido's (NOT MasterGollum's which is incompatible with moreblocks) darkage..."
#linked from MasterGollum's: https://forum.minetest.net/viewtopic.php?id=3213
cd $HOME/Downloads
MTMOD_SRC_ZIP=darkage.zip
MTMOD_UNZ_NAME=darkage-master
MTMOD_DEST_NAME=darkage
MTMOD_DEST_PATH=$MT_MYGAME_MODS_PATH/$MTMOD_DEST_NAME
if [ ! -z "`ls | grep $MTMOD_UNZ_NAME`" ]; then  # works with wildcard in variable
  rm -Rf $MTMOD_UNZ_NAME
fi
if [ -f $MTMOD_SRC_ZIP ]; then
  rm -f $MTMOD_SRC_ZIP
fi
if [ -d "$MTMOD_DEST_PATH" ]; then
  sudo rm -Rf "$MTMOD_DEST_PATH"
fi
wget -O $MTMOD_SRC_ZIP https://github.com/adrido/darkage/archive/master.zip
unzip "$MTMOD_SRC_ZIP"
sudo mv $MTMOD_UNZ_NAME "$MTMOD_DEST_PATH"
if [ ! -d "$MTMOD_DEST_PATH" ]; then
  echo "ERROR: failed to unzip $MTMOD_DEST_PATH, so cannot continue."
  exit 1
fi

cd $HOME/Downloads
MTMOD_SRC_ZIP=cottages.zip
MTMOD_UNZ_NAME=cottages-master
MTMOD_DEST_NAME=cottages
MTMOD_DEST_PATH=$MT_MYGAME_MODS_PATH/$MTMOD_DEST_NAME
if [ ! -z "`ls | grep $MTMOD_UNZ_NAME`" ]; then  # works with wildcard in variable
  rm -Rf $MTMOD_UNZ_NAME
fi
if [ -f $MTMOD_SRC_ZIP ]; then
  rm -f $MTMOD_SRC_ZIP
fi
if [ -d "$MTMOD_DEST_PATH" ]; then
  sudo rm -Rf "$MTMOD_DEST_PATH"
fi
wget $MTMOD_SRC_ZIP https://github.com/Sokomine/cottages/archive/master.zip
unzip "$MTMOD_SRC_ZIP"
sudo mv $MTMOD_UNZ_NAME "$MTMOD_DEST_PATH"
if [ ! -d "$MTMOD_DEST_PATH" ]; then
  echo "ERROR: failed to unzip $MTMOD_DEST_PATH, so cannot continue."
  exit 1
fi



cd $HOME/Downloads
MTMOD_SRC_ZIP=advanced_npc.zip
MTMOD_UNZ_NAME=advanced_npc-master
MTMOD_DEST_NAME=advanced_npc
MTMOD_DEST_PATH=$MT_MYGAME_MODS_PATH/$MTMOD_DEST_NAME
if [ ! -z "`ls | grep $MTMOD_UNZ_NAME`" ]; then  # works with wildcard in variable
  rm -Rf $MTMOD_UNZ_NAME
fi
if [ -f $MTMOD_SRC_ZIP ]; then
  rm -f $MTMOD_SRC_ZIP
fi
if [ -d "$MTMOD_DEST_PATH" ]; then
  sudo rm -Rf "$MTMOD_DEST_PATH"
fi
wget -O $MTMOD_SRC_ZIP https://github.com/hkzorman/advanced_npc/archive/master.zip
unzip "$MTMOD_SRC_ZIP"
sudo mv $MTMOD_UNZ_NAME "$MTMOD_DEST_PATH"
if [ ! -d "$MTMOD_DEST_PATH" ]; then
  echo "ERROR: failed to unzip $MTMOD_DEST_PATH, so cannot continue."
  exit 1
fi


#forum post (special_picks by cx384): https://forum.minetest.net/viewtopic.php?f=11&t=9574
cd $HOME/Downloads
MTMOD_SRC_ZIP=special_picks.zip
MTMOD_UNZ_NAME=special_picks-master
MTMOD_DEST_NAME=special_picks
MTMOD_DEST_PATH=$MT_MYGAME_MODS_PATH/$MTMOD_DEST_NAME
if [ ! -z "`ls | grep $MTMOD_UNZ_NAME`" ]; then  # works with wildcard in variable
  rm -Rf $MTMOD_UNZ_NAME
fi
if [ -f $MTMOD_SRC_ZIP ]; then
  rm -f $MTMOD_SRC_ZIP
fi
if [ -d "$MTMOD_DEST_PATH" ]; then
  sudo rm -Rf "$MTMOD_DEST_PATH"
fi
wget -O $MTMOD_SRC_ZIP https://github.com/cx384/special_picks/archive/master.zip
unzip "$MTMOD_SRC_ZIP"
sudo mv $MTMOD_UNZ_NAME "$MTMOD_DEST_PATH"
if [ ! -d "$MTMOD_DEST_PATH" ]; then
  echo "ERROR: failed to unzip $MTMOD_DEST_PATH, so cannot continue."
  exit 1
fi


# no longer needed since ENLIVEN main branch now uses expertmm travelnet:
#cd $HOME/Downloads
#MTMOD_SRC_ZIP=travelnet.zip
#MTMOD_UNZ_NAME=travelnet-master
#MTMOD_DEST_NAME=travelnet
#MTMOD_DEST_PATH=$MT_MYGAME_MODS_PATH/$MTMOD_DEST_NAME
#if [ ! -z "`ls | grep $MTMOD_UNZ_NAME`" ]; then  # works with wildcard in variable
#  rm -Rf $MTMOD_UNZ_NAME
#fi
#if [ -f $MTMOD_SRC_ZIP ]; then
#  rm -f $MTMOD_SRC_ZIP
#fi
#if [ -d "$MTMOD_DEST_PATH" ]; then
#  sudo rm -Rf "$MTMOD_DEST_PATH"
#fi
#wget -O $MTMOD_SRC_ZIP https://github.com/Sokomine/travelnet/archive/master.zip
#unzip "$MTMOD_SRC_ZIP"
#sudo mv $MTMOD_UNZ_NAME "$MTMOD_DEST_PATH"




cd "$HOME/Downloads"
#does NOT have a zip extension when downloaded via wget:
MTMOD_SRC_ZIP=mesecons_modpack.zip
MTMOD_UNZ_NAME=mesecons-master
MTMOD_DEST_NAME=mesecons
MTMOD_DEST_PATH=$MT_MYGAME_MODS_PATH/$MTMOD_DEST_NAME
if [ ! -z "`ls | grep $MTMOD_UNZ_NAME`" ]; then  # works with wildcard in variable
 rm -Rf $MTMOD_UNZ_NAME
fi
rm -Rf minetest-mods-mesecons-*
rm -Rf ""
if [ -f "$MTMOD_SRC_ZIP" ]; then
  rm -f "$MTMOD_SRC_ZIP"
fi
wget -O $MTMOD_SRC_ZIP https://github.com/minetest-mods/mg/archive/master.zip
unzip $MTMOD_SRC_ZIP
if [ -d "$MTMOD_DEST_PATH" ]; then
  sudo rm -Rf "$MTMOD_DEST_PATH"
fi
sudo mv -f $MTMOD_UNZ_NAME "$MTMOD_DEST_PATH"
if [ ! -d "$MTMOD_DEST_PATH" ]; then
  echo "ERROR: failed to create $MTMOD_DEST_PATH, so cannot continue." > $err_txt
  cat $err_txt
  sleep 3
  exit 1
fi

# no longer needed (?) since minetest-mods now maintains an mg with villages
#forum post (Sokomine's mg_villages provides villages for all mapgens and is based on is fork of Nores mg mapgen): https://forum.minetest.net/viewtopic.php?f=9&t=13116
#cd $HOME/Downloads
#MTMOD_SRC_ZIP=mg_villages.zip
#MTMOD_UNZ_NAME=mg_villages-master
#MTMOD_DEST_NAME=mg_villages
#MTMOD_DEST_PATH=$MT_MYGAME_MODS_PATH/$MTMOD_DEST_NAME
#if [ ! -z "`ls | grep $MTMOD_UNZ_NAME`" ]; then  # works with wildcard in variable
#  rm -Rf $MTMOD_UNZ_NAME
#fi
#if [ -f $MTMOD_SRC_ZIP ]; then
#  rm -f $MTMOD_SRC_ZIP
#fi
#if [ -d "$MTMOD_DEST_PATH" ]; then
#  sudo rm -Rf "$MTMOD_DEST_PATH"
#fi
#wget -O $MTMOD_SRC_ZIP https://github.com/Sokomine/mg_villages/archive/master.zip
#unzip "$MTMOD_SRC_ZIP"
#sudo mv $MTMOD_UNZ_NAME "$MTMOD_DEST_PATH"
#if [ ! -d "$MTMOD_DEST_PATH" ]; then
#  echo "ERROR: failed to unzip $MTMOD_DEST_PATH, so cannot continue."
#  exit 1
#fi


