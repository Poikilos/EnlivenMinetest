import os
import platform
# import shlex
import shutil
import sys
import subprocess

MODULE_DIR = os.path.dirname(os.path.realpath(__file__))
REPO_DIR = os.path.dirname(MODULE_DIR)
if __name__ == "__main__":
    # Allow importing pyenliven if running within
    sys.path.insert(0, REPO_DIR)


def echo0(*args, **kwargs):
    print(*args, file=sys.stderr, **kwargs)


DIFF_CMD_PARTS = None

if platform.system() == "Windows":
    HOME = os.environ['USERPROFILE']
    try_diff = shutil.which("diff")
    # ^ Requires Python 3.3 or later (not 2.7)
    if try_diff is not None:
        DIFF_CMD_PARTS = ["diff"]
    else:
        DIFF_CMD_PARTS = ["fc"]
else:
    HOME = os.environ['HOME']
    DIFF_CMD_PARTS = ["diff"]


def diff_only_head(base, head, rel=None, more_1char_args=None, depth=0):
    """Compare two directories or files.

    Files not in head will not be checked!

    Therefore recursion here differs from a recursive call to GNU diff
    (diff -ru).

    The base and head are both at depth 0 and must be considered the
    root of the relative path.

    Args:
        base (str): Path to original code (file or folder).
        head (str): Path to new code (file or folder).
        more_1char_args (Union[str,list[str]], optional): args. Defaults
            to "-wb", or if using Windows, then "/W" if diff is not
            present in PATH (in that case, fc is used).
        rel (str, optional): Leave as None. This will be set
            automatically for recursion.
        depth (int, optional): Leave as 0. This will be set
            automatically for recursion.

    Raises:
        FileNotFoundError: If base does not exist (and depth is 0).
        FileNotFoundError: If head does not exist (and depth is 0).
        FileNotFoundError: If diff is not in PATH.
        ValueError: If one of the paths is a folder but the other is a
            file.

    Returns:
        list(dict): A list of differing files as info dicts, each with:
        - 'rel': The path relative to head.
        - 'new': True if not in base, otherwise False or not present.
        - 'code': Return code (1 if file in head&base differ)
    """
    diffs = []
    if not DIFF_CMD_PARTS:
        ok_commands = 'diff'
        if platform.system() == "Windows":
            ok_commands = ['fc', 'diff']
        raise FileNotFoundError("There is no {} in your PATH."
                                "".format(ok_commands))
    args_1char = None
    is_binary = False
    if more_1char_args is None:
        if platform.system() == "Windows":
            if not is_binary:
                args_1char = ["/W"]  # ignore whitespace
            else:
                args_1char = ["/B"]  # binary comparison
        else:
            if not is_binary:
                args_1char = ["-wb"]
                # -b: ignore changes in the amount of whitespace
                # -w: ignore all white space (better for code since
                #     "a=1" is same as "a == 1", otherwise tokenizing
                #     the specific language would be necessary)
                # -a: --text  treat all files as text and
                #     --strip-trailing-cr  strip trailing carriage
                #         return
                # -E, --ignore-tab-expansion
    else:
        if more_1char_args.startswith("-"):
            if DIFF_CMD_PARTS[0].lower() == "fc":
                raise ValueError(
                    "diff wasn't in your PATH so fc is being used,"
                    " but it only accepts options"
                    " starting with '/'"
                    " (got \"{}\")".format(more_1char_args)
                )
        if isinstance(more_1char_args, (list, tuple)):
            args_1char = more_1char_args
        else:
            # allow string too (split if has space, otherwise convert
            # to 1-long list still)
            args_1char = more_1char_args.strip().split()

    whats = [None, None]
    if rel:
        base_path = os.path.join(base, rel)
        head_path = os.path.join(head, rel)
    else:
        base_path = base
        head_path = head
    paths = (base_path, head_path)
    names = ("base", "head")
    for i, path in enumerate(paths):
        if not os.path.exists(path):
            if depth == 0:
                raise FileNotFoundError(
                    "{}: {}".format(names[i], path)
                )
        else:
            if os.path.isdir(path):
                whats[i] = "folder"
            else:
                whats[i] = "file"

    if whats[0] is None:
        whats[0] = whats[1]
    if whats[1] is None:
        whats[1] = whats[0]
    # ^ These are here since FileNotFoundError *only* is on depth==0.

    if whats[0] != whats[1]:
        raise ValueError(
            'cannot compare {}:"{}" to {}:"{}"'
            ''.format(whats[0], base_path, whats[1], head_path)
        )
    if "folder" in whats:
        # if "r" not in more_1char_args:
        #     more_1char_args += "r"
        # ^ Not necessary since recursion needs to be done in this code
        #   (See docstring).
        for sub in os.listdir(head_path):
            sub_rel = os.path.join(rel, sub) if rel else sub
            diffs += diff_only_head(
                base,
                head,
                rel=sub_rel,
                more_1char_args=more_1char_args,
                depth=depth+1,
            )
    else:
        # echo0('base={}:"{}"'.format(whats[0], paths[0]))
        # echo0('head={}:"{}"'.format(whats[1], paths[1]))
        # file, so actually compare
        if not os.path.isfile(base_path):
            # echo0("^ not in base")
            if os.path.isdir(base_path):
                raise NotImplementedError('should not be dir: "{}"'
                                          ''.format(base_path))
                # ^ Should have been handled in "if" case above.
            return [{
                'code': 1,
                'rel': rel,
                'new': True,
            }]
        # echo0("^ in base")
        cmd_parts = DIFF_CMD_PARTS.copy()
        # echo0("args_1char={}".format(args_1char))
        if args_1char:
            cmd_parts += args_1char
        cmd_parts += [base_path, head_path]
        # echo0("\n\n{}".format(shlex.join(cmd_parts)))
        child = subprocess.Popen(cmd_parts, stdout=subprocess.PIPE)
        streamdata = child.communicate()[0]
        data = streamdata
        if sys.version_info.major >= 3:
            data = streamdata.decode(sys.stdout.encoding)
        print(data)
        rc = child.returncode
        if rc == 0:
            # echo0("^ files are the same")
            return []  # Do not add any diff entry.
        else:
            pass
            # echo0("^ files differ")
        return [{
            'code': rc,
            'rel': rel,
        }]
    return diffs  # folder, so return every sub's diff(s) ([] if None)


