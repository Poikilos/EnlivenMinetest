#!/bin/sh
mountpoint=/media/flash
if [ ! -d "$mountpoint" ]; then
  sudo mkdir "$mountpoint"
  sudo mount /dev/sdb1 "$mountpoint"
  df -H
else
  echo "FAILED since already mounted at $mountpoint"
fi
