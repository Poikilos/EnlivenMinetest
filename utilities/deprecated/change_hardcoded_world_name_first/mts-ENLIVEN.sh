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
screen -S MinetestServer $mts --gameid ENLIVEN --worldname $MT_MYWORLD_NAME

