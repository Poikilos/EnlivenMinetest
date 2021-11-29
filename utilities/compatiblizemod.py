#!/usr/bin/env python3

import sys
import os
import shutil

def error(msg):
    sys.stderr.write("{}\n".format(msg))
    sys.stderr.flush()

def add_depends(mod_path):
    mod_dir_name = os.path.basename(mod_path)
    modpack_conf = os.path.join(mod_path, "modpack.conf")
    modpack_txt = os.path.join(mod_path, "modpack.txt")
    found_modpack_file = None
    if os.path.isfile(modpack_txt):
        found_modpack_file = "modpack.txt"
    if os.path.isfile(modpack_conf):
        found_modpack_file = "modpack.conf"
        if not os.path.isfile(modpack_txt):
            # shutil.copy(modpack_conf, modpack_txt)
            with open(modpack_txt, 'w') as outs:
                wroteCount = 0
                with open(modpack_conf, 'r') as ins:
                    for rawL in ins:
                        line = line.strip()
                        signI = line.find("=")
                        if signI < 1:
                            continue
                        name = line[:signI].strip()
                        value = line[signI+1:].strip()
                        if name == "description":
                            outs.write(value)
                            wroteCount += 1
                            pass
                if wroteCount < 1:
                    outs.write("\n")
                    # ^ The modpack.txt file just needs to exist.
            print("* created {}/modpack.txt"
                  "".format(mod_dir_name))
        else:
            error("{}/modpack.txt already exists for compatibility."
                  "".format(mod_dir_name))
    if os.path.isfile(modpack_txt):
        error("{}/{} indicates it is a modpack."
              "".format(mod_dir_name, found_modpack_file))
        for sub in os.listdir(mod_path):
            if sub.startswith('.'):
                continue
            subPath = os.path.join(mod_path, sub)
            add_depends(subPath)
        # It must be a modpack, so return after doing subdirectories.
        return
    depends_path = os.path.join(mod_path, "depends.txt")
    description_path = os.path.join(mod_path, "description.txt")
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
    optional_depends = None
    depends = None
    description = None
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
            values = [depend.strip() for depend in value.split(",")]
            if name == "depends":
                depends = values
            elif name == "optional_depends":
                optional_depends = values
            elif name == "description":
                description = value
    print("")
    print("mod: {}".format(mod_dir_name))
    print("* depends: {}".format(depends))
    print("* optional_depends: {}".format(optional_depends))
    depends_count = 0
    if depends is not None:
        depends_count += len(depends)
    if optional_depends is not None:
        depends_count += len(optional_depends)
    if depends_count > 0:
        with open(depends_path, 'w') as outs:
            if depends is not None:
                for depend in depends:
                    outs.write("{}\n".format(depend))
            if optional_depends is not None:
                for depend in optional_depends:
                    outs.write("{}?\n".format(depend))
    print("* wrote {}/depends.txt".format(mod_dir_name))
    if description is not None:
        if os.path.isfile(description_path):
            print("* INFO: There is already a description.txt so it"
                  " will be left intact.")
            return
        with open(description_path, 'w') as outs:
            outs.write("{}\n".format(description))
        print("* wrote {}/description.txt".format(mod_dir_name))


if __name__ == "__main__":
    parent = os.path.realpath(".")
    add_depends(parent)
