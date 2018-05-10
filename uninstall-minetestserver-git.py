#!/usr/bin/env python3
import os
import platform
CMD_REM = "#"
CMD_RM = "rm "
CMD_RMDIR = "rmdir "
if platform.system() == "Windows":
    CMD_REM = "REM "
    CMD_RM = "del "
    CMD_RMDIR = "rd "
#profile_path = None
#if 'HOME' in os.environ:
#    profile_path = os.environ['HOME']
#elif 'USERPROFILE' in os.environ:
#    profile_path = os.environ['USERPROFILE']
#downloads_path = os.path.join(profile_path, "Downloads")
#repo_path = os.path.join(downloads_path, "minetest")
#if not os.path.isdir(repo_path):
#    repo_path = os.path.join(profile_path, "minetest")
#if not os.path.isdir(repo_path):
#    print("ERROR: Nothing done since there is no minetest sourcecode folder in " + downloads_path + " (nor " + profile_path + ")")
#    exit(1)
install_manifest_name = "install_manifest.txt"
#install_manifest_path = os.path.join(repo_path, install_manifest_name)
#if not os.path.isfile(install_manifest_path):
#    print("ERROR: nothing done since there is no " +
#        install_manifest_name + " in '" + repo_path +
#        "'. The file would only be present if you " +
#        "installed minetest from sourcecode" +
#        "(otherwise this uninstaller is not for you).")
#    exit(2)
if not os.path.isfile(install_manifest_name):
    print("ERROR: nothing done since there is no " +
        install_manifest_name + " in the current " +
        "directory. You must run: ")
    print("   sudo python3 "+os.path.abspath(__file__))
    print("from the minetest sourcecode (repo) directory.")
    exit(2)
directories = []
print("Removing files...")
f_removed_count = 0
f_skipped_count = 0
f_failed_count = 0
retry_lines = []
with open(install_manifest_name, 'r') as ins:
    original_line = True
    while original_line:
        original_line = ins.readline()
        if original_line:
            line = original_line.rstrip()  # remove trailing newline
            if len(line)>0:
                d_path = os.path.dirname(line)
                if d_path not in directories:
                    if "minetest" in d_path:
                        directories.append(d_path)
                        # else must be a system directory like
                        # /usr/local/share/applications
                if os.path.isfile(line):
                    os.remove(line)
                    if os.path.isfile(line):
                        f_failed_count += 1
                        retry_lines.append(CMD_RM+'"'+line+'"')
                    else:
                        f_removed_count += 1
                else:
                    f_skipped_count += 1

print("Removed " + str(f_removed_count) + " file(s) (skipped not present:" +
      str(f_skipped_count) + "; failed:" + str(f_failed_count) + ")")

#NOTE: the next line makes ASCENDING (by len) list of TUPLES (name,len)
sorted_directories = [(x, len(x)) for x in sorted(directories, key = len)]

print("Removing folders...")
#NOTE: they are sorted ASCENDING so start at end:
d_removed_count = 0
d_skipped_count = 0
d_failed_count = 0

#still leaves:
# /usr/local/share/minetest/games/minetest_game/mods
# /usr/local/share/minetest/textures/base/pack/:
#   down_arrow.png  left_arrow.png  right_arrow.png  up_arrow.png
# /usr/local/share/minetest/games/minimal/mods
# so:
try_files = ["depends.txt", "down_arrow.png", "left_arrow.png", "right_arrow.png", "up_arrow.png"]
try_dirs = ["mods"]

extra_dirs = []
ed_failed_count = 0
ed_removed_count = 0
extra_files = []
e_failed_count = 0
e_removed_count = 0
for i in reversed(range(len(sorted_directories))):
    d_path = sorted_directories[i][0]
#for d in reversed(sorted_directories):
#    d_path = d[0]
#    print("checking "+str(d_path))
    if os.path.isdir(d_path):
        try:
            for try_name in try_files:
                try_path = os.path.join(d_path, try_name)
                if os.path.isfile(try_path):
                    extra_files.append(try_path)
                    print('Removing known extra file: "' + try_path + '"')
                    try:
                        os.remove(try_path)
                        e_removed_count += 1
                    except Exception as e:
                        e_failed_count += 1
                        retry_lines.append(CMD_RM+'"'+try_path+'"')
                        print(str(e))
            for try_name in try_dirs:
                try_path = os.path.join(d_path, try_name)
                if os.path.isdir(try_path):
                    extra_dirs.append(try_path)
                    print('Removing known extra folder: "' + try_path + '"')
                    try:
                        os.rmdir(try_path)
                        ed_removed_count += 1
                    except Exception as e:
                        ed_failed_count += 1
                        retry_lines.append(CMD_RMDIR+'"'+try_path+'"')
                        print(str(e))
            os.rmdir(d_path)
        except Exception as e:
            print(str(e))
        if os.path.isdir(d_path):
            d_failed_count += 1
            retry_lines.append(CMD_RMDIR+'"'+d_path+'"')
        else:
            d_removed_count += 1
    else:
        d_skipped_count += 1
print("Removed " + str(d_removed_count) + " folder(s) (skipped not present:" +
      str(d_skipped_count) + "; failed:" + str(d_failed_count) + ")")
if e_failed_count > 0:
    print("(failed to remove " + e_failed_count + " known extra file(s) " +
          "(will be shown under FAILURES below)")
if ed_failed_count > 0:
    print("(failed to remove " + ed_failed_count + " known extra folder(s) " +
          "(will be shown under FAILURES below)")
print("Removed " + str(d_removed_count) + " folder(s) (skipped not present:" +
      str(d_skipped_count) + "; failed:" + str(d_failed_count) + ")")

if f_failed_count+d_failed_count+ed_failed_count <= 0:
    print("")
    if f_removed_count+d_removed_count <= 0:
        print("Nothing to do (minetest+minetestserver has 0 known files on system--you apparently already uninstalled the local version that was installed using 'sudo make install')")
    else:
        print("OK [finished uninstalling all installed files]")
    print("")
else:
    print("")
    print("")
    print(CMD_REM+"FAILURES:")
    for rl in retry_lines:
        print(rl)
    print("")
    print("In case of any failures are counted above, "
          "try running this script with administrative privileges."
          "If any more remain, you may have to remove them manually.")
    print("")
    print("")
if not ins.closed:
    print("ERROR: ins was not closed (this should never happen)--"
          "closing manually...")
    ins.close()
