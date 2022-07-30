#!/usr/bin/env python3
import os
import shutil
import sys
actions = {"-- Up-to-date: ": "move", "-- Installing: ": "move"}
changes = {
    "/usr/local/./": "/usr/local/share/minetest/"
}


def main():
    count = 0
    command_count = 0
    in_path = "bad_mt5_make_install_output.txt"
    outs_path = os.path.dirname(os.path.realpath(__file__))
    out_path = os.path.join(outs_path, "install-fix-minetest5-share.sh")
    file_commands = []
    rmd_cmds = []
    mkdir_commands = []
    made_dirs = []
    mtg_mod_dirs = ["games//minetest_game/mods", "games/minetest_game/mods"]
    with open(in_path) as ins:
        with open(out_path, 'w') as outs:
            outs.write("#!/bin/sh\n")
            count += 1
            for line_orig in ins:
                line = line_orig.strip()
                action = None
                old_path = None
                for k, try_action in actions.items():
                    if line.startswith(k):
                        action = try_action
                        old_path = line[len(k):].strip()
                        break
                if action == "move":
                    found = None
                    for old, new in changes.items():
                        if old_path.startswith(old):
                            found = old
                            new_path = new + old_path[len(old):]
                            if not os.path.exists(old_path):
                                if not os.path.exists(new_path):
                                    # raise ValueError(
                                    #     "The program is not installed"
                                    #     " (missing '{}')".format(old_path)
                                    # )
                                    outs.write(
                                        '# WARNING: expected "{}" (there is'
                                        ' no destination "{}" either)'
                                        ''.format(old_path, new_path)
                                    )
                                else:
                                    outs.write(
                                        '# Already moved (no source "{}"'
                                        ' for destination "{}")'
                                        ''.format(old_path, new_path)
                                    )
                            else:
                                if os.path.isfile(old_path):
                                    parent = os.path.split(new_path)[0]
                                    if parent not in made_dirs:
                                        made_dirs.append(parent)
                                        cmd = 'mkdir -p "{}"'.format(
                                            parent.replace("//", "/")
                                        )
                                        mkdir_commands.append(cmd)
                                    # AFTER all directories BEFORE all files
                                    options = ""
                                    if os.path.isfile(new_path):
                                        options = "-f"
                                    if len(options) > 0:
                                        options = " " + options.strip()
                                    cmd = (
                                        'mv' + options
                                        + ' "{}" "{}"'.format(
                                            old_path.replace("//", "/"),
                                            new_path.replace("//", "/")
                                        )
                                    )
                                    # outs.write(cmd + "\n")
                                    # AFTER all directories
                                    file_commands.append(cmd)
                                else:
                                    # old_path == old_path.replace("//","/")
                                    # Manually fix:

                                    # rmdir: failed to remove '/usr/local/
                                    # ./games//minetest_game/mods':
                                    # Directory not empty

                                    # rmdir: failed to remove '/usr/local/
                                    # ./games//minetest_game':
                                    # Directory not empty

                                    # due to /usr/local/./games//
                                    # minetest_game/mods/game_commands:
                                    orphan_mods = ["game_commands"]
                                    removed_orphan_mods = []

                                    for mod_rel in orphan_mods:
                                        for mtg_rel in mtg_mod_dirs:
                                            f_rel = found + mtg_rel
                                            # such as ("/usr/local/./"
                                            # + "games//minetest_game/mods")
                                            if old_path.startswith(f_rel):
                                                # if mod_rel not in
                                                # removed_orphan_mods:
                                                try_path = (found + mtg_rel
                                                            + "/" + mod_rel)
                                                if os.path.isdir(try_path):
                                                    cmd = (
                                                        'rmdir "{}"'.format(
                                                            try_path
                                                        )
                                                    )
                                                    # queue for last stage:
                                                    if cmd not in rmd_cmds:
                                                        rmd_cmds.append(cmd)
                                                    # removed_orphan_mods.
                                                    # append(mod_rel)
                                                    break

                                    cmd = 'rmdir "{}"'.format(old_path)
                                    rmd_cmds.append(cmd)  # AFTER everything
                            break
                    if found is None:
                        outs.write("# WARNING: The destination path is"
                                   " unknown: ")
                        outs.write('# mv "{}" "{}"'.format(old_path,
                                                           old_path))
                else:
                    outs.write("# " + line + "\n")
                    count += 1
            for cmd in sorted(mkdir_commands, key=len):
                outs.write(cmd + "\n")
                count += 1
                command_count += 1
            for cmd in file_commands:
                outs.write(cmd + "\n")
                count += 1
                command_count += 1
            for cmd in sorted(rmd_cmds, key=len, reverse=True):
                outs.write(cmd + "\n")
                count += 1
                command_count += 1

    print('Added {} line(s) to "{}" (including {} command(s))'
          ''.format(count, out_path, command_count))

    return 0


if __name__ == "__main__":
    sys.exit(main())
