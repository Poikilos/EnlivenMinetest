#!/usr/bin/env python
import sys
import os
import shutil
# sys.argv[0] is name of script
myPath = os.path.realpath(__file__)
myDir = os.path.dirname(myPath)


def customExit(msg, code=1):
    print("")
    print("ERROR:")
    print(msg)
    print("")
    print("")
    exit(code)


def usage():
    print("Usage:")
    print(sys.argv[0] + " mod [options]")
    print("")
    print("Options:")
    print(
        '''
--fill      adds only missing files to an existing mod (instead of
            failing when directory exists).

[alias to]  (do not actually use brackets) If you specify any two
            options without --, the first will be an alias and the
            second will be convert_to. The alias options are only for
            mods that are aliases, as a shortcut to creating a mostly
            complete mod (other than copyright information and
            description) with only this script.
'''
    )
    print("")
    print("Examples:")
    print(sys.argv[0] + " mod_name")
    print(sys.argv[0] + " mod_name --fill")
    print(sys.argv[0] + " mod_name modname:item_name other_modname:convert_to")
    print(sys.argv[0] + " mod_name mobsmod:mob_name other_mobsmod:convert_to")
    print("")
    print("")


licSrc = "example_license.txt"
licDestName = "LICENSE.txt"
licDesc = "MIT License"
if not os.path.isfile(licSrc):
    tryLicSrc = os.path.join(myDir, licSrc)
    if not os.path.isfile(tryLicSrc):
        print("ERROR: missing " + licSrc)
        exit(1)
    else:
        licSrc = tryLicSrc
toMod = None
fromName = None
toName = None
extraArgCount = 0
enableFill = False
options = []
for i in range(1, len(sys.argv)):
    if sys.argv[i] == "--fill":
        extraArgCount += 1
        enableFill = True
    else:
        if (len(sys.argv[i]) >= 2) and (sys.argv[i][:2] == "--"):
            usage()
            customExit("Invalid option: " + sys.argv[i])
        options.append(sys.argv[i])
if (len(options) != 1) and (len(options) != 3):
    usage()
    exit(1)
thisName = options[0]
if os.path.isdir(thisName):
    if not enableFill:
        print("")
        print("ERROR: A mod named " + thisName + " cannot be ")
        print("generated when the directory already exists.")
        print("")
        exit(1)
else:
    os.mkdir(thisName)
if (len(options) == 3):
    fromName = options[1]
    toName = options[2]
    delimI = toName.rfind(":")
    if delimI > -1:
        toMod = toName[:delimI]
        if toMod.find(":") > -1:
            usage()
            customExit("Your modname contains too many colons.")
            exit(1)
    else:
        toMod = "default"

mobAPI = None
if toMod is not None:
    if not os.path.isfile(os.path.join(thisName, "depends.txt")):
        dependsOut = open(os.path.join(thisName, "depends.txt"), 'w')
        dependsOut.write(toMod+"\n")
        dependsOut.close()
    if toMod.find("mob") > -1:
        mobAPI = toMod

if not os.path.isfile(os.path.join(thisName, "description.txt")):
    descOut = open(os.path.join(thisName, "description.txt"), 'w')
    descOut.write("\n")
    descOut.close()

if not os.path.isfile(os.path.join(thisName, "mod.conf")):
    confOut = open(os.path.join(thisName, "mod.conf"), 'w')
    confOut.write("name = "+thisName+"\n")
    confOut.close()

if not os.path.isfile(os.path.join(thisName, "readme.md")):
    readmeOut = open(os.path.join(thisName, "readme.md"), 'w')
    readmeLine1 = thisName + " Minetest Mod"
    readmeOut.write(readmeLine1+"\n")
    readmeOut.write("="*len(readmeLine1)+"\n")
    readmeOut.write("See description.txt\n")
    readmeOut.write("\n")
    readmeOut.write("## License\n")
    readmeOut.write("See " + licDestName + "\n")
    readmeOut.close()

licDest = os.path.join(thisName, licDestName)
if not os.path.isfile(licDest):
    shutil.copyfile(licSrc, licDest)
luaOut = None
if not os.path.isfile(os.path.join(thisName, "init.lua")):
    luaOut = open(os.path.join(thisName, "init.lua"), 'w')
    # luaOut.write("#!/usr/bin/env lua\n")
    luaOut.write("-- " + sys.argv[0] + " (EnlivenMinetest) generated\n")
    luaOut.write("-- the original version of this file.\n")
fromMod = None  # not required
step0 = ""

if (len(options) == 3):
    delimI = fromName.find(":")
    if delimI > -1:
        fromMod = fromName[:delimI]
    else:
        fromMod = ""
    apiLinePrefix = ""
    mobLinePrefix = ""
    if luaOut is not None:
        if mobAPI is not None:
            apiLinePrefix = "-- "
        else:
            mobLinePrefix = "-- "
            luaOut.write("-- If your mobs API doesn't contain the\n")
            luaOut.write("-- word 'mobs', your alias method is not\n")
            luaOut.write("-- known. In that case, you may have to\n")
            luaOut.write("-- change minetest.register_alias to your\n")
            luaOut.write("-- mob API's (if your alias is for a mob).\n")
        luaOut.write(mobLinePrefix + mobAPI + ':alias_mob("'
                     + fromName + '", "' + toName + '")' + "\n")
        luaOut.write(apiLinePrefix + 'minetest.register_alias("'
                     + fromName + '", "' + toName + '")' + "\n")
else:
    step0 = "Add your code init.lua."
if luaOut is not None:
    luaOut.write("\n")
    luaOut.close()

print("")
print("")
print(step0)
print("The new mod is the " + thisName + " folder. Remember to:")
ender = "."
if (toMod is not None) and (len(toMod) > 0):
    ender = ""
print("1. Edit depends.txt if your mod requires some mod" + ender)
if (toMod is not None) and (len(toMod) > 0):
    print("   other than '" + toMod + "'.")
print("")
print("2. Edit description.txt to contain a brief description of")
print("   your mod (less than 100 characters).")
print("")
print("3. Edit LICENSE.txt and add the year and the name of all ")
print("   authors, and change the license if desired (The included")
print("   " + licSrc)
print("   should be the " + licDesc + ".")
print(
    '''   The MIT License is good for Minetest mods so they can be used
   most widely such as on app stores where replacing the program as per
   the GPL v3 is not compliant with mobile OS security--the license of
   most Minetest releases is the MIT License). Some joke licenses exist
   but DO NOT protect your work in cases where they explicitly allow
   others to copy your work and claim it as their own especially if they
   modify it in any way. They would just be doing what you said they
   could do!
'''
)
print("")
print("")
