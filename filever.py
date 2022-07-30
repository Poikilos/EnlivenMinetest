#!/usr/bin/env python
import sys
# based on code by Jamie at
#   <http://stackoverflow.com/questions/580924/python-windows-
#   file-version-attribute>
try:
    from win32api import GetFileVersionInfo, LOWORD, HIWORD
except ImportError:
    print("you need to install win32api such as with the command:")
    print("sudo python2 -m pip install --upgrade pip")
    print("sudo python -m pip install pypiwin32")
    sys.exit(1)

    from win32api import GetFileVersionInfo, LOWORD, HIWORD


def get_version_number(filename):
    try:
        info = GetFileVersionInfo(filename, "\\")
        ms = info['FileVersionMS']
        ls = info['FileVersionLS']
        return HIWORD(ms), LOWORD(ms), HIWORD(ls), LOWORD(ls)
    except IndexError:
        # FIXME: test this and find out what exception can occur.
        return 0, 0, 0, 0


API_USAGE = '''
# API Usage:
import filever
parts = filever.get_version_number(filename)
major,minor,subminor,revision = parts
print(".".join([str (i) for i in parts]))
'''


def main():
    import os
    if "COMSPEC" in os.environ:
        filename = os.environ["COMSPEC"]
        this_delimiter = "."
        print(str(filename) + " version:")
        print(".".join([str(i) for i in get_version_number(filename)]))
    print("Running filever directly doesn't do much\n\n"+API_USAGE)
    return 0


if __name__ == '__main__':
    sys.exit(main())
