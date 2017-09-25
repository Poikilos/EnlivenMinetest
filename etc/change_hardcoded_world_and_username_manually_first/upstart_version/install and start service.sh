#!/bin/sh

echo "This doesn't work on Xenial since Ubuntu switched from Canonical upstart to systemd (unless you manually switched to upstart)"
wget https://github.com/expertmm/EnlivenMinetest/raw/master/etc/change_hardcoded_username_first/upstart_version/etc/init.d/mts-ENLIVEN.conf
sudo mv -f mts-ENLIVEN.conf /etc/init.d/
#enable the mts-ENLIVEN upstart service on Ubuntu:
sudo service mts-ENLIVEN enable
sudo service mts-ENLIVEN start
