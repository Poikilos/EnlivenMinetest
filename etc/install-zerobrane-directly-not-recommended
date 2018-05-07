#!/bin/bash
archive_name=ZeroBraneStudioEduPack-1.70-linux.sh
cd "$HOME"
if [ ! -d "Downloads" ]; then
  mkdir Downloads
fi
cd Downloads
if [ ! -f "$archive_name" ]; then
  wget -O $archive_name https://download.zerobrane.com/$archive_name
fi
sudo sh "$archive_name"
echo
echo "You can donate to the ZeroBrane Studio project at https://studio.zerobrane.com/support"
echo "  (using that URL when linking to ZeroBrane Studio is most courteous to the project)."
echo
