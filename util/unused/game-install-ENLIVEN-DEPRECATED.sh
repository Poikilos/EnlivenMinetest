
echo "# STEPS BELOW ARE DEPRECATED"
echo
echo "## Deprecated since this travelnet is used instead"
echo "Also remember to:"
echo "  nano $MT_MYGAME_MODS_PATH/teleporter/config.lua"
echo "  #then change:"
echo "  teleporter.requires_pairing = true"
echo "  # also see other lines in this script that wouldn't echo as non-root"
echo "  #otherwise people can type any coordinates for destination (approaching infinite distance)!"
echo
echo "## Deprecated since using cme_to_spawners and tsm_pyramids_to_spawners from patches/mods-WIP"
echo "  * set number = 0 or number = {min=0, max=0} in cme since only using cme for creatures:*_spawner nodes and for compatibility with old worlds"

#UNUSED, and is based on a much older version of minetest_game:
#MTMOD_DL_ZIP=master.zip
#MTMOD_SRC_ZIP=carbone-ng.zip
#MTMOD_UNZ_NAME=carbone-ng-master
#MTMOD_DEST_NAME=carbone-ng
##MTMOD_DEST_PATH=$MT_MYGAME_MODS_PATH/$MTMOD_DEST_NAME
#MTMOD_DEST_PATH=$MT_GAMES_DIR/$MTMOD_DEST_NAME
#if [ ! -z "`ls | grep $MTMOD_UNZ_NAME`" ]; then  # works with wildcard in variable
#  rm -Rf $MTMOD_UNZ_NAME
#fi
#if [ -f "$MTMOD_DL_ZIP" ]; then
#  rm -f "$MTMOD_DL_ZIP"
#fi
#if [ -f "$MTMOD_SRC_ZIP" ]; then
#  rm -f "$MTMOD_SRC_ZIP"
#fi
#cd "$HOME/Downloads"
#wget https://github.com/Calinou/carbone-ng/archive/master.zip
#mv $MTMOD_DL_ZIP $MTMOD_SRC_ZIP
#unzip $MTMOD_SRC_ZIP
#sudo mv $MTMOD_UNZ_NAME "$MTMOD_DEST_PATH"
#if [ ! -d "$MTMOD_DEST_PATH" ]; then
#  echo "ERROR: failed to unzip $MTMOD_DEST_PATH, so cannot continue." > $err_txt
#  cat $err_txt
#  sleep 3
#  exit 1
#fi



#sudo cp -R /usr/share/games/minetest/games/carbone-ng /usr/local/share/minetest/games/carbone-ng

#IF git version is installed:
#if [ -d "/usr/local/share/minetest/games" ];
#then
#sudo cp -R $USR_SHARE_MINETEST/games/$MT_MYGAME_NAME /usr/local/share/minetest/games/$MT_MYGAME_NAME
#sudo mv $HOME/Downloads/cme /usr/local/share/minetest/games/$MT_MYGAME_NAME/mods/cme
#sudo mv $HOME/Downloads/protector /usr/local/share/minetest/games/$MT_MYGAME_NAME/mods/protector
#fi

# actually farming REDO as per https://forum.minetest.net/viewtopic.php?f=11&t=9019
#wget https://forum.minetest.net/download/file.php?id=5045
#mv "file.php?id=5045" farming.zip
#unzip farming.zip
#sudo rm -Rf $MT_MYGAME_MODS_PATH/farming
#sudo mv farming $MT_MYGAME_MODS_PATH/farming
# breaks 0.4.13 dev version 2016-02-17 (says height_max deprecated, use y_max; and later
#2016-02-17 11:10:19: ERROR[Main]: ModError: Failed to load and run script from $USR_SHARE_MINETEST/games/enliven/mods/farming/init.lua:
#2016-02-17 11:10:19: ERROR[Main]: ...share/minetest/games/enliven/mods/farming/pumpkin.lua:78: attempt to perform arithmetic on field 'LIGHT_MAX' (a nil value)
#2016-02-17 11:10:19: ERROR[Main]: stack traceback:
#2016-02-17 11:10:19: ERROR[Main]:       ...share/minetest/games/enliven/mods/farming/pumpkin.lua:78: in main chunk
#2016-02-17 11:10:19: ERROR[Main]:       [C]: in function 'dofile'
#2016-02-17 11:10:19: ERROR[Main]:       ...al/share/minetest/games/enliven/mods/farming/init.lua:65: in main chunk
# Remove & overwrite Farming REDO since it crashes 0.4.13 git 2016-02-16:
#sudo rm -Rf $MT_MYGAME_MODS_PATH/farming
#sudo cp -R $USR_SHARE_MINETEST/games/$mtgame_name/mods/farming $MT_MYGAME_MODS_PATH/farming

#ls "$MT_MYGAME_MODS_PATH"
if [ ! -d "$MT_BACKUP_GAMES_DIR" ]; then
  mkdir -p "$MT_BACKUP_GAMES_DIR"
