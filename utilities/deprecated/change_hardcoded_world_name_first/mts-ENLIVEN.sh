#!/bin/sh
echo "WARNING: mts-ENLIVEN script is deprecated--instead, run:"
try_path="./GitHub/EnlivenMinetest/mtsenliven.py"
if [ -f "$try_path" ]; then
  echo "  python3 $try_path"
else
  try_path="$HOME/GitHub/EnlivenMinetest/mtsenliven.py"
  if [ -f "$try_path" ]; then
    echo "  python3 $try_path"
  else
    echo "  python3 mtsenliven.py"
  fi
fi
# sleep 4
# exit 1
mts=minetestserver
if [ ! -f "`command -v minetestserver`" ]; then
  try_path="$HOME/minetest/bin/minetestserver"
  if [ -f "$try_path" ]; then
    mts="$try_path"
  fi
fi
# BROKEN: screen -t MinetestServer minetestserver --gameid minetest_next --draworigin --drawplayers --world FCAWorldMTNext
# BROKEN: screen -t MinetestServer minetestserver --gameid ENLIVEN --worldname FCAGameAWorld
# NOTE: if only title is set, screen -x must be used to resume, so use -S <name> to resume with -r <name>
# screen -S MinetestServer minetestserver --gameid ENLIVEN --worldname FCAGameAWorld
# screen -S MinetestServer /home/owner/minetest/bin/minetestserver --gameid ENLIVEN --worldname FCAGameAWorld
MT_MYWORLD_NAME="FCAWorldB"
MT_MYWORLD_DIR="$HOME/.minetest/worlds/$MT_MYWORLD_NAME"
WORLD_MT_PATH="$MT_MYWORLD_DIR/world.mt"
if [ ! -d "$MT_MYWORLD_DIR" ]; then
  echo "ERROR: Nothing to do since missing $MT_MYWORLD_DIR"
  exit 1
fi
if grep -q "backend =" "$WORLD_MT_PATH"; then
  echo "backends:"
  cat $WORLD_MT_PATH | grep backend
else
  if [ -d "$MT_MYWORLD_DIR/map.db" ]; then
    echo "ERROR: Nothing to do since map.db was found but there is no backend specified in $WORLD_MT_PATH:"
    cat "$WORLD_MT_PATH"
    exit 1
  else
    cat "WARNING: no backend specified in $WORLD_MT_PATH"
    echo "3..."
    sleep 1
    echo "2..."
    sleep 1
    echo "1..."
    sleep 1
  fi
fi

# screen -S MinetestServer $mts --gameid Bucket_Game --worldname $MT_MYWORLD_NAME
# screen -S MinetestServer $mts --gameid ENLIVEN --worldname $MT_MYWORLD_NAME
# minetestserver options:
# --worldname <world must be in normal worlds directory>
# --world <any world directory can be specified>
# --config <any minetest.conf>
# cmd="$mts --gameid ENLIVEN --world /home/owner/.minetest/worlds/$MT_MYWORLD_NAME --config /home/owner/minetest/games/ENLIVEN/minetest.conf"
cmd="$mts --gameid ENLIVEN --world /home/owner/.minetest/worlds/$MT_MYWORLD_NAME"
enable_screen=true
if [ -z "$screen_cmd" ]; then
    if [ -f "`command -v screen`" ]; then
        screen_cmd="screen"
    else
        enable_screen=false
    fi
fi

if [ "@$1" = "@--noscreen" ]; then
    enable_screen=false
fi
if [ "@$enable_screen" = "@true" ]; then
    if [ "@$screen_cmd" = "@screen" ]; then
        screen -S MinetestServer $cmd
    else
        echo "Syntax for $screen_cmd is not implemented, so falling back to:"
        echo "    $screen_cmd $cmd"
        $screen_cmd $cmd
    fi
    echo "$screen_cmd finished running $cmd"
else
    echo "Running minetestserver without screen command..."
    $cmd
    echo "$cmd  # finished."
fi

