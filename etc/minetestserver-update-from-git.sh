#!/bin/sh


if [ -d "$HOME/Downloads/minetest" ]; then
  cd "$HOME/Downloads"
  cd minetest; git pull; make -j$(nproc)
  #cd games; sudo git pull; sudo make -j$(nproc)
  #git config global user.email ""
  #git config global user.name "expertmm"
  git pull https://github.com/minetest/minetest_game.git
  #sudo git fetch
  #sudo git checkout HEAD games/minetest_game
  #sudo make install
else
  echo "ERROR: no minetest in $HOME/Downloads"
fi
