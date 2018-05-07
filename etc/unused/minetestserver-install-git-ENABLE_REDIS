#!/bin/bash
#sudo apt-get install libncurses5-dev libgettextpo-dev doxygen libspatialindex-dev lua-redis-dev gettext

sudo apt-get install build-essential cmake git libirrlicht-dev libbz2-dev libgettextpo-dev libfreetype6-dev libpng12-dev libjpeg8-dev libxxf86vm-dev libgl1-mesa-dev libsqlite3-dev libogg-dev libvorbis-dev libopenal-dev libhiredis-dev libcurl3-dev
#above is from http://dev.minetest.net/Compiling_Minetest#Compiling_on_GNU.2FLinux

#as per <https://www.digitalocean.com/community/tutorials/how-to-configure-a-redis-cluster-on-ubuntu-14-04>:
#this ppa doesn't work anymore (tested 2017-04)
#sudo add-apt-repository ppa:chris-lea/redis-server
sudo apt-get update
sudo apt-get install redis-server


#if you skip the above, the below says missing: GetText, Curses, ncurses, Redis, SpatialIndex, Doxygen
#cd "$HOME"  #done below by parameterless "cd" command
sudo apt-get install -y git build-essential libirrlicht-dev libgettextpo0 libfreetype6-dev cmake libbz2-dev libpng12-dev libjpeg8-dev libxxf86vm-dev libgl1-mesa-dev libsqlite3-dev libogg-dev libvorbis-dev libopenal-dev libcurl4-openssl-dev libluajit-5.1-dev liblua5.1-0-dev libleveldb-dev; cd; git clone https://github.com/minetest/minetest.git; cd minetest/games; git clone https://github.com/minetest/minetest_game.git; cd ..; cmake . -DENABLE_GETTEXT=1 -DENABLE_FREETYPE=1 -DENABLE_LEVELDB=1 -DENABLE_REDIS=1 -DBUILD_SERVER=TRUE -DBUILD_CLIENT=FALSE; make -j$(nproc); sudo make install;
# minetest;
echo -e "\n\n\e[1;33mYou can run Minetest Server by typing \"minetestserver\" in a terminal.\e[0m"
echo "Remember to add requirepass to /etc/redis/redis.conf -- a long password since redis is fast and can be bruteforced quickly"
# based on https://forum.minetest.net/viewtopic.php?f=42&t=3837 (below)
# sudo apt-get install -y git build-essential libirrlicht-dev libgettextpo0 libfreetype6-dev cmake libbz2-dev libpng12-dev libjpeg8-dev libxxf86vm-dev libgl1-mesa-dev libsqlite3-dev libogg-dev libvorbis-dev libopenal-dev libcurl4-openssl-dev libluajit-5.1-dev liblua5.1-0-dev libleveldb-dev; cd; git clone https://github.com/minetest/minetest.git; cd minetest/games; git clone https://github.com/minetest/minetest_game.git; cd ..; cmake . -DENABLE_GETTEXT=1 -DENABLE_FREETYPE=1 -DENABLE_LEVELDB=1 -DENABLE_REDIS=1; make -j$(nproc); sudo make install; minetest; echo -e "\n\n\e[1;33mYou can run Minetest again by typing \"minetest\" in a terminal or selecting it in an applications menu.\nYou can install mods in ~/.minetest/mods, too.\e[0m"
