#!/usr/bin/env python
'''
Count the number of meshes in OBJ files. In the Wavefront OBJ format,
these meshes are technically called "Objects" and the OBJ file can have
any number of them. They are created by the "o" command in the file.

Alternative (OBJ or non-OBJ):
- For support of any file that can be imported into Blender, try pasting
  count_objects.py's contents (found in
  EnlivenMinetest/utilities/blender/) into a Blender script Window
  (Follow instructions in docstring at top of file).
'''
from __future__ import print_function
import sys
import os


def echo0(*args, **kwargs):
    dst = sys.stderr
    if 'file' in kwargs:
        dst = kwargs['file']
        del kwargs['file']
    print(*args, file=dst, **kwargs)


def usage():
    echo0(__doc__)
    echo0()


def obj_stats(path):
    results = {
        'mesh_count': 0,
    }
    if not os.path.isfile(path):
        raise FileNotFoundError(path)
    lineN = 0
    with open(path, 'rb') as stream:
        for rawL in stream:
            lineN += 1  # counting numbers start at 1
            line = rawL.strip()
            if not line.strip():
                # blank line
                continue
            parts = line.split()
            if parts[0] == b"o":
                results['mesh_count'] += 1
            else:
                pass
                # echo0('line {}: Does not start with "o": {}'
                #       ''.format(lineN, parts))
    return results


def main():
    if len(sys.argv) < 2:
        usage()
        echo0("You must provide an OBJ filename.")
        return 1
    path = sys.argv[1]
    if not path.lower().endswith(".obj"):
        usage()
        echo0("Error: Only OBJ files can be analyzed. Try pasting"
              " count_objects.py's contents into a Blender script window"
              " (Follow instructions in docstring at top of file)")
              " to analyze any file you can import into Blender."
        return 1
    if not os.path.isfile(path):
        # Avoid an exception & use CLI-style (pipe & filter) logic
        usage()
        echo0('Error: "{}" does not exist.'.format(path))
        return 1
    stats = obj_stats(path)
    print(stats['mesh_count'])
    return 0


if __name__ == "__main__":
    sys.exit(main())
