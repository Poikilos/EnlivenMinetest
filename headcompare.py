#!/usr/bin/env python3
from __future__ import print_function
import sys
import os
import platform

me = os.path.basename(__file__)
myDir = os.path.dirname(__file__)
defaultVirtualReposDir = myDir

def error(msg):
    sys.stderr.write("{}\n".format(msg))
    sys.stderr.flush()


def usage():
    error("Usage:")
    sys.stderr.write("Specify a branch")
    parent = "Bucket_Game-branches"
    if os.path.isdir(parent):
        error(" from Bucket_Game-branches:")
        for sub in os.listdir(parent):
            subPath = os.path.join(parent, sub)
            if sub.startswith("."):
                continue
            if os.path.isdir(subPath):
                error(subPath)
    else:
        error(" from Bucket_Game-branches.")

    error("{} <branch name (see above)> [<bucket_game path>]".format(me))
    error("")


profile = None
if platform.system() == "Windows":
    profile = os.environ.get('USERPROFILE')
    if profile is None:
        error("Error: USERPROFILE is not set.")
        exit(1)
else:
    profile = os.environ.get('HOME')
    if profile is None:
        error("Error: HOME is not set.")
        exit(1)

minetestPath = os.path.join(profile, "minetest")
gamesPath = os.path.join(minetestPath, "games")
gamePath = None


def compareBranch(branchName, gamePath=None, bgVersion=None,
                  bgVersionsPath=minetestPath, compareOld=False,
                  branchesPath=None,
                  vReposDir=defaultVirtualReposDir):
    results = {}
    '''
    Keyword arguments:
    gamePath -- Specify a bucket_game base path to which to compare.
    bgVersion -- Specify a bucket_game version that is stored outside
        of the games directory but directly in bgVersionsPath (If
        bgVersion is not None, the function will fail if the directory
        "bucket_game-{}".format(bgVersion) doesn't exist in
        bgVersionsPath.
    compareOld: Set to True to use
        patchesDir = os.path.join(myDir, "Bucket_Game-base")
        instead of
        patchesDir = os.path.join(myDir, "Bucket_Game-branches")
        (The option is ignored if branchesPath is set).
    branchesPath -- Specify what directory contains the head branches.
    vReposDir -- Specify what directory contains
        Bucket_Game-branches and Bucket_Game-base (The option is ignored
        if branchesPath is set).

    Raises:
    - ValueError if the bgVersion is neither specified nor detected
      after "-vs-" in the patch name.
    - ValueError if the bgVersion directory isn't found
    - ValueError if the branch isn't found
    '''
    detectedBGVer = None
    parts = branchName.split("-")
    versionMsg = "specified"
    if (len(parts) > 2) and (parts[-2] == "vs"):
        detectedBGVer = parts[-1]
    if bgVersion is not None:
        if detectedBGVer is not None:
            print("WARNING: detected version {} but you specified {}"
                  "".format(detectedBGVer, bgVersion))
    else:
        bgVersion = detectedBGVer
        versionMsg = "detected"
    '''
    tryGame = "bucket_game"
    tryGamePath = os.path.join(gamesPath, tryGame)
    if not os.path.isdir(tryGamePath):
        tryGame = "Bucket_Game"
        tryGamePath = os.path.join(gamesPath, tryGame)
    '''
    if bgVersion is None:
        raise ValueError("The game version was neither specified nor "
                         " after \"-vs-\" in the patch name.")

    specifiedGame = "bucket_game-{}".format(bgVersion)
    # os.path.join(bgVersionsPath, specifiedGame)
    specifiedGamePath = os.path.join(bgVersionsPath, specifiedGame)
    if not os.path.isdir(specifiedGamePath):
        usage()
        raise ValueError("The {} game version is not present at"
                         " {}".format(versionMsg, specifiedGamePath))
    if branchesPath is None:
        if compareOld:
            branchesPath = os.path.join(vReposDir,
                                        "Bucket_Game-base")
        else:
            branchesPath = os.path.join(vReposDir,
                                        "Bucket_Game-branches")
    if os.path.sep in branchName:
        branchName = os.path.split(branchName)[1]
    branchPath = os.path.join(branchesPath, branchName)
    if not os.path.isdir(branchPath):
        raise ValueError("The branch wasn't found at \"{}\""
                         "".format(branchPath))
    branchPath = os.path.realpath(branchPath)
    print("meld \"{}\" \"{}\"".format(specifiedGamePath, branchPath))
    patchFilePath = branchPath+".patch"
    print("diff -ru \"{}\" \"{}\" > \"{}\""
          "".format(specifiedGamePath, branchPath, patchFilePath))
    results = {
        'gamePath': specifiedGamePath,
        'branchPath': specifiedGamePath,
        'patchFilePath': specifiedGamePath,
    }
    return results

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

    results = compareBranch(sys.argv[1], gamePath=gamePath)
    error("# ^ Do that to see the difference or generate a patch,"
      " but the first directory must be unmodified from the"
      " original release package.")


if __name__ == "__main__":
    main()
