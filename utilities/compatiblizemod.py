#!/usr/bin/env python3

import sys
import os

def error(msg):
    sys.stderr.write("{}\n".format(msg))
    sys.stderr.flush()

def add_depends(mod_path):
    depends_path = os.path.join(mod_path, "depends.txt")
    if os.path.isfile(depends_path):
        error("WARNING: Writing {} will be skipped since it exists."
              "".format(depends_path))
        return
    mod_conf = os.path.join(mod_path, "mod.conf")
    if not os.path.isfile(mod_conf):
        error("WARNING: Writing {} will be skipped since {} does"
              " not exist."
              "".format(depends_path, mod_conf))
        return
    optional_depends = []
    depends = []
    lineN = 0
    with open(mod_conf, 'r') as ins:
        for rawL in ins:
            lineN += 1  # Counting numbers start at 1.
            line = rawL.strip()
            if len(line) < 1:
                continue
            if line.startswith("#"):
                continue
            signI = line.find("=")
            if signI < 0:
                print("{}:{}: Warning: There is no '='"
                      "".format(mod_conf, lineN))
                continue
            if signI < 1:
                print("{}:{}: Warning: starts with '='"
                      "".format(mod_conf, lineN))
                continue
            name = line[:signI].strip()
            value = line[signI+1:].strip()
            if name == "depends":
                depends = [depend.strip() for depend in value.split(",")]
            elif name == "optional_depends":
                optional_depends = [depend.strip() for depend in value.split(",")]
    print("")
    mod_dir_name = os.path.basename(mod_path)
    print("mod: {}".format(mod_dir_name))
    print("* depends: {}".format(depends))
    print("* optional_depends: {}".format(optional_depends))
    with open(depends_path, 'w') as outs:
        for depend in depends:
            outs.write("{}\n".format(depend))
        for depend in optional_depends:
            outs.write("{}?\n".format(depend))
    print("* wrote {}/depends.txt".format(mod_dir_name))


if __name__ == "__main__":
    parent = os.path.realpath(".")
    modpack_conf = os.path.join(parent, "modpack.conf")
    if os.path.isfile(modpack_conf):
        for sub in os.listdir(parent):
            subPath = os.path.join(parent, sub)
            if sub.startswith("."):
                continue
            if not os.path.isdir(subPath):
                continue
            add_depends(subPath)
    else:
        add_depends(parent)
