#!/bin/sh
# NOTE: only works since all scripts in /etc/cron.*/ or crontab run as root
python $HOME/chunkymap/generator.py --no-loop true


