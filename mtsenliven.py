#!/usr/bin/env python3

# runs minetestserver using the paths defined by minetestinfo

import os
from mtanalyze.minetestinfo import *
import subprocess, signal
game_id = "ENLIVEN"
#screen -S MinetestServer $mts --gameid ENLIVEN --worldname FCAGameAWorld
print()
print()
print()

if not minetestinfo.contains("minetestserver_path"):
    print("[ mtsenliven.py ] ERROR: minetestserver_path"
          " was not found in your version of minetestinfo.py")
    exit(1)

mts = minetestinfo.get_var("minetestserver_path")
if not minetestinfo.contains("primary_world_path"):
    print("[ mtsenliven.py ] ERROR: primary_world_path"
          "was selected by minetestinfo.py")
    exit(2)
wp = minetestinfo.get_var("primary_world_path")
wn = os.path.basename(wp)
print("Using minetestserver: " + mts)
print("Using primary_world_path: " + wp)
print("Using world_name: " + wn)
print()
process = subprocess.Popen(
    [mts, '--gameid', game_id, '--worldname', wn],
    stdout=subprocess.PIPE
)

# see https://www.endpoint.com/blog/2015/01/28/getting-realtime-output-
# using-python
while True:
    output = process.stdout.readline()
    if output == '' and process.poll() is not None:
        break
    if output:
        # output is bytes
        print(output.decode("utf-8").strip())  # works on python2 or 3
    rc = process.poll()
