#!/bin/sh
sudo su -
# NOTE: this works only since user is a field on Ubuntu (on some GNU/Linux systems it is not, which is implied by omission at http://www.adminschoice.com/crontab-quick-reference)
# Minute, Hour, Day of Month, Month (1 to 12), Day of Week
# m h dom mon dow user command
echo "* * * * * root /home/owner/minetest/utils/chunkymap-cronjob" >> /etc/crontab