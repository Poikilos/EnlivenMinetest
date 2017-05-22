#!/usr/bin/env python
#by Jamie at http://stackoverflow.com/questions/580924/python-windows-file-version-attribute
try:
    from win32api import GetFileVersionInfo, LOWORD, HIWORD
except:
    print("you need to install win32api such as with the command:")
    print("python -m pip install --upgrade pip")
    print("python -m pip install pypiwin32")
    exit(1)
    
    from win32api import GetFileVersionInfo, LOWORD, HIWORD

def get_version_number (filename):
    try:
        info = GetFileVersionInfo (filename, "\\")
        ms = info['FileVersionMS']
        ls = info['FileVersionLS']
        return HIWORD (ms), LOWORD (ms), HIWORD (ls), LOWORD (ls)
    except:
        return 0,0,0,0

if __name__ == '__main__':
    import os
    if "COMSPEC" in os.environ:
        filename = os.environ["COMSPEC"]
        this_delimiter = "."
        print(str(filename) + " version:")
        print(".".join ([str (i) for i in get_version_number (filename)]))
    print("Running filever directly doesn't do much.\n\n#Usage:\n" +
        "import filever\n" +
        "parts = filever.get_version_number(filename)\n" +
        "major,minor,subminor,revision = parts\n" +
        "print(\".\".join([str (i) for i in parts]))\n\n")
