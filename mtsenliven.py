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
process = None
try:
    # get both stdout and stderr (see
    # https://www.saltycrane.com/blog/2008/09/how-get-stdout-and-
    # stderr-using-python-subprocess-module/)
    process = subprocess.Popen(
        [mts, '--gameid', game_id, '--worldname', wn],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )
except:
    print(mts + " could not be executed. Try installing the "
          " minetest-server package or compiling from git instructions"
          " on minetest.net")
    exit(1)
msg_flags = ["WARNING[Server]: ", "ACTION[Server]: "]
msg_lists = {}  # where flag is key
for flag in msg_flags:
    msg_lists[flag] = []
# see https://www.endpoint.com/blog/2015/01/28/getting-realtime-output-
# using-python

def print_unique_only(output):
    output_strip = output.strip()
    # (out_bytes is bytes)
    show_enable = True
    found_flag = None
    f_i = None
    for flag in msg_flags:
    # such as '2018-02-06 21:08:06: WARNING[Server]: Deprecated call to get_look_yaw, use get_look_horizontal instead'
    # or 2018-02-06 21:08:05: ACTION[Server]: [playereffects] Wrote playereffects data into /home/owner/.minetest/worlds/FCAGameAWorld/playereffects.mt.
        f_i = output.find(flag)
        if f_i >= 0:
            found_flag = flag
            break
    if found_flag:
        sub_msg = output[f_i+len(flag):].strip()
        if sub_msg in msg_lists[found_flag]:
            show_enable = False
        else:
            msg_lists[found_flag].append(sub_msg)
    if show_enable:
        print(output_strip)
        if found_flag is not None:
            print("[ mtsenliven.py ] INFO: this is the last"
                  " time the message above will be shown")

def process_msg(bstring):
    output = bstring.decode("utf-8")
            # works on python2 or 3
    print_unique_only(output)


while True:
    try:
        # out_bytes = process.stdout.readline()
        # err_bytes = process.stderr.readline()
        out_bytes, err_bytes = p.communicate()
        if (out_bytes == '') and \
           (err_bytes == '') and \
           (process.poll() is not None):
            break
        if out_bytes:
            process_msg(out_bytes)
        if err_bytes:
            process_msg(err_bytes)
        rc = process.poll()
    except KeyboardInterrupt:
        break
