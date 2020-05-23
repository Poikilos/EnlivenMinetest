#!/usr/bin/env python
"""
Make a copy of any files in the given paths, replacing
spaces with " \", newline, then indent. This is useful for creating
intermediate files for the purpose of running meld or diff on files
with long lines (such as cmake commands pasted into files for
comparison purposes and link.txt files).
"""
import sys
import os

def continuify(inPath, outPath, continueStr="  \\", indent="    ",
        sep=" "):
    with open(outPath, 'w') as outs:
        with open(inPath) as ins:
            rawLine = True
            while rawLine:
                rawLine = ins.readline()
                line = rawLine.rstrip()
                parts = line.split(sep)
                starter = ""
                ender = continueStr
                for i in range(len(parts)):
                    part = parts[i]
                    if i == len(parts) - 1:
                        ender = ""
                    outs.write(indent + part.strip(sep) + ender + "\n")
                    if i >= 0:
                        starter = indent

def main():
    if len(sys.argv) < 2:
        print("You must specify file(s).")
        exit(1)
    for i in range(1, len(sys.argv)):
        arg = sys.argv[i]
        if not os.path.isfile(arg):
            print("ERROR: {} is not a file.".format(arg))
            exit(1)
        # parts = os.path.splitext(arg)
        # outPath = parts[0] + ".tmp" + parts[1]
        outPath = arg + ".continuified.tmp"
        continuify(arg, outPath)
        print("* wrote \"{}\"".format(outPath))
    pass

if __name__ == "__main__":
    main()
