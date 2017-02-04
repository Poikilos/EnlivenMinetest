#!/bin/sh
mountpoint=/media/flash
if [ -d /media/flash ]; then
  sudo umount /media/flash
  #ok since does NOT remove unless empty:
  sudo rmdir "$mountpoint"
else
echo "Nothing to do: nothing was mounted at $mountpoint"
fi
