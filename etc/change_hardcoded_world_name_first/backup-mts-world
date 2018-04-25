#!/bin/sh
# Copyright 2017 poikilos
# Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:
# The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

MT_WORLDS_PATH=$HOME/.minetest/worlds
WORLD_NAME=FCAWorldB
WORLD_PATH=$MT_WORLDS_PATH/$WORLD_NAME
MT_MYWORLD_ENV_META_PATH="$WORLD_PATH/env_meta.txt"
MT_MYWORLD_ENV_META_BAK_PATH="$WORLD_PATH/env_meta.bak"
echo
echo
if [ ! -d "$HOME/Backup" ]; then
  mkdir "$HOME/Backup"
fi

date_string=`date +%Y-%m-%d`
cd $MT_WORLDS_PATH
ls

echo "Making in-place copy of env_meta.txt if good..."
actualsize=$(stat -c%s "$MT_MYWORLD_ENV_META_PATH")
#minsize should actually be more but this should do:
minsize=2
if [ $actualsize -ge $minsize ]; then
    cp -f "$MT_MYWORLD_ENV_META_PATH" "$MT_MYWORLD_ENV_META_BAK_PATH"
    echo "  copied to $MT_MYWORLD_ENV_META_BAK_PATH"
else
    echo "  skipping bad $MT_MYWORLD_ENV_META_PATH"
fi

dated_name=$WORLD_NAME-$date_string.tar.gz
echo "Attempting to create $dated_name..."
if [ ! -f "$dated_name" ]; then
  tar -czvf "$dated_name" $WORLD_NAME
  dest_path=$HOME/Backup/$dated_name
  if [ -f $dated_name ]; then
    mv -f "$dated_name" "$HOME/Backup/"
  fi
  if [ -f "$dest_path" ]; then
    echo "  successfully created and moved to $dest_path"
  else
    echo "  failed to create $MT_WORLDS_PATH/$dated_name"
  fi
else
  echo "  nothing to do since already saved $MT_WORLDS_PATH/$dated_name"
fi
echo
