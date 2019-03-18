#!/bin/sh

date_string=`date +%Y-%m-%d`
MT_WORLDS_PATH=/home/owner/.minetest/worlds
cd $MT_WORLDS_PATH
ls
dest_name=FCAGameAWorld-$date_string.tar.gz
dest_path=$MT_WORLDS_PATH/$dest_name
echo "Attempting to create $name_string"
if [ ! -f "$name_string" ]
  then
  cd "$MT_WORLDS_PATH"
  tar -czvf "$dest_name" FCAGameAWorld
  if [ -f "$dest_path" ]
    then
    echo "Successfully created $dest_path" > $HOME/backup-FCAGAW-result.txt >> /var/log/minetestserver-scripts.log
  else
    echo "Failed to create $dest_path" > $HOME/backup-FCAGAW-result.txt >> /var/log/minetestserver/scripts.log
  fi
else
  echo "Nothing to do. Already saved $MT_WORLDS_PATH/$name_string" >> /var/log/minetestserver-scripts.log
fi
