#!/bin/sh

#This is a systemd startup unit, and will only work if your system is running systemd
#(see https://wiki.ubuntu.com/SystemdForUpstartUsers or https://www.freedesktop.org/software/systemd/man/systemd.service.html
# and https://www.freedesktop.org/software/systemd/man/systemd.exec.html# --discusses execution options such as User)
#* Ignores invalid directives and starts the service ...
#  systemd-analyze verify <unit> file to get warnings on typos and badly formatted options.
#* requires full path, so ExecStart=/bin/sleep 20 works but ExecStart=sleep 20 does not.
#* custom system-wide scripts go in /etc/systemd/system/, builtin services which reside in /usr/lib/systemd/system/ (and custom ones may override system-wide ones)

## Known Issues
# * should use machinectl shell instead of su or sudo as of 2016 updates to systemd
# * Restart=on-abort and RestartSec=3 settings could be used (but probably shouldn't, so minetest crash can be noticed [and debugged more easily by viewing tail of debug log])
# * Maybe for ExecStart, instead use:
#   su owner "screen -S MinetestServer /home/owner/minetest/bin/minetestserver --gameid ENLIVEN --worldname FCAGameAWorld"
#   OR
#   sudo -u owner screen -S MinetestServer /home/owner/minetest/bin/minetestserver --gameid ENLIVEN --worldname FCAGameAWorld
#   instead of User=owner

#Update the unit:
cd $HOME/Downloads
if [ -f mts-ENLIVEN.service ]; then
#clear old downloaded copy if exists in userspace
rm mts-ENLIVEN.service
fi
wget https://github.com/poikilos/EnlivenMinetest/raw/master/etc/change_hardcoded_world_and_username_manually_first/mts-ENLIVEN.service
echo "This will only work if you are using systemd."
sudo mv -f mts-ENLIVEN.service /etc/systemd/system/
#sudo chmod +x /etc/systemd/system/mts-ENLIVEN.service
sudo chmod 644 /etc/systemd/system/mts-ENLIVEN.service
#644 since should not be executable ( 1 is the executable flag bit )
sudo chown root /etc/systemd/system/mts-ENLIVEN.service
sudo chgrp root /etc/systemd/system/mts-ENLIVEN.service
#? sudo mv -f mts-ENLIVEN.service /etc/systemd/system/
#enable the mts-ENLIVEN systemd service on Ubuntu:
#sudo service mts-ENLIVEN enable
#sudo service mts-ENLIVEN start
sudo systemctl enable mts-ENLIVEN
sudo systemctl start mts-ENLIVEN

#VIEW STATUS LIKE:
#sudo journalctl -u mts-ENLIVEN
##OR
#sudo systemctl status mts-ENLIVEN
#(press q to exit)
