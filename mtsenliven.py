#!/usr/bin/env python3
from __future__ import print_function

# runs minetestserver using the paths defined by minetestinfo
# NOTE: SIGINT (as opposed to KILL) makes sure minetest server
#   shuts down properly (makes sure all processes finish) according to
#   dr4Ke on
#   https://forum.minetest.net/viewtopic.php?f=11&t=13138&start=50
import os
import sys
import subprocess
import signal
try:
    from Threading import thread as Thread  # Python 2
except ImportError:
    from threading import Thread  # Python 3
# if sys.version[0] == '2':
try:
    from Queue import Queue  # Python 2
except ImportError:
    from queue import Queue  # Python 3

REPO_PATH = os.path.dirname(os.path.realpath(__file__))
# ^ realpath follows symlinks
REPOS_PATH = os.path.dirname(REPO_PATH)
TRY_REPO_PATH = os.path.join(REPOS_PATH, "mtanalyze")
if os.path.isfile(os.path.join(TRY_REPO_PATH, "mtanalyze", "__init__.py")):
    # ^ Yes, it is 2 mtanalyze deep,
    #   such as "$HOME/git/mtanalyze/mtanalyze/__init__.py"
    sys.path.insert(0, TRY_REPO_PATH)

from pyenliven import (
    echo0,
    echo1,
)


# from mtanalyze.minetestinfo import *
from mtanalyze import (
    mti,
    get_var_and_check,
)

non_unique_wraps = []
non_unique_wraps.append(
    {
        "opener": "active block modifiers took ",
        "closer": "ms (longer than 200ms)"
    }
)

unique_flags = [
    "leaves game",
    "joins game"
]

msgprefix_flags = ["WARNING[Server]: ", "ACTION[Server]: "]
msgprefix_lists = {}  # where flag is key
for flag in msgprefix_flags:
    msgprefix_lists[flag] = []


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
        # Look for flags to identify lines such as
        #   '2018-02-06 21:08:06: WARNING[Server]: Deprecated call
        #   to get_look_yaw, use get_look_horizontal instead'
        # or 2018-02-06 21:08:05: ACTION[Server]: [playereffects] Wrote
        #   playereffects data into /home/owner/.minetest/worlds/
        #   .../playereffects.mt.
        for flag in msgprefix_flags:
            f_i = output.find(flag)
            if f_i >= 0:
                found_flag = flag
                break
        if found_flag:
            sub_msg = output[f_i+len(flag):].strip()
            for wrap in non_unique_wraps:
                if (wrap["opener"] in sub_msg and
                        wrap["closer"] in sub_msg):
                    sub_msg = wrap["opener"] + "..." + wrap["closer"]
                    msg_msg = "similar messages"
                    break
            if sub_msg in msgprefix_lists[found_flag]:
                show_enable = False
            else:
                msgprefix_lists[found_flag].append(sub_msg)
    if show_enable:
        print(output_strip)
        if found_flag is not None:
            echo0("  [ mtsenliven.py ] " + msg_msg
                  + " will be suppressed")


def process_msg(bstring):
    output = bstring
    err_flag = False
    try:
        output = bstring.decode("utf-8")
        #         works on python2 or 3
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


# See jfs's answer on <https://stackoverflow.com/questions/31833897/
#   python-read-from-subprocess-stdout-and-stderr-separately-while-
#   preserving-order>
def reader(pipe, q):
    try:
        try:
            with pipe:
                for line in iter(pipe.readline, b''):
                    q.put((pipe, line))
        finally:
            q.put(None)
    except KeyboardInterrupt:
        echo0("[ mtsenliven.py ] " + key_exit_msg)
        pass


def decode_safe(b):
    try:
        s = b.decode()
    except UnicodeDecodeError:
        s = b.decode('utf-8')
    '''
    except AttributeError as ex:
        if "'str' object has no attribute" in str(ex):
            return b
        raise ex
    '''
    return s


def main():
    key_exit_msg = "SIGINT should shut down server safely...\n"
    game_id = "ENLIVEN"
    # screen -S MinetestServer $mts --gameid ENLIVEN --worldname ...
    echo0()
    echo0()
    echo0()

    mts, code = get_var_and_check("minetestserver_path", code=1)
    if code != 0:
        return code

    wp, code = get_var_and_check("primary_world_path", code=1)
    if code != 0:
        return code

    wn = os.path.basename(wp)
    echo0("Using minetestserver: " + mts)
    echo0("Using primary_world_path: " + wp)
    echo0("Using world_name: " + wn)
    echo0()
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
        # bufsize=1 as per jfs on <https://stackoverflow.com/questions/
        #   31833897/python-read-from-subprocess-stdout-and-stderr-
        #   separately-while-preserving-order>
    except Exception as e:
        echo0(mts + " could not be executed. Try installing the "
              " minetest-server package or compiling from git instructions"
              " on minetest.net")
        echo0(e)
        return 2
    # see https://www.endpoint.com/blog/2015/01/28/getting-realtime-output-
    # using-python

    q = Queue()
    Thread(target=reader, args=[process.stdout, q]).start()
    Thread(target=reader, args=[process.stderr, q]).start()
    try:
        for _ in range(2):
            for source, line in iter(q.get, None):
                # print "%s: %s" % (source, line),
                s = source
                l_s = line
                # NOTE: source is a string such as
                # "<_io.BufferedReader name=5>"
                l_s = decode_safe(line)  # line.decode("utf-8")
                process_msg("%s: %s" % (s, l_s))
    except KeyboardInterrupt:
        print("[ mtsenliven.py ] " + key_exit_msg)
        pass

    return 0
    '''
    while True:
        try:
            # can deadlock on high volume--use communicate instead
            # as per https://docs.python.org/2/library/subprocess.html
            out_bytes = process.stdout.readline()
            # err_bytes = process.stderr.readline()
            #    (err_bytes == '') and \
            if (out_bytes == '') and \
               (process.poll() is not None):
                break
            if out_bytes:
                process_msg(out_bytes)
            # if err_bytes:
            #     process_msg(err_bytes)
            rc = process.poll()
        except KeyboardInterrupt:
            echo0("[ mtsenliven.py ] " + key_exit_msg)
            break
    # process.kill()
    return 0
    '''


if __name__ == "__main__":
    sys.exit(main())
