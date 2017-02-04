#!/bin/sh
#deb http://ppa.launchpad.net/minetestdevs/stable/ubuntu trusty main 
#deb-src http://ppa.launchpad.net/minetestdevs/stable/ubuntu trusty main 
sudo add-apt-repository ppa:minetestdevs/stable
sudo apt-get update
sudo apt-get install minetest-server
sudo ufw allow 30000