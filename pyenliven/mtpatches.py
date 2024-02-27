#!/usr/bin/env python3
'''
mtpatches
---------
Check for Minetest game patches stored in the form of regular
text/binary files that can be directly copied to the program.

Usage:
mtpatches.py [options]

Options:
--skip-missing        Do not list files in heads that are not in sources.
'''
import os
import platform
import shlex
import shutil
import sys
import subprocess
from binaryornot.check import is_binary


class Fore:
    """Print these to change console color
    (emulate colorama)
    See <https://gist.github.com/kamito/704813>

    Example: Use Fore.RED as if you had done
    `from colorama import Fore`, but you don't need to
    import anything from colorama.
    """
    RED = "\033[31m"
    GREEN = "\033[32m"
    YELLOW = "\033[33m"
    BLUE = "\033[34m"
    PURPLE = "\033[35m"
    CYAN = "\033[36m"
    WHITE = "\033[37m"
    RESET = "\033[0m"


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


def diff_only_head(base, head, more_1char_args=None, log_level=0):
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
        log_level (int): How much info to show (-1 to hide output of
            diff command).

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
    return _diff_only_head(
        base,
        head,
        more_1char_args=more_1char_args,
        log_level=log_level,
    )


def validate_diff_args(more_1char_args):
    """Check the given arguments format for diff or fc
    and convert to a list if has spaces.

    Args:
        more_1char_args (Union[str,list[str],tuple[str]]): Arguments for
            the diff tool.

    Raises:
        TypeError: Not list, tuple, nor str.
        ValueError: is blank str
        ValueError: is just a '-' or '/'
        ValueError: starts with '/' when using diff, or '-' when not

    Returns:
        list(str): Arguments (usually only one, such as "-wbB" for diff,
            or for FC, "/B" for binary and "/W" to ignore whitespace).
            In other words, return the original more_1char_args or
            split it into a list.
    """
    diff_bin_name = DIFF_CMD_PARTS[0].lower()
    opener_for_1char = "-" if (diff_bin_name == "fc") else "/"
    # ^ even on Windows, diff would take "-" (fc takes "/" before options)

    if not isinstance(more_1char_args, (list, tuple)):
        if not isinstance(more_1char_args, str):
            raise TypeError("more_1char_args must be list, tuple, or str")
        more_1char_args = more_1char_args.strip()
        if len(more_1char_args) == 0:
            raise ValueError("more_1char_args for \"{}\" was empty str"
                             " but should be None or an args string"
                             " starting with '{}'"
                             "".format(diff_bin_name, opener_for_1char))
        elif len(more_1char_args) == 1:
            if more_1char_args in ("-", "/"):
                raise ValueError("more_1char_args was only '{}' with no args"
                                 "".format(more_1char_args))
        # Allow string too (split if has space, otherwise convert
        # to 1-long list still)
        # Split into tuple and recurse:
        return validate_diff_args(more_1char_args.strip().split())

    for arg in more_1char_args:
        if not arg.startswith(opener_for_1char):
            bin_msg = "diff"
            if diff_bin_name != "diff":
                bin_msg = (
                    "diff wasn't in your PATH so {} is being used, but it"
                    "".format(diff_bin_name)
                )
            raise ValueError(
                "{} only accepts options"
                " starting with '{}'"
                " (got \"{}\")".format(bin_msg, opener_for_1char,
                                       arg)
            )
    return more_1char_args  # It is a list now.


