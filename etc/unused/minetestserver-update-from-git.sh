#!/bin/sh
cd
cd minetest; sudo git pull; sudo make -j$(nproc)
#cd games; sudo git pull; sudo make -j$(nproc)
#git config global user.email "tertiary@axlemedia.net"
#git config global user.name "Expert Multimedia"
sudo git pull https://github.com/minetest/minetest_game.git
#sudo git fetch
#sudo git checkout HEAD games/minetest_game
#sudo make install