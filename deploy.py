#!/usr/bin/env python
import os
import sys
import shutil
from forwardfilesync import *
# import filever
from pyenliven import (
    echo0,
)
if sys.version_info.major >= 3:
    pass
else:
    input = raw_input


def rm_sub(bad_sub):
    bad_path = path_join_all(deploy_path, bad_sub)
    if os.path.isfile(bad_path):
        os.remove(bad_path)


def main():
    warnings = list()

    echo0("")
    echo0("This script is NOT YET IMPLEMENTED")


    # TODO: Scrape https://minetest.kitsunemimi.pw/builds/ (NOTE: stable is
    #   always "https://minetest.kitsunemimi.pw/builds/win64/"
    #   "minetest-0.4.15-win64.7z")


    echo0("This script patches minetest and minetest_game with ENLIVEN\n" +
          "(such as launcher and subgame) and creates a Windows installer.")

    script_dir_path = os.path.dirname(os.path.abspath(__file__))
    enliven_project_path = os.path.dirname(script_dir_path)

    profile_path = None
    if "HOME" in os.environ:
        profile_path = os.environ["HOME"]
    elif "USERPROFILE" in os.environ:
        profile_path = os.environ["USERPROFILE"]
    else:
        raise ValueError(
            "HOME and USERPROFILE aren't set. This should never happen."
        )
        '''
        try_path = "C:\\Users\\jgustafson"
        if not os.path.isdir(try_path):
            try_path = "C:\\Users\\Owner"

        echo0("WARNING: no HOME or USERPROFILE found, reverting to '" +
              try_path + "'")
        profile_path = try_path
        '''
    # TODO: Make a settings file for values in the next region.
    #   region user settings

    deploy_path = "C:\\Games\\ENLIVEN-deploy"
    '''
    try_path = "C:\\Games\\Minetest"
    if (not os.path.isdir(deploy_path)):
        if os.path.isdir(try_path):
            deploy_path = try_path
        # else make the default one further down
    '''
    # ^ The path must match the one in projects/setup-ENLIVEN-win64.iss
    installer_deploy_path = path_join_all([profile_path, "Nextcloud", "www",
                                          "expertmultimedia", "downloads"])
    installer_name = "install-ENLIVEN.exe"
    # endregion user settings

    installer_path = os.path.join(installer_deploy_path, installer_name)

    if not os.path.isdir(installer_deploy_path):
        echo0("#WARNING: does not exist:")
    print("installer_deploy_path: " + installer_deploy_path)

    # this is a waste--it just shows 0.0.0.0 though iss file has version
    # if os.path.isfile(installer_path):
    #     numbers=filever.get_version_number(installer_path)
    #     major,minor,subminor,revision = numbers
    #     print(".".join([str (i) for i in numbers]))

    if not os.path.isdir(deploy_path):
        if platform.system() != "Windows":
            raise RuntimeError(
                "A proper tmp deploy path for {} is not defined."
                "".format(platform.system())
            )
        os.makedirs(deploy_path)
    games_path = os.path.join(deploy_path, "games")
    minetest_game_path = os.path.join(games_path, "minetest_game")
    minetest_game_mods_path = os.path.join(minetest_game_path, "mods")
    if not os.path.isdir(minetest_game_path):
        echo0("This deploy script requires an unmodified build of minetest and\n" +
              " minetest_game. Please place an unmodified build of minetest in\n" +
              " " + deploy_path + " so that minetest_game is at: \n\n" +
              " " + minetest_game_path + "\n\n")
        return 1

    game_path = os.path.join(games_path, "ENLIVEN")

    # NOTE: remove this case, and instead: copy minetest_game, download ENLIVEN
    # automatically
    if not os.path.isdir(game_path):
        echo0("")
        echo0("ERROR: ENLIVEN must first be installed from web sources" +
              " using the provided 'install' script in the etc/change*" +
              " folder (run on linux then copy to a Windows machine" +
              " in " + game_path)
        # return 2
    else:
        print("game_path: " + game_path)
    mods_path = os.path.join(game_path, "mods")
    if not os.path.isdir(mods_path):
        os.makedirs(mods_path)
    mtg_list_path = os.path.join(game_path, "minetest_game-mod-list.txt")
    mtg_list_out = open(mtg_list_path, 'w')
    folder_path = minetest_game_mods_path
    if os.path.isdir(folder_path):
        for sub_name in os.listdir(folder_path):
            sub_path = os.path.join(folder_path, sub_name)
            if sub_name[:1] != "." and os.path.isdir(sub_path):
                mtg_list_out.write(sub_name + "\n")
    mtg_list_out.close()

    # TODO: uncomment this: update_tree(minetest_game_path, game_path)

    server_devel_minetest_conf_path = os.path.join(
        game_path,
        "minetest.conf.ENLIVEN-server"
    )
    server_minetest_conf_path = os.path.join(game_path, "minetest.conf")

    if not os.path.isfile(server_devel_minetest_conf_path):
        warnings.append(server_devel_minetest_conf_path + " was not found")
    else:
        shutil.copyfile(server_devel_minetest_conf_path,
                        server_minetest_conf_path)

    rm_sub(["CC-BY-SA 3.0 Unported (fallback license for ENLIVEN assets)"
            ".txt"])
    rm_sub(["MIT LICENSE (fallback license for ENLIVEN code).txt"])

    # NOTE: At this point, the following LICENSE and README files are
    #   minetest_game's and the following are intentionally looking in
    #   C:\games\ENLIVEN\games\ENLIVEN:
    # rm_sub(["games", "ENLIVEN", "LICENSE.txt"])
    # rm_sub(["games", "ENLIVEN", "README.txt"])

    echo0("")
    if len(warnings) > 0:
        echo0(str(len(warnings)) + " warning(s):")
        for warning in warnings:
            echo0(warning)
    else:
        echo0("0 warnings.")
    echo0()
    return 0


if __name__ == "__main__":
    sys.exit(main())
