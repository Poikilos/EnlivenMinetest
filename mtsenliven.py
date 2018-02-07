#!/usr/bin/env python3

# runs minetestserver using the paths defined by minetestinfo
# NOTE: SIGINT (as opposed to KILL) makes sure minetest server
#   shuts down properly (makes sure all processes finish) according to
#   dr4Ke on
#   https://forum.minetest.net/viewtopic.php?f=11&t=13138&start=50
key_exit_msg = "SIGINT should shut down server safely...\n"
import os
from mtanalyze.minetestinfo import *
try:
    from Threading import thread as Thread # Python 2
except:
    from threading import Thread # Python 3
# if sys.version[0] == '2':
try:
    from Queue import Queue # Python 2
except:
    from queue import Queue # Python 3
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
        stderr=subprocess.PIPE,
        bufsize=1
    )
    #bufsize=1 as per jfs on https://stackoverflow.com/questions/31833897/python-read-from-subprocess-stdout-and-stderr-separately-while-preserving-order
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

non_unique_wraps = []
non_unique_wraps.append(
    {
        "opener":"active block modifiers took ",
        "closer":"ms (longer than 200ms)"
    }
)

unique_flags = [
    "leaves game",
    "joins game"
]

def print_unique_only(output, err_flag=False):
    output_strip = output.strip()
    u_prefix = "active block modifiers took "
    u_suffix = "ms (longer than 200ms)"
    # (out_bytes is bytes)
    show_enable = True
    found_flag = None
    f_i = None
    always_show_enable = False
    msg_msg = "previous message"
    for flag in unique_flags:
        if flag in output:
            always_show_enable = True
    if not always_show_enable:
        for flag in msg_flags:
        # such as '2018-02-06 21:08:06: WARNING[Server]: Deprecated call to get_look_yaw, use get_look_horizontal instead'
        # or 2018-02-06 21:08:05: ACTION[Server]: [playereffects] Wrote playereffects data into /home/owner/.minetest/worlds/FCAGameAWorld/playereffects.mt.
            f_i = output.find(flag)
            if f_i >= 0:
                found_flag = flag
                break
        if found_flag:
            sub_msg = output[f_i+len(flag):].strip()
            for wrap in non_unique_wraps:
                if wrap["opener"] in sub_msg and wrap["closer"] in sub_msg:
                    sub_msg = wrap["opener"] + "..." + wrap["closer"]
                    msg_msg = "similar messages"
                    break
            if sub_msg in msg_lists[found_flag]:
                show_enable = False
            else:
                msg_lists[found_flag].append(sub_msg)
    if show_enable:
        print(output_strip)
        if found_flag is not None:
            print("  [ mtsenliven.py ] " + msg_msg
                  + " will be suppressed")

def process_msg(bstring):
    output = bstring
    err_flag = False
    try:
        output = bstring.decode("utf-8")
                # works on python2 or 3
    except AttributeError:
        output = bstring
    if output[:1] == "<":
        stop_s = ">: "
        closer_i = output.find(stop_s)
        if closer_i >= 0:
            next_i = closer_i + len(stop_s)
            err_flag = True
            output = output[next_i:]
    print_unique_only(output, err_flag=err_flag)

# see jfs's answer on https://stackoverflow.com/questions/31833897/python-read-from-subprocess-stdout-and-stderr-separately-while-preserving-order
def reader(pipe, q):
    try:
        try:
            with pipe:
                for line in iter(pipe.readline, b''):
                    q.put((pipe, line))
        finally:
            q.put(None)
    except KeyboardInterrupt:
        print("[ mtsenliven.py ] " + key_exit_msg)
        pass

q = Queue()
Thread(target=reader, args=[process.stdout, q]).start()
Thread(target=reader, args=[process.stderr, q]).start()
try:
    for _ in range(2):
        for source, line in iter(q.get, None):
            # print "%s: %s" % (source, line),
            s = source
            l = line
            # NOTE: source is a string such as "<_io.BufferedReader name=5>"
            try:
                l = line.decode("utf-8")
            except:
                # this should never happen but doesn't matter anyway
                pass
            process_msg("%s: %s" % (s, l))
except KeyboardInterrupt:
    print("[ mtsenliven.py ] " + key_exit_msg)
    pass

exit(0)

while True:
    try:
        # can deadlock on high volume--use communicate instead
        # as per https://docs.python.org/2/library/subprocess.html
        out_bytes = process.stdout.readline()
        # err_bytes = process.stderr.readline()
           # (err_bytes == '') and \
        if (out_bytes == '') and \
           (process.poll() is not None):
            break
        if out_bytes:
            process_msg(out_bytes)
        # if err_bytes:
            # process_msg(err_bytes)
        rc = process.poll()
    except KeyboardInterrupt:
        print("[ mtsenliven.py ] " + key_exit_msg)
        break
# process.kill()