def _diff_only_head(base, head, rel=None, more_1char_args=None, depth=0,
                    log_level=0):
    """Compare two directories or files.

    For other documentation see diff_only_head.

    Args:
        rel (str, optional): Leave as None. This will be set
            automatically for recursion.
        depth (int, optional): Leave as 0. This will be set
            automatically for recursion.

    """
    diffs = []
    if not DIFF_CMD_PARTS:
        ok_commands = 'diff'
        if platform.system() == "Windows":
            ok_commands = ['fc', 'diff']
        raise FileNotFoundError("There is no {} in your PATH."
                                "".format(ok_commands))
    args_1char = None

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
            diffs += _diff_only_head(
                base,
                head,
                rel=sub_rel,
                more_1char_args=more_1char_args,
                depth=depth+1,
                log_level=log_level,
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


        head_is_binary = is_binary(head_path)

        if more_1char_args is None:
            if platform.system() == "Windows":
                if not head_is_binary:
                    args_1char = ["/W"]  # ignore whitespace
                else:
                    args_1char = ["/B"]  # binary comparison
            else:
                if not head_is_binary:
                    args_1char = ["-wbB"]
                    # -b: ignore changes in the amount of whitespace
                    # -w: ignore all white space (better for code since
                    #     "a=1" is same as "a == 1", otherwise tokenizing
                    #     the specific language would be necessary)
                    # -a: --text  treat all files as text and
                    #     --strip-trailing-cr  strip trailing carriage
                    #         return
                    #     [doesn't do enough if has extra blank line,
                    #     still says different, so use -B instead]
                    # -B, ignore changes where all lines are blank
                    # -E, --ignore-tab-expansion
                # else None (just use diff without any options)
        else:
            args_1char = validate_diff_args(more_1char_args)
        del more_1char_args

        # echo0("^ in base")
        cmd_parts = DIFF_CMD_PARTS.copy()
        # echo0("args_1char={}".format(args_1char))
        if args_1char:
            cmd_parts += args_1char
        cmd_parts += [base_path, head_path]
        # echo0("\n\n{}".format(shlex.join(cmd_parts)))
        child = subprocess.Popen(cmd_parts, stdout=subprocess.PIPE)
        streamdata = child.communicate()[0]
        if log_level >= 0:
            # ^ Only -1 should hide diff output itself.
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


def get_shallowest_files_sub(root, log_level=0, mask=None, name=None):
    """Get the shallowest folder relative to root that contains file(s).

    Args:
        root (str): The folder to check for files recursively.
            NOTE: "" or paths ending with "." will be converted to a
            real path (following symlinks if any).
        log_level (int, optional): 0 for only errors. 1 for info.
        mask (Union[str,list[str]], optional): Filename or list of
            filenames to find (None/0/""/False/"*"/[] will match any
            file). If a folder contains the files, the folder path
            relative to root will be returned.
        name (str, optional): What parent folder name to return, or None
            for any with files (see mask). Defaults to None.

    Returns:
        str: Get the relative dir that contains file(s) ("" for root,
            None if not found).
    """
    if (root == "") or root.endswith("."):
        root = os.path.realpath(root)
    return _get_shallowest_files_sub(
        root,
        log_level=log_level,
        mask=mask,
        name=name,
    )


def _get_shallowest_files_sub(root, rel=None, depth=0, log_level=0,
                              mask=None, name=None):
    """Get the shallowest folder relative to root that contains file(s).
    See get_shallowest_files_sub for other arguments.

    Args:
        rel (str, optional): Leave blank (set automatically during
            recursion).
        depth (int, optional): Leave as 0 (set automatically during
            recursion).

    Raises:
        ValueError: root is None
        ValueError: _description_

    Returns:
        str: Get the relative dir that contains file(s) ("" for root,
            None if not found).
    """
    if isinstance(mask, str):
        if mask == "*":
            mask = None
        mask = [mask]
    if root is None:
        raise ValueError("root is {}".format(root))
    if rel and rel.startswith(os.path.sep):
        raise ValueError(
            "rel cannot start with '{}'"
            " because that would override root (depth={})"
            "".format(os.path.sep, depth)
        )

    parent = os.path.join(root, rel) if rel else root
    _, parent_name = os.path.split(parent)
    # ^ Ok even if rel is used, since split name results in ('', name)
    for sub in os.listdir(parent):
        if name and (parent_name != name):
            # Match against the name if name is set by caller.
            continue
        sub_path = os.path.join(parent, sub)
        if os.path.isfile(sub_path):
            if (not mask) or (sub in mask):
                if rel is None:
                    rel = ""  # found in root, so rel is ""
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
            mask=mask,
            name=name,
        )

        if found_path is not None:
            return found_path
        continue

    return None


