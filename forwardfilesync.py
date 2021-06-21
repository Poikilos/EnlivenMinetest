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
CMD_MKDIR = "mkdir -p"

if platform.system() == "Windows":
    CMD_RMTREE = "rd /S /Q"
    # /S: Delete all files and subdirectories and the directory itself.
    # /Q: Do not ask on global wildcard.
    CMD_RM = "del /Q /F"
    # /Q: Do not confirm on wildcard.
    # /F: Force deleting read-only files.
    CMD_COMMENT = "REM "
    CMD_CP = "COPY"
    CMD_MKDIR = "MD"

def path_join_all(names):
    result = names[0]
    for i in range(1, len(names)):
        result = os.path.join(result, names[i])
    return result


def trim_branch(src, dst, dot_hidden=True, verbose=True):
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
                os.remove(dst_sub_path)
            else:
                print("{} \"{}\"...".format(CMD_RMTREE, dst_sub_path))
                shutil.rmtree(dst_sub_path)


def update_tree(src, dst, level=0, do_trim=False, dot_hidden=False,
                verbose=True):
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
    indent = " "*level
    if level <= 1:
        print(indent + CMD_COMMENT + "* synchronizing with \"{}\""
              "".format(dst))
    if not os.path.isdir(dst):
        if verbose:
            print(indent + CMD_MKDIR + " \"{}\"".format(dst))
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
            if not allow_copy:
                continue
            if os.path.isdir(sub_path):
                update_tree(sub_path, dst_sub_path, level=level+1,
                            do_trim=do_trim, dot_hidden=dot_hidden,
                            verbose=verbose)
            elif os.path.isfile(sub_path):
                mode = None
                sub_mt = os.path.getmtime(sub_path)
                dst_sub_mt = os.path.getmtime(dst_sub_path)
                if not os.path.isfile(dst_sub_path):
                    mode = "+"
                elif sub_mt > dst_sub_mt:
                    mode = ">"
                elif sub_mt < dst_sub_mt:
                    # mode = "<"
                    # Don't set any mode, or the newer file will be overwritten!
                    print(indent + CMD_COMMENT
                          + "WARNING: \"{}\" is newer on destination!"
                          "".format(dst_sub_path))
                if mode is None:
                    continue
                try:
                    if verbose:
                        if mode == ">":
                            print(indent + CMD_CP + "update:")
                        print(indent + CMD_CP + " \"{}\" \"{}\""
                              "".format(sub_path, dst_sub_path))
                    # shutil.copyfile(sub_path, dst_sub_path)
                    shutil.copy2(sub_path, dst_sub_path)
                except PermissionError:
                    print(indent + CMD_COMMENT + "PermissionError:")
                    print(indent + CMD_COMMENT + "    {} \"{}\" \"{}\""
                          "".format(CMD_CP, sub_path, dst_sub_path))
                    pass

USAGE = '''
Syntax:
forwardfilesync.py <source> <destination> [options]

--hidden    Process files & folders even if named starting with '.'.
--delete    Delete files & folders on the destination if not in source.

'''

def usage():
    print(USAGE)

def main():
    flags = {}
    flags["hidden"] = False
    flags["delete"] = False
    
    if len(sys.argv) < 3:
        usage()
        print("Error: You must provide at least a source and destination.")
        exit(1)

    src = sys.argv[1]
    dst = sys.argv[2]

    for argI in range(3, len(sys.argv)):
        arg = sys.argv[argI]
        if (arg[:2] != "--"):
            usage()
            print("Error: The option \"{}\" is not formatted correctly"
                  " since it doesn't start with \"--\". If it is part"
                  " of a path with spaces, put the path in quotes."
                  "".format(sys.argv[argI]))
            exit(1)
        name = arg[2:]
        if name not in flags:
            usage()
            print("Error: There is no option \"{}\". If it is part of a"
                  " path with spaces, put the path in quotes."
                  "".format(sys.argv[argI]))
            exit(1)
        flags[name] = True
    print(CMD_COMMENT + "Using options:")
    for k,v in flags.items():
        print(CMD_COMMENT + "{}: {}".format(k, v))

    update_tree(
        src,
        dst,
        do_trim=flags["delete"] is True,
        dot_hidden=flags["hidden"] is True,
    )
    print(CMD_COMMENT + "Done.")
    


if __name__ == "__main__":
    main()
