#!/bin/sh
#BROKEN: screen -t MinetestServer minetestserver --gameid minetest_next --draworigin --drawplayers --world FCAWorldMTNext
#BROKEN: screen -t MinetestServer minetestserver --gameid ENLIVEN --worldname FCAGameAWorld
#NOTE: if only title is set, screen -x must be used to resume, so use -S <name> to resume with -r <name>
#screen -S MinetestServer minetestserver --gameid ENLIVEN --worldname FCAGameAWorld
#screen -S MinetestServer /home/owner/minetest/bin/minetestserver --gameid ENLIVEN --worldname FCAGameAWorld
if [ -d ~/Applications/EnlivenMinetest/webapp ]; then
  cd ~/Applications/EnlivenMinetest/webapp
elif [ -d ~/Documents/EnlivenMinetest/webapp ]; then
  cd ~/Documents/GitHub/EnlivenMinetest/webapp
elif [ -d ~/GitHub/EnlivenMinetest/webapp ]; then
  cd ~/GitHub/EnlivenMinetest/webapp
elif [ -d webapp ]; then
  cd webapp
else
  echo "FAILED to find webapp directory in EnlivenMinetest"
fi

node_bin="echo"
if [ `which node` ]; then
  node_bin="node"
  echo "detected node.js command: $node_bin"
elif [ `which js` ]; then
  node_bin="js"
  echo "detected node.js command: $node_bin"
else
  echo "ERROR: Nothing to do since could not find a node or js command!"
  exit 1
fi

#js app.js
if [ ` which screen` ]; then
  screen -S EnlivenMinetest $node_bin server.js
else
  echo "WARNING: no screen command so running directly in this session..."
  echo "3..."
  sleep 1
  echo "2..."
  sleep 1
  echo "1..."
  sleep 1
  $node_bin server.js
fi
