import os
import datetime

os_name = "*x"
debug_name = "debug.txt"
debug_path = "/usr/share/minetest/worlds"
world_name = None
if os.sep=="\\":
    os_name = "windows"

print("os detected: "+os_name)

