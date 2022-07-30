#!/usr/bin/env python3
from __future__ import print_function
import sys
import os

from pyenliven import (
    echo0,
)

from headcompare import (
    compareBranch,
    defaultVirtualReposDir,
    minetestPath,
    gamesPath,
    defaultGamePath,
    profile,
)

me = os.path.basename(__file__)


def usage():
    echo0("Usage:")
    sys.stderr.write("Specify a branch")
    parent = "Bucket_Game-base"
    if os.path.isdir(parent):
        echo0(" from Bucket_Game-base:")
        for sub in os.listdir(parent):
            subPath = os.path.join(parent, sub)
            if sub.startswith("."):
                continue
            if os.path.isdir(subPath):
                echo0(subPath)
    else:
        echo0(" from Bucket_Game-base.")

    echo0("{} <branch name (see above)> [<bucket_game path>]".format(me))
    echo0("")


def main():
    global defaultGamePath
    defaultGamePath = None
    if len(sys.argv) < 2:
        usage()
        echo0("Error: You must provide a branch name.\n")
        return 1
    if len(sys.argv) > 3:
        usage()
        echo0("Error: There are too many arguments: {}.\n"
              "".format(sys.argv))
        return 1
    if len(sys.argv) > 2:
        defaultGamePath = sys.argv[2]

    results = compareBranch(sys.argv[1], gamePath=defaultGamePath,
                            compareOld=True)
    echo0("# ^ Do that to verify: they MUST match, and the first"
          " directory must be unmodified from the original"
          " release package.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
