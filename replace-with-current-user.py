#!/usr/bin/env python2
import os
from os.path import expanduser

filenames = list()
filenames.append("chunkymap-cronjob")
filenames.append("chunkymap-regen.sh")
filenames.append("set-minutely-crontab-job.sh")

home_path = expanduser("~")
home_minetest_chunkymap_path = os.path.join(home_path,"minetest/util")
#for dirname, dirnames, filenames in os.walk(home_minetest_chunkymap_path):
if "\\" not in home_minetest_chunkymap_path:
    if os.path.isdir(home_minetest_chunkymap_path):
        for filename in filenames:
            file_path = os.path.join(home_minetest_chunkymap_path, filename)
            temp_path = file_path+".tmp"
            os.rename(file_path, temp_path)
            if not os.path.isfile(file_path):
                ins = open(temp_path, 'r')
                outs = open(file_path, 'w')
                line = True
                while line:
                    line = ins.readline()
                    if line:
                        line = line.replace("/home/owner", home_path)
                        outs.write(line+"\n")
                outs.close()
                os.remove(temp_path)
                ins.close()
            else:
                print "FAILED to rewrite the file '"+file_path+"' (to change minetest util path to '"+home_minetest_chunkymap_path+"')--perhaps it is in use. Make the file writeable then try running "+__FILE__+" again."
                input("Press enter to continue...")
    else:
        print "FAILED to find '"+home_minetest_chunkymap_path+"'"
        print "Please install a compatible version of minetest-server package, run minetestserver once, then if you were running a chunkymap installer that called this py file, re-run that installer (otherwise re-run this script if you are sure that installer was successful)."
        input("Press enter to continue...")
else:
    print "This script only works on GNU/Linux systems (it is not needed on Windows, since on Windows, chunkymap will detect the scripts and colors.txt in the same folder as itself instead of using the minecraftserver minetest/util folder)"
