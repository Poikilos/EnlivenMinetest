import os
from expertmm import *

#variables to eliminate from chunkymap-regen (and manage here instead):
#os_name
#self.config (use minetestinfo.get_val instead)
#config_name
#config_path
#profile_path

worldgen_mod_list = list()
worldgen_mod_list.append("caverealms")
worldgen_mod_list.append("ethereal")
worldgen_mod_list.append("lapis")
worldgen_mod_list.append("mines")
worldgen_mod_list.append("mg")  # this delays/prevents chunk generation and sometimes crashes in 0.4.13 release (tested on Windows 10)
worldgen_mod_list.append("moretrees")
worldgen_mod_list.append("moreores")
#worldgen_mod_list.append("nature_classic")  # NOTE: plantlife_modpack has this and other stuff, but detecting this could help since it is unique to the modpack
worldgen_mod_list.append("plantlife_modpack")  #ok if installed as modpack instead of putting individual mods in mods folder
worldgen_mod_list.append("pyramids")
worldgen_mod_list.append("railcorridors")
worldgen_mod_list.append("sea")
worldgen_mod_list.append("technic")
worldgen_mod_list.append("technic_worldgen")
worldgen_mod_list.append("tsm_mines")
worldgen_mod_list.append("tsm_pyramids")
worldgen_mod_list.append("tsm_railcorridors")

loaded_mod_list = list()

minetestinfo = ConfigManager(os.path.join(os.path.dirname(os.path.abspath(__file__)), "minetestmeta.yml"), ":")

os_name="linux"
if (os.path.sep!="/"):
    os_name="windows"
    print("Windows detected")

def init_minetestinfo():
    if not minetestinfo.contains("www_minetest_path"):
        default_www_minetest_path = "/var/www/html/minetest"
        if os_name=="windows":
            default_www_minetest_path = None
            prioritized_try_paths = list()
            prioritized_try_paths.append("C:\\wamp\\www")
            prioritized_try_paths.append("C:\\www")
            prioritized_try_paths.append("C:\\Program Files\\Apache Software Foundation\\Apache2.2\\htdocs")
            prioritized_try_paths.append("C:\\Inetpub\\Wwwroot")

            #prioritized_try_paths.append("C:\\Program Files\\Apache Software Foundation\\Apache2.2\\htdocs\\folder_test\\website")
            for try_path in prioritized_try_paths:
                try:
                    if os.path.isdir(try_path):
                        default_www_minetest_path = try_path
                        break
                except:
                    pass
            if default_www_minetest_path is None:
                print("WARNING: could not detect website directory automatically. You need WAMP or similar web server with php 5 or higher to use minetest website scripts. You can change www_minetest_path to your server's website root later by editing '"+minetestinfo._config_path+"'")
                default_www_minetest_path = os.path.dirname(os.path.abspath(__file__))

        minetestinfo.prepare_var("www_minetest_path", default_www_minetest_path, "your web server directory (or other folder where minetest website features and data should be placed)")

    profile_path = None
    if os_name=="windows":
        profile_path = os.environ['USERPROFILE']
    else:
        profile_path = os.environ['HOME']

    default_profile_minetest_path = os.path.join(profile_path,".minetest")
    if (os_name=="windows"):
        default_profile_minetest_path = "C:\\games\\Minetest"
    minetestinfo.prepare_var("profile_minetest_path", default_profile_minetest_path, "user minetest path containing worlds folder and debug.txt")
    if not os.path.isdir(minetestinfo.get_var("profile_minetest_path")):
        print("(WARNING: missing "+minetestinfo.get_var("profile_minetest_path")+", so please close and update profile_minetest_path in '"+minetestinfo._config_path+"' before next run)")
    print("")

    if not minetestinfo.contains("worlds_path"):
        minetestinfo._data["worlds_path"] = os.path.join(minetestinfo.get_var("profile_minetest_path"),"worlds")
        minetestinfo.save_yaml()

    default_shared_minetest_path = "/usr/share/games/minetest"
    try_path = "/usr/local/share/minetest"
    if os_name == "windows":
        default_shared_minetest_path = "C:\\Games\\Minetest"
    elif os.path.isdir(try_path):
        default_shared_minetest_path = try_path

    while True:
        minetestinfo.prepare_var("shared_minetest_path", default_shared_minetest_path, "path containing Minetest's games folder")
        games_path = os.path.join(minetestinfo.get_var("shared_minetest_path"), "games")
        if not os.path.isdir(games_path):
            answer=raw_input("WARNING: '"+minetestinfo.get_var("shared_minetest_path")+"' does not contain a games folder. If you use this shared_minetest_path, some features may not work correctly (such as adding worldgen mod labels to chunks, and future programs that may use this metadata to install minetest games). Are you sure you want to use y/n [blank for 'n' (no)]? ")
            if answer.lower()=="y" or answer.lower()=="yes":
                print("You can change the value of shared_minetest_path later by editing '"+minetestinfo._config_path+"'.")
                print("")
                break
            else:
                minetestinfo.remove_var("shared_minetest_path")
        else:
            break
    load_world_and_mod_data()


