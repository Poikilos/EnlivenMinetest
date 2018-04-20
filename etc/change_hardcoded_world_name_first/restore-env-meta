#!/bin/sh
MT_WORLDS_PATH=$HOME/.minetest/worlds
WORLD_NAME=FCAWorldB
WORLD_PATH=$MT_WORLDS_PATH/$WORLD_NAME
MT_MYWORLD_ENV_META_PATH="$WORLD_PATH/env_meta.txt"
MT_MYWORLD_ENV_META_BAK_PATH="$WORLD_PATH/env_meta.bak"

actualsize=$(stat -c%s "$MT_MYWORLD_ENV_META_PATH")
#minsize should actually be more but this should do:
minsize=2
if [ $actualsize -ge $minsize ]; then
    echo "WARNING: nothing done since already non-zero-sized $MT_MYWORLD_ENV_META_PATH"
    exit 0
fi


if [ -f "$MT_MYWORLD_ENV_META_BAK_PATH" ]; then
  mv -f "$MT_MYWORLD_ENV_META_BAK_PATH" "$MT_MYWORLD_ENV_META_PATH"
else
  echo "ERROR: nothing done since there is no $MT_MYWORLD_ENV_META_BAK_PATH (would be created by backup-mts-world if ran when source was non-zero-size)"
fi
