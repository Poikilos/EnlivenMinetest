#!/bin/sh
sudo rm /var/log/mysql/error.log.*.gz
sudo rm /var/log/mysql/error.log.1
sudo rm /var/log/*.log.*.gz
sudo rm /var/log/*.log.1