def get_shallowest_files_sub(root, log_level=0, filter=None):
    """Get the shallowest folder relative to root that contains file(s).

    Args:
        root (str): The folder to check for files recursively.
        rel (str, optional): Leave blank (set automatically during
            recursion).
        depth (int, optional): Leave as 0 (set automatically during
            recursion).
        filter (Union[str,list[str]], optional): Filename or list of
            filenames to find (None/0/""/False/"*"/[] will match any
            file).

    Returns:
        Union(str, None): Get the relative dir that contains file(s).
    """
    return _get_shallowest_files_sub(
        root,
        log_level=log_level,
        filter=filter,
    )


def _get_shallowest_files_sub(root, rel=None, depth=0, log_level=0,
                              filter=None):
    if isinstance(filter, str):
        if filter == "*":
            filter = None
        filter = [filter]
    if root is None:
        raise ValueError("root is {}".format(root))
    if rel and rel.startswith(os.path.sep):
        raise ValueError(
            "rel cannot start with '{}'"
            " because that would override root (depth={})"
            "".format(os.path.sep, depth)
        )

    parent = os.path.join(root, rel) if rel else root
    for sub in os.listdir(parent):
        sub_path = os.path.join(parent, sub)
        if os.path.isfile(sub_path):
            if (not filter) or (sub in filter):
                return rel
    # ^ Check *all* subs first, in case dir is listed before file.
    #   The *parent* has file(s), so return parent
    #   (must check if file *before* recursion
    #   or deeper folder with file may be found):
    for sub in os.listdir(parent):
        sub_path = os.path.join(parent, sub)
        if os.path.isfile(sub_path):
            continue
        sub_rel = os.path.join(rel, sub) if rel else sub
        if log_level > 0:
            pass
            # echo0("\ndepth={}".format(depth))
            # echo0("root:{}".format(root))
            # echo0("+rel:{}".format(rel))
            # echo0("=parent:{}".format(parent))
            # echo0("sub={}".format(sub))
            # echo0("sub_rel={}".format(sub_rel))
        found_path = _get_shallowest_files_sub(
            root,
            rel=sub_rel,
            depth=depth+1,
            log_level=log_level,
            filter=filter,
        )

        if found_path:
            return found_path
        continue

    return None


