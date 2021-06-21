#!/usr/bin/env python
import os
import sys
import shutil
import platform

# copy_dot_hidden_enable = False
# delete_if_not_on_src_enable = True

CMD_RMTREE = "rm -Rf"
CMD_RM = "rm -f"
CMD_COMMENT = "# "
CMD_CP = "cp"

if platform.system() == "Windows":
    CMD_RMTREE = "rd /S /Q"
    # /S: Delete all files and subdirectories and the directory itself.
    # /Q: Do not ask on global wildcard.
    CMD_RM = "del /Q /F"
    # /Q: Do not confirm on wildcard.
    # /F: Force deleting read-only files.
    CMD_COMMENT = "REM "
    CMD_CP = "COPY"

def path_join_all(names):
    result = names[0]
    for i in range(1, len(names)):
        result = os.path.join(result, names[i])
    return result


def trim_branch(src, dst, dot_hidden=True):
    '''
    Explore dst non-recursively and delete files
    and subdirectories recursively that are not present on src.
    
    Keyword arguments:
    dot_hidden -- Operate on files and directories even if they are
                  hidden by starting with '.'.
    '''
    for sub_name in os.listdir(dst):
        src_sub_path = os.path.join(src, sub_name)
        dst_sub_path = os.path.join(dst, sub_name)
        if not dot_hidden:
            if sub_name.startswith("."):
                continue
        if not os.path.exists(src_sub_path):
            if os.path.isfile(dst_sub_path):
                print("{} \"{}\"...".format(CMD_RM, dst_sub_path))
                # os.remove(dst_sub_path)
            else:
                print("{} \"{}\"...".format(CMD_RMTREE, dst_sub_path))
                # shutil.rmtree(dst_sub_path)


def update_tree(src, dst, level=0, do_trim=True, dot_hidden=False):
    '''
    Creates dst if not present, then copies everything from src to dst
    recursively.
    
    Keyword arguments:
    do_trim -- Delete files and directories from dst that are not on
               src.
    dot_hidden --  Copy files and directories even if hidden by
                   starting with '.'.
    '''
    folder_path = src
    if level <= 1:
        print(CMD_COMMENT + " "*level + "synchronizing with \"{}\""
              "".format(dst))
    if not os.path.isdir(dst):
        os.makedirs(dst)
    else:
        if do_trim:
            trim_branch(src, dst, dot_hidden=dot_hidden)
    if os.path.isdir(folder_path):
        for sub_name in os.listdir(folder_path):
            sub_path = os.path.join(folder_path, sub_name)
            dst_sub_path = os.path.join(dst, sub_name)
            allow_copy = True
            if not dot_hidden:
                allow_copy = not sub_name.startswith(".")
            if allow_copy and os.path.isdir(sub_path):
                update_tree(sub_path, dst_sub_path, level+1)
            if allow_copy and os.path.isfile(sub_path):
                try:
                    shutil.copyfile(sub_path, dst_sub_path)
                except PermissionError:
                    print(CMD_COMMENT + "PermissionError:")
                    print(CMD_COMMENT + "  {} \"{}\" \"{}\""
                          "".format(CMD_CP, sub_path, dst_sub_path))
                    pass


def main():
    flags = {}
    flags["hidden"] = False
    if len(sys.argv) == 3:
        pass
    elif (len(sys.argv) == 4) and (sys.argv[3][:2] == "--"):
        name = sys.argv[3][2:]
        if name not in flags:
            print("Error: The syntax is invalid. Expected:")
            print("forwardfilesync.py <source> <destination>")
            print("forwardfilesync.py <source> <destination> --hidden")
        flags[name] = True
    else:
        print("Error: The syntax is invalid. Expected:")
        print("forwardfilesync.py <source> <destination>")
        print("forwardfilesync.py <source> <destination> --hidden")
        exit(1)
    src = sys.argv[1]
    dst = sys.argv[2]
    update_tree(src, dst, dot_hidden=flags["hidden"])


if __name__ == "__main__":
    main()
