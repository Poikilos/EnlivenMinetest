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
  #cd games; sudo git pull; sudo make -j$(nproc)
  #git config global user.email ""
  #git config global user.name "expertmm"
  #git pull https://github.com/minetest/minetest_game.git
  #sudo git fetch
  #sudo git checkout HEAD games/minetest_game
  sudo make install

  MT_GAMES_DIR="/usr/local/share/minetest/games"
  if [ -d "$MT_GAMES_DIR/minetest_game" ]; then
    if [ ! -d "$MT_GAMES_DIR/minetest_game" ]; then
      sudo mkdir -p "$MT_GAMES_DIR/minetest_game"
    fi
    MY_SUBGAME_PATH="$MT_GAMES_DIR/ENLIVEN"
    if [ -d "$MY_SUBGAME_PATH" ]; then
      echo "updating "
      sudo rsync -rtv "$HOME/Downloads/minetest/games/minetest_game/mods/" "$MY_SUBGAME_PATH/mods/"
    else
      echo "skipping update of components from minetest_game since does not exist: "
      echo "  $MY_SUBGAME_PATH"
    fi
  else
    echo "WARNING: could not find $MT_GAMES_DIR/minetest_game"
  fi
else
  echo "ERROR: no minetest in $HOME/Downloads"
fi
