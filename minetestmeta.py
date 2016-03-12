import os
from expertmm import *

class MinetestMetadata:

    config = None
    config_name = None
    config_path = None
    worldgen_mod_list = None


    def __init__(self):
        self.config_name = "minetestmeta.yml"
        self.config_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), self.config_name)
        self.config = {}
        self.config = get_dict_modified_by_conf_file(self.config, self.config_path, ":")
        is_config_changed = False
        if not os.path.isfile(self.config_path):
            is_config_changed = True
            print("Creating '"+self.config_path+"'")

        self.worldgen_mod_list = list()
        self.worldgen_mod_list.append("technic_worldgen")
        self.worldgen_mod_list.append("mg")  # this delays/prevents chunk generation and sometimes crashes in 0.4.13 release (tested on Windows 10)
        self.worldgen_mod_list.append("moreores")
        self.worldgen_mod_list.append("lapis")
        self.worldgen_mod_list.append("sea")
        self.worldgen_mod_list.append("moretrees")
        self.worldgen_mod_list.append("caverealms")
        #self.worldgen_mod_list.append("nature_classic")  # NOTE: plantlife_modpack has this and other stuff, but detecting this could help since it is unique to the modpack
        self.worldgen_mod_list.append("plantlife_modpack")  #ok if installed as modpack instead of putting individual mods in mods folder



mtmeta = MinetestMetadata()
