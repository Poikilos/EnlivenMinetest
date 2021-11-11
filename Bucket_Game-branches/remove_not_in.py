#!/usr/bin/env python3

import sys
import os
import platform

profile = None
if platform.system() == "Windows":
    profile = os.environ['USERPROFILE']
else:
    profile = os.environ['HOME']


def error(msg):
    sys.stderr.write("{}\n".format(msg))
    sys.stderr.flush()


def showNotInOriginal(patched, original, root=None, ignores=[]):
    '''
    Print rm relative ('rm ./...') commands to standard output where
    a file in patched doesn't exist in original.

    Keyword arguments:
    root -- Remove this from the beginning of the rm commands and
            replace it with ".". If None, it is set to patched.
    ignores -- files to ignore
    '''
    if root is None:
        root = patched
    for sub in os.listdir(patched):
        originalPath = os.path.join(original, sub)
        patchedPath = os.path.join(patched, sub)
        if sub in ignores:
            continue
        if os.path.isdir(patchedPath):
            showNotInOriginal(patchedPath, originalPath, root=root, ignores=ignores)
            continue
        if not os.path.isfile(originalPath):
            relPath = patchedPath[len(root):]
            dotPath = "." + relPath
            dotPathShell = dotPath
            if "'" in dotPathShell:
                dotPathShell = '"{}"'.format(dotPathShell)
            elif '"' in dotPathShell:
                dotPathShell = "'{}'".format(dotPathShell)
            print("rm {}".format(dotPathShell))


if __name__ == "__main__":
    original = os.path.join(profile, "minetest", "games", "Bucket_Game")
    patched = os.path.abspath(".")
    originalMods = os.path.join(original, "mods")
    patchedMods = os.path.join(patched, "mods")
    if not os.path.isdir(originalMods):
        error("Error: \"{}\" doesn't seem to be a game since it doesn't have a \"mods\" directory.".format(original))
        exit(1)
    if not os.path.isdir(patchedMods):
        error("Error: \"{}\" doesn't seem to be a game since it doesn't have a \"mods\" directory.".format(patched))
        exit(1)
    myName = os.path.split(sys.argv[0])[1]
    # error("myName:{}".format(myName))
    showNotInOriginal(patched, original, None, ignores=[myName])
