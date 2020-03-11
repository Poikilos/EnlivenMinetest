#!/usr/bin/env python
import os
import platform


def doDie(msg, error_code=1):
    print()
    print(msg)
    print()
    print()
    exit(error_code)


rem_cmd = "#"
rm_cmd = "rm "
rmdir_cmd = "rmdir "
if platform.system() == "Windows":
    rm_cmd = "DEL "
    rmdir_cmd = "RD "
    rem_cmd = "REM "
profile_path1 = os.environ.get('HOME')
profile_path = profile_path1
profile_path2 = os.environ.get('USERPROFILE')
if profile_path2 is not None:
    profile_path = profile_path2
    if profile_path1 is not None:
        print(rem_cmd + "WARNING: HOME is present, but USERPROFILE '"
              + profile_path + "' is being used.")
else:
    if profile_path1 is None:
        doDie(rem_cmd + "ERROR: There is nothing to do since neither"
              + " HOME nor USERPROFILE is present.")

mnf_name = "install_manifest.txt"
mnf_path = os.path.join(profile_path, mnf_name)

unsorted_list = []

if not os.path.isfile(mnf_path):
    doDie(rem_cmd + "Uninstall cannot continue since '" + mnf_path
          + "' is missing.")

with open(mnf_path) as fp:
    for cnt, line_original in enumerate(fp):
        # print("Line {}: {}".format(cnt, line))
        line = line_original.strip()
        if len(line) > 0:
            unsorted_list.append(line)

if len(unsorted_list) < 1:
    doDie(rem_cmd + "ERROR: There are no files in the manifest '"
          + mnf_path + "'")

# See https://stackoverflow.com/questions/4659524/\
# how-to-sort-by-length-of-string-followed-by-alphabetical-order
sorted_list = sorted(unsorted_list, key=len, reverse=True)
# reverse: descending
# or (also reverse):
# the_list.sort(key=lambda item: (-len(item), item))

print(rem_cmd + "Uninstalling...")
not_removed_files = []
not_removed_dirs = []
does_not_exist = []
file_count = 0
dir_count = 0
for path in sorted_list:
    if os.path.isfile(path):
        if path[0:1] == ".":
            print(rm_cmd + "\"" + path + "\"")
            not_removed_files.append(path)
            continue
        try:
            os.remove(path)
            file_count += 1
        except PermissionError:
            not_removed_files.append(path)
    elif os.path.isdir(path):
        if path[0:1] == ".":
            print(rmdir_cmd + "\"" + path + "\"")
            not_removed_dirs.append(path)
            continue
        try:
            os.rmdir(path)
            dir_count += 1
        except PermissionError:
            not_removed_dirs.append(path)
    else:
        does_not_exist.append(path)

if len(does_not_exist) > 0:
    if len(does_not_exist) == len(sorted_list):
        doDie("  " + rem_cmd + " The program is not installed such as"
              + " at '" + sorted_list[-1] + "'.")

show_dot_warning = True
print(rem_cmd + "Uninstall is complete.")
print(rem_cmd + "- files: " + str(file_count))
print(rem_cmd + "- directories: " + str(dir_count))
print(rem_cmd + "- missing: " + len(does_not_exist))
if (len(not_removed_files) + len(not_removed_dirs)) > 0:
    for path in not_removed_files:
        if path[0:1] == ".":
            if show_dot_warning:
                print(rem_cmd + "Paths starting with '.' are not yet"
                      " implemented.")
                show_dot_warning = False
        print(rm_cmd + "\"" + path + "\"")
    for path in not_removed_dirs:
        print(rmdir_cmd + "\"" + path + "\"")
    print(rem_cmd + "Deleting items above FAILED:")
    print("  " + rem_cmd + "- files: " + str(not_removed_file_count))
    print("  " + rem_cmd + "- directories: "
          + str(not_removed_dir_count))

print("")
print("")
