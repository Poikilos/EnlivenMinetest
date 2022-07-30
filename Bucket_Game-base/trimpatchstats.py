#!/usr/bin/env python3
'''
Remove the lines from the from the input file in Bucket_Game-base that
are not in the matching list file in Bucket_Game-branches.
The resulting modified list is written to standard output.

The provided filename must exist in both the Bucket_Game-base directory
and the parallel Bucket_Game-branches directory.

The file must contain output such as from ls or find executing ls. Examples:
    find -type f -name "*.ogg" -exec ls -lh {} \\;
    find -type f -exec ls -lh {} \\;

Usage:
./trimpatchstats.py <filename>
'''
import sys
import os
import json


def echo0(*args, **kwargs):
    print(*args, file=sys.stderr, **kwargs)


def usage():
    echo0("")
    echo0("trimpatchstats.py")
    echo0("-----------------")
    echo0(__doc__)


def splitFirst(line, delimiter):
    '''
    Only split once. Return a tuple of both parts excluding delimiter.
    If delimiter isn't present, return the line, None
    '''
    delI = line.find(delimiter)
    if delI < 0:
        return line, None
    return line[:delI], line[delI+1:]


def splitLast(line, delimiter):
    '''
    Only split once. Return a tuple of both parts excluding delimiter.
    If delimiter isn't present, return the line, None
    '''
    delI = line.rfind(delimiter)
    if delI < 0:
        return line, None
    return line[:delI], line[delI+1:]


def parse_ls(line):
    '''
    Parse the output from "ls -l" or "ls -lh" (human-readable size).
    You can use 'n' instead of 'l' in either case, but the owner and
    group will be numbers instead of names.

    Returns: a dictionary containing 'permissions',
             'hardlinks' (count), 'owner', 'group', 'size', 'date',
             'name' where each entry is a string. The format of size is
             in bytes, unless the 'h' option was used with ls, in which
             case it will be human-readable (such as "8.3K"").
             The owner and group will be number strings rather than
             name strings if the 'n' option was used with ls.

    Sequential arguments:
    line -- The line must be like "perms hardlinks user group size date"
      such as any of the following:
      -rw-r--r-- 1 owner owner 8.3K Dec 14  2018 fire_extinguish.ogg
      -rw-r--r-- 1 1000 1000 8.3K Dec 14  2018 'fire extinguish.ogg'
      -rw-r--r-- 1 owner owner 8300 Dec 14  2018 "Poikilos' fire.ogg"
    '''
    if line.startswith("total "):
        raise ValueError("Expected ls -l file lines but got the"
                         "ls -l total line: {}".format(line))
    results = {}
    results['name'] = None
    chopped = line

    # Gradually chop off parts of line until only the date
    # remains, since that is the least predictable as far as
    # delimiters.

    if chopped.endswith("'") or chopped.endswith('"'):
        # the filename has spaces
        # (or has "'" if has double quotes).
        inQ = chopped[-1]
        chopped = chopped[:-1]
        firstQI = chopped.rfind(inQ)
        if firstQI < 0:
            raise ValueError("There is a missing '{}' before the"
                             " filename that ends with '{}'"
                             " in \"{}\""
                             "".format(inQ, inQ, chopped + inQ))
        name = chopped[firstQI+1:]
        chopped = chopped[:firstQI-1]  # -1 to remove the space
    else:
        chopped, name = splitLast(chopped, " ")
    results['permissions'], chopped = splitFirst(chopped, " ")
    results['hardlinks'], chopped = splitFirst(chopped, " ")
    results['owner'], chopped = splitFirst(chopped, " ")
    results['group'], chopped = splitFirst(chopped, " ")
    results['size'], chopped = splitFirst(chopped, " ")
    results['date'] = chopped  # Only the date should remain by now.
    # results['name'] = os.path.split(path)[0]
    # results['path'] = path
    results['name'] = name
    return results


def fill_file_dict_path(fileInfoDict, baseDir):
    '''
    Fill in the 'path' of the fileInfoDict with the baseDir, or if not
    specified, the current working directory IF the file exists in it,
    otherwise set 'path' to None if not set already.
    '''

    name = fileInfoDict.get('name')
    if name is None:
        raise ValueError("The 'name' key must contain a filename"
                         " in the dictionary provided to"
                         " fill_file_dict_path.")
    baseDirMsg = "specified baseDir"
    if baseDir is None:
        baseDirMsg = "current directory"
        baseDir = os.getcwd()
    path = os.path.join(baseDir, name)

    fileInfoDict['path'] = os.path.abspath(name)
    if not os.path.exists(path):
        if os.path.exists(fileInfoDict['path']):
            print("WARNING: missing \"{}\" so using {} to form the path"
                  " \"{}\""
                  "".format(path, baseDirMsg, fileInfoDict['path']))
        else:
            print("WARNING: missing \"{}\" so using {} to form the path"
                  " \"{}\" which also doesn't exist"
                  "".format(path, baseDirMsg, fileInfoDict['path']))
    fileInfoDict['name'] = os.path.split(fileInfoDict['path'])[-1]


