#!/usr/bin/env python
import os
import shutil

copy_dot_hidden_enable = False
# NOT YET IMPEMENTED: delete_if_not_on_src_enable = True

def path_join_all(names):
    result = names[0]
    for i in range(1, len(names)):
        result = os.path.join(result, names[i])
    return result

# Creates dst if not present, then copies everything from src to dst recursively
def update_tree(src, dst, level=0):
    folder_path = src
    if level <= 1:
        print("#" + " "*level + "synchronizing with \"" + dst + "\"")
    if not os.path.isdir(dst):
        os.makedirs(dst)
    if os.path.isdir(folder_path):
        for sub_name in os.listdir(folder_path):
            sub_path = os.path.join(folder_path, sub_name)
            dst_sub_path = os.path.join(dst, sub_name)
            if (copy_dot_hidden_enable or sub_name[:1]!=".") and os.path.isdir(sub_path):
                update_tree(sub_path, dst_sub_path, level+1)
            if (copy_dot_hidden_enable or sub_name[:1]!=".") and os.path.isfile(sub_path):
                shutil.copyfile(sub_path, dst_sub_path)
