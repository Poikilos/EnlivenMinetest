#!/bin/sh
cd ~/minetest-stuff
rm master.zip
wget https://github.com/expertmm/minetest-chunkymap/archive/master.zip
mv master.zip minetest-chunkymap.zip
unzip minetest-chunkymap.zip
mv minetest-chunkymap-master minetest-chunkymap
cd minetest-chunkymap
chmod +x install-chunkymap-on-ubuntu.sh
./install-chunkymap-on-ubuntu.sh