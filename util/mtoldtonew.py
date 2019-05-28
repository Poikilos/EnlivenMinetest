#!/usr/bin/env python
import os
import csv
import sys

mtdeltas_csv = "mtoldtonew.csv"
if not os.path.isfile(mtdeltas_csv):
    print("ERROR: missing " + mtdeltas_csv)
    #exit(1)

files = []

usageStr = '''
Usage:
   python3 mtoldtonew.py <filename>
   or
   python3 mtoldtonew.py <filenames>

Examples:
   python3 mtoldtonew.py palm_oldnodes.we
   python3 mtoldtonew.py palm_oldnodes.we palm.we

* Example 2 yields: palm_newnodes.we and newpalm.we
  with all nodes replaced according to csv.
  (adds "new" to beginning if "old" is not in specified filename)

* only replaces node names surrounded by quotes
  - you can change that behavior using python:
    from mtoldtonew import oldToNew
    oldToNew('file.we', quotechar='')

'''
usageStr += "edit '%s' as needed (old name in column 1, new name in 2)"

def usage():
    print(usageStr)

mtdeltas = {}

def stripQuotes(s, quotechar='"'):
    if (len(s) >= 2) and (s[0] == quotechar) and (s[-1] == quotechar):
        s = s[1:-1]
    return s

def quoted(str1, quotechar='"'):
    return(quotechar + str1 + quotechar)

def replaceQuoted(str1, deltas, quotechar='"'):
    ret = str1
    for k, v in deltas.items():
        ret = ret.replace(quoted(k, quotechar), quoted(v, quotechar))
    return ret

with open(mtdeltas_csv) as csvfile:
    ins = csv.reader(csvfile, delimiter=',', quotechar='"')
    lineI = 0
    for row in ins:
        lineI += 1
        if (len(row) < 2):
            continue
        oldStr = stripQuotes(row[0].strip())
        newStr = stripQuotes(row[1].strip())
        # csv doesn't strip quotes if a space is before an opening quote
        # print("'%s', '%s'" % (oldStr, newStr))
        if len(oldStr) > 0:
            if len(newStr) > 0:
                mtdeltas[oldStr] = newStr
            else:
                print("Skipped empty destination for '" + oldStr
                      + " on line " + str(lineI) + " in " + csvfile)

def oldToNew(path, quotechar='"'):
    newName = path.replace("old", "new")
    if newName == path:
        newName = "new" + newName
    if os.path.exists(newName):
        print("WARNING: Overwriting '%s'..." % newName)
    with open(path, 'r') as ins:
        with open(newName, 'w') as outs:
            oldLine = True
            while oldLine:
                oldLine = ins.readline()
                if oldLine:
                    outs.write(replaceQuoted(oldLine, mtdeltas) + "\n")
    print("* wrote '%s'" % newName)

if __name__ == "__main__":
    for i in range(1, len(sys.argv)):
        try_path = sys.argv[i]
        if os.path.isfile(try_path):
            files.append(try_path)
        else:
            print("MISSING file: '" + try_path + "'")

    if len(files) < 1:
        usage()
        print("")
        print("You must specify a plain-text schem such as a\n"
              ".we file, or any file containing double-quoted node names.")

    for oldName in files:
        print("Processing %s..." % oldName)
        oldToNew(oldName)
