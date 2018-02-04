#!/usr/bin/env python3
import os
from mtanalyze.minetestinfo import *
import subprocess, signal
game_id = "ENLIVEN"
#screen -S MinetestServer $mts --gameid ENLIVEN --worldname FCAGameAWorld

if not minetestinfo.contains("minetestserver_path"):
    print("[ mtsenliven.py ] ERROR: minetestserver_path"
          "was not found in your version of minetestinfo.py")
    exit(1)

mts = minetestinfo.get_var("system.minetestserver_path")
if not minetestinfo.contains("primary_world_path"):
    print("[ mtsenliven.py ] ERROR: primary_world_path"
          "was selected by minetestinfo.py")
    exit(2)
wp = minetestinfo.get_var("primary_world_path")
wn = os.path.basename(wp)
p = subprocess.Popen([mts, '--gameid '+game_id, '--worldname '+wn])
                     # stdout=subprocess.PIPE)
