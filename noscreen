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
else
  cd ~/GitHub/EnlivenMinetest/webapp
fi

#js app.js
if [ -f "`command -v node`" ]; then
  node server.js
else
  js server.js
fi