def find_mod(parent, name):
    mask = ["init.lua", "mod.conf", "depends.txt", "description.txt"]
    # return _find_sub_with_known_files(
    #     parent,
    #     name,
    #     mask=mask,
    # )
    return get_shallowest_files_sub(
        parent,
        mask=mask,
        name=name,
    )


def find_modpack(parent, name):
    mask = ["modpack.txt", "modpack.conf"]
    # return _find_sub_with_known_files(
    #     parent,
    #     name,
    #     mask=mask,
    # )
    return get_shallowest_files_sub(
        parent,
        mask=mask,
        name=name,
    )


def usage():
    echo0(__doc__)


def main():
    bases = (
        "/opt/minebest/assemble/bucket_game",
        # "/opt/minebest/mtkit/minetest/src",
    )
    head_parents = (
        os.path.join(REPO_DIR, "Bucket_Game-branches"),
        os.path.join(HOME, "metaprojects", "pull-requests", "OldCoder"),
        os.path.join(HOME, "metaprojects", "pull-requests",
                     "Bucket_Game-branches"),
    )
    for arg in sys.argv[1:]:
        if arg == "--skip-missing":
            skip_missing = True
        else:
            usage()
            echo0("Error: unknown argument {}".format(arg))
            return 1
    return check_if_head_files_applied(bases, head_parents,
                                       skip_missing=skip_missing)