#-p to make parent recursively
fi
first_suffix="_1st"
if [ -d "$MT_BACKUP_GAMES_DIR/$mtgame_name$first_suffix" ]; then
  echo "already backed up $USR_SHARE_MINETEST/games/$mtgame_name"
else
  sudo cp -R "$USR_SHARE_MINETEST/games/$mtgame_name" "$MT_BACKUP_GAMES_DIR/"
fi

#DEPRECATED, replaced by spawners (which includes pyramids worldgen mod)
#MTMOD_DL_ZIP=ebf839579197053b2ead85072757f23158960319.zip
#MTMOD_SRC_ZIP=tsm_pyramids.zip
#MTMOD_UNZ_NAME=tsm_pyramids-*
#MTMOD_DEST_NAME=tsm_pyramids
#MTMOD_DEST_PATH=$MT_MYGAME_MODS_PATH/$MTMOD_DEST_NAME
#if [ ! -z "`ls | grep $MTMOD_UNZ_NAME`" ]; then  # works with wildcard in variable
#  rm -Rf $MTMOD_UNZ_NAME
#fi
#if [ -f "$MTMOD_DL_ZIP" ]; then
#  rm -f "$MTMOD_DL_ZIP"
#fi
#if [ -f "$MTMOD_SRC_ZIP" ]; then
#  rm -f "$MTMOD_SRC_ZIP"
#fi
#wget http://repo.or.cz/w/minetest_pyramids/tsm_pyramids.git/snapshot/ebf839579197053b2ead85072757f23158960319.zip
#mv $MTMOD_DL_ZIP $MTMOD_SRC_ZIP
#unzip $MTMOD_SRC_ZIP
#sudo mv -f $MTMOD_UNZ_NAME "$MTMOD_DEST_PATH"
#if [ ! -d "$MTMOD_DEST_PATH" ]; then
#  echo "ERROR: failed to unzip $MTMOD_DEST_PATH, so cannot continue." > $err_txt
#  cat $err_txt
#  sleep 3
#  exit 1
#fi
# AKA http://repo.or.cz/minetest_pyramids.git

#an old version of worldedit included in a minetest fork last updated 2016:
#MTMOD_DL_ZIP=akiba-*
#wget http://git.akiba.fr:81/minetest/akiba/repository/archive.zip?ref=af571404a27a2cb06842c644930344f565a0b786
#rm -f $MTMOD_DL_ZIP

if [ ! -d "$MT_MYGAME_MODS_PATH/hudbars" ]; then
    cd "$HOME/Downloads"
    #MTMOD_DL_ZIP=hud_hunger-2_x_1-BlockMen.zip
    #MTMOD_SRC_ZIP=hud_hunger-2_x_1-BlockMen.zip
    MTMOD_DL_ZIP=master.zip
    MTMOD_SRC_ZIP=hud_hunger.zip
    MTMOD_UNZ_NAME=hud_hunger
    MTMOD_DEST_NAME=hud_hunger
    MTMOD_DEST_PATH=$MT_MYGAME_MODS_PATH/$MTMOD_DEST_NAME
    #in case someone installed the mods apart from the modpack:
    if [ -d "$MT_MYGAME_MODS_PATH/hud" ]; then
      sudo rm -Rf "$MT_MYGAME_MODS_PATH/hud"
    fi
    if [ -d "$MT_MYGAME_MODS_PATH/hunger" ]; then
      sudo rm -Rf "$MT_MYGAME_MODS_PATH/hunger"
    fi
    if [ -f $MTMOD_DL_ZIP ]; then
      rm -f $MTMOD_DL_ZIP
    fi
    if [ -f $MTMOD_SRC_ZIP ]; then
      rm -f $MTMOD_SRC_ZIP
    fi
    rm -Rvf $MTMOD_UNZ_NAME
    #BlockMen's is not maintained, & has problem on hud/buildin line 79 (crash since air can be nil)
    #wget https://github.com/BlockMen/hud_hunger/releases/download/2.x.1/hud_hunger-2_x_1-BlockMen.zip
    #FozLand's has a couple fixes
    #wget https://github.com/FozLand/hud_hunger/archive/master.zip
    #tenplus1's fixes nil air, nil player, and sprint
    wget https://github.com/tenplus1/hud_hunger/archive/master.zip
    unzip $MTMOD_SRC_ZIP
    sudo mv $MTMOD_UNZ_NAME "$MTMOD_DEST_PATH"
    sudo rm "$MTMOD_DEST_PATH/hunger/functions_UNUSED_sprint.lua"
    sudo mv "$MTMOD_DEST_PATH/hunger/functions.lua" "$MTMOD_DEST_PATH/hunger/functions_UNUSED_sprint.lua"
    sudo mv "$MTMOD_DEST_PATH/hunger/functions_(nosprint).lua" "$MTMOD_DEST_PATH/hunger/functions.lua"
    sudo rm "$MTMOD_DEST_PATH/hunger/init_UNUSED_sprint.lua"
    sudo mv "$MTMOD_DEST_PATH/hunger/init.lua" "$MTMOD_DEST_PATH/hunger/init_UNUSED_sprint.lua"
    sudo mv "$MTMOD_DEST_PATH/hunger/init_(nosprint).lua" "$MTMOD_DEST_PATH/hunger/init.lua"
    if [ ! -d "$MTMOD_DEST_PATH" ]; then
      echo "ERROR: failed to unzip $MTMOD_DEST_PATH, so cannot continue." > $err_txt
      cat $err_txt
      sleep 3
      exit 1
    fi
    # END IF no hudbars mod
    else
    if [ -d "$MT_MYGAME_MODS_PATH/hud_hunger" ]; then
    sudo rm -Rvf "$MT_MYGAME_MODS_PATH/hud_hunger"
    fi
