#!/usr/bin/env python3
from __future__ import print_function
import sys
import os

from headcompare import (
    error,
    compareBranch,
    defaultVirtualReposDir,
    minetestPath,
    gamesPath,
    gamePath,
    profile,
)

me = os.path.basename(__file__)

def usage():
    error("Usage:")
    sys.stderr.write("Specify a branch")
    parent = "Bucket_Game-base"
    if os.path.isdir(parent):
        error(" from Bucket_Game-base:")
        for sub in os.listdir(parent):
            subPath = os.path.join(parent, sub)
            if sub.startswith("."):
                continue
            if os.path.isdir(subPath):
                error(subPath)
    else:
        error(" from Bucket_Game-base.")

    error("{} <branch name (see above)> [<bucket_game path>]".format(me))
    error("")

def main():
    global gamePath
    gamePath = None
    if len(sys.argv) < 2:
        usage()
        error("Error: You must provide a branch name.\n")
        exit(1)
    if len(sys.argv) > 3:
        usage()
        error("Error: There are too many arguments: {}.\n"
              "".format(sys.argv))
        exit(1)
    if len(sys.argv) > 2:
        gamePath = sys.argv[2]

    results = compareBranch(sys.argv[1], gamePath=gamePath,
                            compareOld=True)
    error("# ^ Do that to verify: they MUST match, and the first"
          " directory must be unmodified from the original"
          " release package.")


if __name__ == "__main__":
    main()
