#!/bin/bash
dls_path="$HOME/Downloads"
dl_name="MinetestIDEvers1(dot)0.zip"
dl_path="$dls_path/$dl_name"
if [ ! -f "$dl_path" ]; then
  echo "ERROR: Nothing done since you must first download $dl_name from"
  echo "  https://forum.minetest.net/viewtopic.php?f=14&t=12923"
  echo "  such that it exists as $dl_path"
  echo "Press Ctrl C to cancel otherwise this terminal will exit..."
  echo "3..."
  sleep 1
  echo "2..."
  sleep 1
  echo "1..."
  sleep 1
  exit 1
fi
share_path=/opt/zbstudio
try_path=/usr/share/zbstudio
if [ -d "$try_path/api" ]; then
  share_path="$try_path"
elif [ ! -d "$share_path" ]; then
  echo "Neither $share_path nor $try_path was found."
  echo "  Make sure ZeroBrane is installed, or modify share_path in this script."
  echo "  https://studio.zerobrane.com/support"
  echo "Press Ctrl C to cancel otherwise this terminal will exit..."
  echo "3..."
  sleep 1
  echo "2..."
  sleep 1
  echo "1..."
  sleep 1
  exit 2
fi
cd "$dls_path"
zb_tmp_name="tmp_zb_minetest"
if [ -d "$zb_tmp_name" ]; then
  rm -Rf "$zb_tmp_name"
fi
mkdir "$zb_tmp_name"
cd "$zb_tmp_name"
unzip ../$dl_name
cd ..
sudo cp -Rf $zb_tmp_name/* "$share_path/"
echo "You must close ZeroBrain Studio (if open) for this to take effect."
echo
echo
echo "(For each project) after opening your lua file, click:"
echo "  * Project"
echo "  * Lua Interpreter"
echo "  * minetest"
echo
sleep 4