def find_mod(parent, name):
    return _find_sub_with_known_files(
        parent,
        name,
        filter=["init.lua", "mod.conf", "depends.txt", "description.txt"],
    )


def find_modpack(parent, name):
    return _find_sub_with_known_files(
        parent,
        name,
        filter=["modpack.txt", "modpack.conf"],
    )


def _find_sub_with_known_files(parent, name, root_slash=None, filter=None):
    """Get relative path to Minetest mod (or "" if parent is it).

    Args:
        parent (str): Folder to search for Minetest mod files.
        name (str): Name of the mod to find. It can still be found if it
            is the same name as the parent, so if parent is "mods",
            then "3d_armor/3d_armor" would be the result rather than
            "3d_armor".
        root_slash (str, optional): Leave as None. Recursion sets it
            automatically. Defaults to None.
        filter (list[str]): Defaults to files found in a mod,
            but can be changed to find a modpack or anything else.

    Returns:
        str: relative path to Minetest mod (or "" if parent is it),
            or None if not Found.
    """
    if not root_slash:
        root_slash = parent + os.path.sep
    _, parent_name = os.path.split(parent)

    if parent_name == name:
        for sub in os.listdir(parent):
            sub_path = os.path.join(parent, sub)
            if not os.path.isfile(sub_path):
                continue
            if sub in filter:
                # Then parent is the mod. End the search
                #   and return *relative* path to mod
                #   (with root_slash removed, so
                #   "" if parent matches before recursion)
                return parent[len(root_slash):]
    # ^ must iterate files *before* recursion to avoid deeper false
    #   positive suchas backup folder inside of a mod that has a
    #   file in filter.
    for sub in os.listdir(parent):
        sub_path = os.path.join(parent, sub)
        if os.path.isfile(sub_path):
            continue
        found = _find_sub_with_known_files(
            sub_path,
            name,
            root_slash=root_slash,
            filter=filter,
        )
        if found:
            return found
    return None


def main():
    bases = (
        "/opt/minebest/assemble/bucket_game",
        "/opt/minebest/mtkit/minetest/src"
    )
    heads = (
        os.path.join(REPO_DIR, "Bucket_Game-branches"),
        os.path.join(HOME, "metaprojects", "pull-requests", "OldCoder")
    )
    for base in bases:
        if not os.path.isdir(base):
            echo0('Warning: There is no base "{}".'.format(base))
            continue
        for head in heads:
            for head_sub in os.listdir(head):
                head_sub_path = os.path.join(head, head_sub)
                if os.path.isfile(head_sub_path):
                    # echo0('Warning: Only folders, skipped "{}"'
                    #       ''.format(head_sub))
                    continue
                if "original" in head_sub:
                    echo0('INFO: skipped original: "{}"'
                          ''.format(head_sub))
                    continue
                mod_rel = get_shallowest_files_sub(
                    head_sub_path,
                    filter=["init.lua", "mod.conf", "depends.txt",
                            "description.txt"],
                )
                modpack_rel = get_shallowest_files_sub(
                    head_sub_path,
                    filter=["modpack.txt"],
                )
                if mod_rel and not modpack_rel:
                    mod_parent = os.path.dirname(os.path.join(head_sub_path,
                                                              mod_rel))
                    mod_parent_rel = mod_parent[len(head_sub_path)+1:]
                    # ^ +1 no os.path.sep
                    _, mod_parent_name = os.path.split(mod_parent)
                    if mod_parent_rel and (mod_parent_name not in ["mods"]):
                        echo0('Warning: No modpack.txt,'
                              ' so assuming modpack={} ("{}")'
                              ''.format(mod_parent_name, mod_parent))
                if mod_rel:
                    echo0('mod="{}"'.format(mod_rel))
                else:
                    echo0('Warning: mod not identified in "{}"'
                          ''.format(head_sub))

    return 0


if __name__ == "__main__":
    sys.exit(main())