def key_matches_for_any(haystacks, key, needle):
    '''
    See if any dict in haystacks such as haystacks[0][key] is needle.
    '''
    for haystack in haystacks:
        if haystack.get(key) == needle:
            return True
    else:
        return False


class LSFileInfo:

    def __init__(self, line, baseDir):
        '''
        Parse the output from "ls -l" or "ls -lh" (human-readable size).
        You can use 'n' instead of 'l' in either case, but the owner and
        group will be numbers instead of names.

        Sequential arguments:
        line -- The line must be like (ls -lh in this example):
          -rw-r--r-- 1 owner owner 8.3K Dec 14  2018 fire_extinguish.ogg
          perms hardlinks user group size date
        baseDir -- Provide the directory from which the ls command was
          originally run so the LSFileInfo can get the full path.
          Otherwise, the current working directory will be tried.
        '''
        results = parse_ls(line)
        # self.name = results['name']
        # self.path = None
        self.permissions = results['permissions']
        self.hardlinks = results['hardlinks']
        self.owner = results['owner']
        self.group = results['group']
        self.size = results['size']
        self.date = results['date']
        fill_file_dict_path(results, baseDir)
        self.name = results.get('name')
        self.path = results.get('path')

    def to_dict(self):
        results = {}
        # result['name'] = self.name
        results['path'] = self.path
        results['permissions'] = self.permissions
        results['hardlinks'] = self.hardlinks
        results['owner'] = self.owner
        results['group'] = self.group
        results['date'] = self.date
        return result

    def __repr__(self):
        return json.dumps(self.to_dict())

    def __str__(self):
        return json.dumps(self.to_dict())


def getFileNumber(path, num):
    '''
    Get a file from a listfile that contains ls -l or ls -n output.

    Sequential arguments:
    path -- The file must be output from 'ls -l' or 'ls -n' or other
            ls commands with 'l' or 'n'.
    num -- The file number, such as 1 for the first file, skipping a
           line that is blank or starts with "total ", "#", or "$".
    '''
    lineN = 0
    with open(path, 'r') as ins:
        for rawL in ins:
            line = rawL.strip()
            if len(line) == 0:
                continue
            if line.startswith("total "):
                continue
            if line.startswith("#"):
                continue
            if line.startswith("$"):
                continue
            lineN += 1
            if lineN == num:
                return parse_ls(line)
    return None


def printOnlyPatched(baseListPath):
    baseListPath = os.path.abspath(baseListPath)
    basePath, listName = os.path.split(baseListPath)
    parentPath = os.path.split(basePath)[0]
    patchedPath = os.path.join(parentPath, "Bucket_Game-branches")
    patchedListPath = os.path.join(patchedPath, listName)
    if not os.path.isfile(patchedListPath):
        raise ValueError("{} is missing.".format(patchedListPath))

    dotI = listName.find(".")
    targetDirName = None
    targetDirPath = None
    if dotI > -1:
        # See if the filename is named after the directory.
        targetDirName = os.path.split(listName[:dotI])[1]
        tryPath = os.path.join(patchedPath, targetDirName)
        if os.path.isdir(tryPath):
            targetDirPath = tryPath
        else:
            targetDirPath = os.getcwd()
            print("WARNING: missing \"{}\" so trying current directory"
                  "".format(tryPath, None))

    fid = getFileNumber(patchedListPath, 1)
    if fid is None:
        print("Error: \"{}\" contained no filenames."
              "".format(patchedListPath))
        return 1
    tryFilePath = os.path.join(targetDirPath, fid['name'])
    if not os.path.isfile(tryFilePath):
        print("Error: \"{}\" doesn't exist. Run again from the"
              " directory containing \"{}\", otherwise name the patch"
              " file so the part before the first dot matches a"
              " directory name in the \"{}\" directory and run in a"
              " directory parallel to that."
              "".format(tryFilePath, fid['name'], patchedPath))
        return 2

    echo0("* analyzing \"{}\"".format(patchedListPath))
    patchedFIs = []
    rawNames = []
    with open(patchedListPath, 'r') as ins:
        for rawL in ins:
            line = rawL.strip()
            if len(line) < 1:
                continue
            if line.startswith("total "):
                continue
            if line.startswith("$"):
                continue
            if line.startswith("#"):
                continue
            fid = parse_ls(line)
            rawNames.append(fid['name'])
            # fill_file_dict_path(fid, targetDirPath)
            # echo0(fid)

    echo0("* analyzing \"{}\"".format(baseListPath))
    allCount = 0
    matchCount = 0
    with open(baseListPath, 'r') as ins:
        for rawL in ins:
            line = rawL.strip()
            if len(line) < 1:
                continue
            if line.startswith("total "):
                continue
            if line.startswith("$"):
                continue
            if line.startswith("#"):
                continue
            fid = parse_ls(line)
            allCount += 1
            if fid['name'] in rawNames:
                print(line)
                matchCount += 1
    echo0("{} of {} in {} were also in {}"
          "".format(matchCount, allCount, baseListPath,
                    patchedListPath))
    return 0


def main():
    if len(sys.argv) < 2:
        usage()
        echo0("Error: You are missing the required list filename argument.\n")
        return 1
    return printOnlyPatched(sys.argv[1])


if __name__ == "__main__":
    sys.exit(main())
