#!/bin/sh
sudo apt-get install python-numpy python-pil
cd ~
rm -f ~/minetestmapper-numpy.py
wget https://github.com/spillz/minetest/raw/master/util/minetestmapper-numpy.py
#since colors.txt is in ~/minetest/util:
mv minetestmapper-numpy.py ~/minetest/util/minetestmapper-numpy.py
cp 
# NOTE: colors.txt should ALREADY be in ~/minetest/util