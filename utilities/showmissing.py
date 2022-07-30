#!/usr/bin/env python
import sys


def usage():
    print("")
    print(sys.argv[0] + " <file1> <file2>")
    print("")
    print("- Show QUOTED strings in file2 that aren't in file1.")
    print("")
    print("")


def getStrings(path, delimiter='"', unique=True):
    ret = []
    got = ""
    inQ = False
    with open(path) as f:
        line = True
        while line:
            line = f.readline()
            if line:
                i = 0
                while i < len(line):
                    if line[i] == delimiter:
                        if inQ:
                            if (not unique) or (got not in ret):
                                ret.append(got)
                            got = ""
                            inQ = False
                        else:
                            inQ = True
                    elif inQ:
                        got += line[i]
                    i += 1
    return ret


def main():
    argCount = len(sys.argv) - 1

    if argCount < 2:
        usage()
        return 1

    oldPath = sys.argv[1]
    newPath = sys.argv[2]

    olds = getStrings(oldPath)
    news = getStrings(newPath)
    for v in olds:
        if v not in news:
            print(v)
    return 0


if __name__ == "__main__":
    sys.exit(main())
