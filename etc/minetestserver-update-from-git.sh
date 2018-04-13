#!/bin/sh


if [ -d "$HOME/Downloads/minetest" ]; then
  cd "$HOME/Downloads"
  cd minetest
  git pull
  if [ -d "games/minetest_game" ]; then
    cd games/minetest_game
    #echo "$(pwd):"
    echo "minetest_game:"
    git pull
    cd ../..
  else
    echo "skipping missing games/minetest_game"
  fi
  build_what="-DBUILD_SERVER=on -DBUILD_CLIENT=off"
  if [ "$1" = "both" ]; then
    build_what="-DBUILD_SERVER=on -DBUILD_CLIENT=on"
  elif [ "$1" = "client" ]; then
    build_what="-DBUILD_SERVER=off -DBUILD_CLIENT=on"
  fi
  cmake . -DENABLE_GETTEXT=on -DENABLE_CURSES=on -DENABLE_FREETYPE=on -DENABLE_LEVELDB=on -DENABLE_CURL=on -DENABLE_GETTEXT=on -DENABLE_REDIS=on -DENABLE_POSTGRESQL=on -DRUN_IN_PLACE=off -DCMAKE_BUILD_TYPE=Release $build_what

  make -j$(nproc)
  #cd games; git pull; make -j$(nproc)
  #git config global user.email ""
  #git config global user.name "expertmm"
  #git pull https://github.com/minetest/minetest_game.git
  #git fetch
  #git checkout HEAD games/minetest_game
  sudo make install
  USR_SHARE_MINETEST="/usr/local/share/minetest"
  MT_GAMES_DIR="$USR_SHARE_MINETEST/games"
  MT_MYGAME_DIR="$MT_GAMES_DIR/ENLIVEN"
  if [ -d "$MT_GAMES_DIR/minetest_game" ]; then
    if [ ! -d "$MT_GAMES_DIR/minetest_game" ]; then
      sudo mkdir -p "$MT_GAMES_DIR/minetest_game"
    fi
    if [ -d "$MT_MYGAME_DIR" ]; then
      echo "updating "
      sudo rsync -rtv "$HOME/Downloads/minetest/games/minetest_game/mods/" "$MT_MYGAME_DIR/mods/"
      if [ -d "$MT_MYGAME_DIR/mods/tsm_chests_dungeon" ]; then
        echo "REMOVING dungeon_loot since tsm_chests_dungeon is installed (even though more than one should work now since https://github.com/minetest/minetest/issues/6590 is resolved, dungeon_loot would be redundant in this case)..."
        sudo rm -Rf "$MT_MYGAME_DIR/mods/dungeon_loot"
      fi
    else
      echo "skipping update of components from minetest_game since does not exist: "
      echo "  $MT_MYGAME_DIR"
    fi
    echo "patching bones (this will not be needed after https://github.com/minetest/minetest_game/pull/2082 is merged)..."
    if [ -f "$MT_MYGAME_DIR/mods/bones/init.lua" ]; then
      cd "$MT_MYGAME_DIR/mods/bones"
      if [ -f init.bak ]; then
        sudo rm init.bak
      fi
      if [ -f init.1st ]; then
        sudo rm init.1st
      fi
      sudo mv init.lua init.bak
      sudo wget https://github.com/poikilos/minetest_game/raw/master/mods/bones/init.lua
      cd "$HOME/Downloads"
      if [ ! -d farming ]; then
        git clone https://github.com/tenplus1/farming.git
      else
        cd farming
        git pull
        cd ..
      fi
      sudo rm -Rf "$MT_MYGAME_DIR/mods/farming"
      sudo cp -Rf farming "$MT_MYGAME_DIR/mods/"
      sudo rm -Rf "$MT_MYGAME_DIR/mods/farming/.git"
      sudo rm "$MT_MYGAME_DIR/mods/farming/screenshot.png"
      sudo rm "$MT_MYGAME_DIR/mods/farming/.gitignore"
    else
      echo "ERROR: missing '$MT_MYGAME_DIR/mods/bones/init.lua'"
    fi
  else
    echo "WARNING: could not find $MT_GAMES_DIR/minetest_game"
  fi
else
  echo "ERROR: no minetest in $HOME/Downloads"
fi