def check_if_head_files_applied(bases, head_parents, skip_missing=False):
    """Check if head files are applied.

    Args:
        bases (list[str]): Directories where heads should have been
            applied.
        head_parents (list[str]): Folders containing various patches,
            where each sub of each parent is in the form of files to
            overlay onto base.

    Returns:
        int: 0 on success.
    """
    for base in bases:
        if not os.path.isdir(base):
            echo0('Warning: There is no base "{}".'.format(base))
            continue
        for head in head_parents:
            echo0("\n# {}".format(head))
            for head_sub in os.listdir(head):
                # Identify each head folder as an overlay to "patch" a base.
                head_sub_path = os.path.join(head, head_sub)
                # region skip non-patch subs
                if os.path.isfile(head_sub_path):
                    # echo0('Warning: Only folders, skipped "{}"'
                    #       ''.format(head_sub))
                    continue
                if "original" in head_sub:
                    # echo0('INFO: skipped original: "{}"'
                    #       ''.format(head_sub))
                    continue
                elif "-BASE" in head_sub:
                    # echo0('INFO: skipped BASE: "{}"'
                    #       ''.format(head_sub))
                    continue
                elif head_sub in ("1.Tasks", "1.old", "1.wontfix",
                                  "1.website"):
                    # echo0('INFO: skipped Tasks folder: "{}"'
                    #       ''.format(head_sub))
                    continue

                # endregion skip non-patch subs

                # region identify patch structure
                mod_rel = get_shallowest_files_sub(
                    head_sub_path,
                    mask=["init.lua", "mod.conf", "depends.txt",
                          "description.txt"],
                )
                modpack_rel = get_shallowest_files_sub(
                    head_sub_path,
                    mask=["modpack.txt", "modpack.conf"],
                )
                game_patch_root = None
                mod_patch_root = None
                modpack_patch_root = None

                if head_sub.endswith("_game"):
                    game_patch_root = head_sub_path
                elif os.path.isdir(os.path.join(head_sub_path, "mods")):
                    game_patch_root = head_sub_path
                    echo0('game_patch_root="{}"'.format(head_sub))
                elif (mod_rel is not None) and (modpack_rel is None):
                    mod_parent = os.path.dirname(os.path.join(head_sub_path,
                                                              mod_rel))
                    mod_parent_rel = mod_parent[len(head_sub_path)+1:]
                    # ^ +1 no os.path.sep
                    _, mod_parent_name = os.path.split(mod_parent)
                    if mod_parent_rel and (mod_parent_name not in ["mods"]):
                        echo0('Warning: No modpack.txt nor modpack.conf,'
                              ' so assuming modpack={} ("{}")'
                              ''.format(mod_parent_name, mod_parent))
                        modpack_patch_root = mod_parent

                if game_patch_root:
                    pass  # Already set above.
                elif modpack_patch_root:
                    pass  # Already set above.
                elif mod_rel is not None:
                    if mod_rel:
                        mod_patch_root = os.path.join(head_sub_path, mod_rel)
                    else:
                        # Must be "", so don't do join or will add os.path.sep
                        mod_patch_root = head_sub_path
                    _, got_mod_name = os.path.split(mod_patch_root)
                    echo0('mod_patch="{}" root="{}"'
                          ''.format(got_mod_name, mod_patch_root))
                else:
                    pass
                    # echo0('Warning: mod not identified in "{}"'
                    #       ''.format(head_sub))
                    # See output in "else" below instead.
                # endregion identify patch structure

                # region check whether base has it installed
                patch_root = None
                if game_patch_root is not None:
                    patch_root = game_patch_root
                    _, game_name = os.path.split(base)
                    base_sub_path = base
                    echo0("* Checking whether {} was applied to {} game"
                          "".format(head_sub, game_name))
                elif modpack_patch_root is not None:
                    patch_root = modpack_patch_root
                    _, modpack_name = os.path.split(modpack_patch_root)
                    modpack_rel = find_modpack(base, modpack_name)
                    if modpack_rel is None:
                        echo0("Error: {} was not found in {}"
                              "".format(modpack_name, base))
                        continue
                    if modpack_rel:
                        base_sub_path = os.path.join(base, modpack_rel)
                    else:
                        # Must be "", so avoid join to avoid adding os.path.sep
                        base_sub_path = base
                    echo0("* Checking whether {} was applied to"
                          " {} modpack in {} game"
                          "".format(head_sub, modpack_name, game_name))
                elif mod_patch_root is not None:
                    patch_root = mod_patch_root
                    _, mod_name = os.path.split(mod_patch_root)
                    mod_rel = find_mod(base, mod_name)
                    if mod_rel is None:
                        echo0("Error: {} was not found in {}"
                              "".format(mod_name, base))
                        continue
                    if modpack_rel:
                        base_sub_path = os.path.join(base, modpack_rel)
                    else:
                        # Must be "", so avoid join to avoid adding os.path.sep
                        base_sub_path = base
                    echo0("* Checking whether {} was applied to"
                          " {} mod in {} game"
                          "".format(head_sub, mod_name, game_name))
                else:
                    echo0('Warning: Skipping unknown patch structure: "{}"'
                          ''.format(head_sub))

                diffs = diff_only_head(base_sub_path, patch_root, log_level=-1)
                for diff in diffs:
                    missing = bool(diff.get("new"))
                    if missing:
                        if skip_missing:
                            continue
                        color = Fore.GREEN
                    else:
                        color = Fore.YELLOW
                    why = "MISSING" if missing else "differs"
                    # echo0("  * {}: {}".format(why, diff))
                    # if not missing:
                    if diff['rel'].startswith(os.path.sep):
                        raise NotImplementedError(
                            "rel cannot start with {}"
                            " or it will override base or head."
                            "".format(os.path.sep)
                        )
                    echo0("    "+shlex.join([
                        "meld",
                        os.path.join(base_sub_path, diff['rel']),
                        os.path.join(head_sub_path, diff['rel']),
                    ])+"{}  # {} in base (original) vs head (patch) {}".format(color, why, Fore.RESET))
                # endregion check whether base has it installed

    return 0


if __name__ == "__main__":
    sys.exit(main())