fi


MTMOD_SRC_ZIP=treasurer0.2.0.zip
MTMOD_UNZ_NAME=treasurer
MTMOD_DEST_NAME=treasurer
MTMOD_DEST_PATH=$MT_MYGAME_MODS_PATH/$MTMOD_DEST_NAME
if [ -f "tsm_gift_example" ]; then
  rm "tsm_gift_example"
fi
if [ -d "tsm_gift_example" ]; then
  rm -Rf "tsm_gift_example"
fi
if [ -d "tsm_chests_example" ]; then
  rm -Rf "tsm_chests_example"
fi
if [ -d "trm_default_example" ]; then
  rm -Rf "trm_default_example"
fi
if [ -d "tsm_default_example" ]; then
  rm -Rf "tsm_default_example"
fi
if [ ! -z "`ls | grep $MTMOD_UNZ_NAME`" ]; then  # works with wildcard in variable
  rm -Rf $MTMOD_UNZ_NAME
fi
if [ -f "$MTMOD_SRC_ZIP" ]; then
  rm -f "$MTMOD_SRC_ZIP"
fi
wget -O $MTMOD_SRC_ZIP http://axlemedia.net/abiyahh/users/Wuzzy/downloads/treasurer0.2.0.zip
unzip $MTMOD_SRC_ZIP
sudo mv -f $MTMOD_UNZ_NAME "$MTMOD_DEST_PATH"
if [ ! -d "$MTMOD_DEST_PATH" ]; then
  echo "ERROR: failed to unzip $MTMOD_DEST_PATH, so cannot continue." > $err_txt
  cat $err_txt
  echo "  press Ctrl C to cancel ENLIVEN install or this terminal will close..."
  sleep 1
  echo " 3..."
  sleep 1
  echo " 2..."
  sleep 1
  echo " 1..."
  sleep 1
  exit 1
fi

# EXTRA FONTS PACK for signs_lib DOESN'T SEEM TO WORK IN MULTIPLAYER, and is unwieldy to use:
#cd $HOME/Downloads
#MTMOD_DL_ZIP=master.zip
#MTMOD_SRC_ZIP=minetest-signs_lib-extrafonts.zip
#MTMOD_UNZ_NAME=minetest-signs_lib-extrafonts-master
#MTMOD_DEST_NAME=signs_lib/textures
#MTMOD_DEST_PATH=$MT_MYGAME_MODS_PATH/$MTMOD_DEST_NAME
#if [ ! -z "`ls | grep $MTMOD_UNZ_NAME`" ]; then  # works with wildcard in variable
#  rm -Rf $MTMOD_UNZ_NAME
#fi
#if [ -f $MTMOD_DL_ZIP ]; then
#  rm -f $MTMOD_DL_ZIP
#fi
#if [ -f $MTMOD_SRC_ZIP ]; then
#  rm -f $MTMOD_SRC_ZIP
#fi
#if [ -d "$MTMOD_DEST_PATH" ]; then
#  sudo rm -Rf "$MTMOD_DEST_PATH"
#fi
#wget https://github.com/kaeza/minetest-signs_lib-extrafonts/archive/master.zip
#mv $MTMOD_DL_ZIP "$MTMOD_SRC_ZIP"
#unzip "$MTMOD_SRC_ZIP"
##sudo cp -f $MTMOD_UNZ_NAME/15px/* "$MTMOD_DEST_PATH/"
#sudo cp -f $MTMOD_UNZ_NAME/31px/* "$MTMOD_DEST_PATH/"
#if [ ! -d "$MTMOD_DEST_PATH" ]; then
#  echo "ERROR: failed to unzip $MTMOD_DEST_PATH, so cannot continue." > $err_txt
#  cat $err_txt
#  echo "  press Ctrl C to cancel ENLIVEN install or this terminal will close..."
#  sleep 1
#  echo " 3..."
#  sleep 1
#  echo " 2..."
#  sleep 1
#  echo " 1..."
#  sleep 1
#  exit 1
#fi

#https://forum.minetest.net/viewtopic.php?t=14359
#This mod is part of minetest_game 0.4.15!
#TODO: With exception of the wieldlight
#add_git_mod torches torches https://github.com/BlockMen/torches.git

# This mod is part of minetest_game 0.4.15!
# add_git_mod moresnow moresnow https://github.com/Sokomine/moresnow

# no longer needed since ENLIVEN main branch now uses poikilos travelnet:
# add_git_mod travelnet travelnet https://github.com/Sokomine/travelnet.git