def load_world_and_mod_data():
    #if games_path =
    global loaded_mod_list
    while len(loaded_mod_list) > 0 : loaded_mod_list.pop()  # instead of remaking, pop to ensure global is changed
    is_world_changed = False
    auto_chosen_world = False
    is_missing_world = False

    default_world_path = None
    if minetestinfo.contains("primary_world_path"):
        if not os.path.isdir(minetestinfo.get_var("primary_world_path")):
            is_missing_world = True
            print("primary_world_path ERROR: '"+minetestinfo.get_var("primary_world_path")+"' is not a folder.")


    if (not minetestinfo.contains("primary_world_path")) or is_missing_world:
        print ("LOOKING FOR WORLDS IN " + minetestinfo.get_var("worlds_path"))
        for base_path, dirnames, filenames in os.walk(minetestinfo.get_var("worlds_path")):
            #for j in range(0,len(dirnames)):
            #    i = len(dirnames) - 0 - 1
            #    if dirnames[i][0] == ".":
            #        print ("  SKIPPING "+dirnames[i])
            #        dirnames.remove_at(i)
            world_count = 0
            for subdirname in dirnames:
                print ("  EXAMINING "+subdirname)
                if subdirname[0]!=".":
                    world_count += 1
            index = 0
            world_number = 0
            for subdirname in dirnames:
                print ("  EXAMINING "+subdirname)
                if subdirname[0]!=".":
                    #if (index == len(dirnames)-1):  # skip first one because the one on my computer is big
                    if (subdirname!="world") or (world_number==(world_count-1)):
                        default_world_path = os.path.join(base_path, subdirname) #  os.path.join(minetestinfo.get_var("worlds_path"), "try7amber")
                        auto_chosen_world = True
                        break
                    world_number += 1
                index += 1
            if auto_chosen_world:
                break

        if is_missing_world:
            print("MISSING WORLD '"+minetestinfo.get_var("primary_world_path")+"'")
            if default_world_path is not None:
                print("(so a default was picked below that you can change)")
            else:
                print("(and no world could be found in worlds_path '"+minetestinfo.get_var("worlds_path")+"')")

        default_message = ""
        if default_world_path is not None:
            default_message = " (or world name if above; blank for ["+default_world_path+"])"
        input_string = raw_input("World path"+default_message+": ")
        if (len(input_string)>0):
            try_path = os.path.join(minetestinfo.get_var("worlds_path"), input_string)
            this_primary_world_path = input_string
            if (not os.path.isdir(this_primary_world_path)) and os.path.isdir(try_path):
                this_primary_world_path = try_path
            minetestinfo._data["primary_world_path"] = this_primary_world_path
            auto_chosen_world = False
        minetestinfo.save_yaml()

    if get_world_var("gameid") != minetestinfo.get_var("game_path"):
        is_world_changed = True

    if minetestinfo.contains("game_path") or is_world_changed:
        if minetestinfo.contains("game_path"):
            default_game_name = minetestinfo.get_var("game_path")
        if default_game_name is None:
            default_game_name = get_world_var("gameid")
        if default_game_name is not None:
            print("gameid "+default_game_name+" detected in world.")

        games_path = os.path.join(minetestinfo.get_var("shared_minetest_path"), "games")
        game_blacklist = list()  # is only used if there is no game defined in world
        game_blacklist.append("minetest_game")
        games_list = list()
        if default_game_name is None:
            if os.path.isdir(games_path):
                folder_path = games_path
                sub_names = os.listdir(folder_path)
                real_count = 0
                for sub_name in sub_names:
                    if (sub_name[:1]!="."):
                        real_count += 1
                real_index = 0
                for sub_name in sub_names:
                    sub_path = os.path.join(folder_path,sub_name)
                    if os.path.isdir(sub_path):
                        if (sub_name[:1]!="."):
                            if (sub_name != "minetest_game") or (real_index>=real_count-1):
                                if default_game_name is None:
                                    default_game_name = sub_name
                                games_list.append(sub_name)
                    real_index += 1
        if default_game_name is not None:
            path_msg = ""
            if len(games_list)>0:
                path_msg = " (or game name listed above)"
                for try_game_name in games_list:
                    print("  "+try_game_name)
            minetestinfo.prepare_var("game_path",os.path.join(games_path,default_game_name),"game (your subgame) path"+path_msg)

            if (not os.path.isdir(minetestinfo.get_var("game_path"))):
                try_path = os.path.join(games_path,minetestinfo.get_var("game_path"))
                if os.path.isdir(try_path):
                    minetestinfo.set_var("game_path",try_path)

        mods_path = None
        if minetestinfo.contains("game_path") and os.path.isdir(minetestinfo.get_var("game_path")):
            mods_path = os.path.join(minetestinfo.get_var("game_path"), "mods")
            folder_path = mods_path
            for sub_name in os.listdir(folder_path):
                sub_path = os.path.join(folder_path,sub_name)
                if os.path.isdir(sub_path):
                    if (sub_name[:1]!="."):
                        if get_world_var("load_mod_"+sub_name) == True:
                            loaded_mod_list.append(sub_name)
        else:
            print("Could not find game folder '"+minetestinfo.get_var("game_path")+"'. Please fix game_path in '"+minetestinfo._config_path+"' to point to your subgame, so that game and mod management features will work.")
        print("Mod list for current game: "+','.join(loaded_mod_list))
        #mods_path
        #mod_path = os.path.join(mods_path, mod_name)
        #if os.path.isdir(mod_path):

        #if default_game is None:
        #    game_names = os.listdir
world_mt_mapvars = None
world_mt_mapvars_world_path = None
def get_world_var(name):
    result = None
    global world_mt_mapvars_world_path
    world_path = minetestinfo.get_var("world_path")

    #world_mt_mapvars = None
    global world_mt_mapvars
    if world_mt_mapvars is None or (world_path != world_mt_mapvars_world_path):
        world_mt_mapvars_world_path = world_path
        if world_path is not None:
            world_mt_mapvars = get_dict_from_conf_file(os.path.join(world_path, "world.mt"),"=")
    if (world_mt_mapvars is not None) and name in world_mt_mapvars:
        result = world_mt_mapvars[name]
    return result

init_minetestinfo()
