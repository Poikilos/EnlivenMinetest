#!/usr/bin/env python2
import os
import subprocess
import traceback
import argparse
import time
import sys
import timeit
from timeit import default_timer as best_timer
#file modified time etc:
import time
#copyfile etc:
import shutil
import math

from PIL import Image, ImageDraw, ImageFont, ImageColor

#best_timer = timeit.default_timer
#if sys.platform == "win32":
    # on Windows, the best timer is time.clock()
#    best_timer = time.clock
#else:
    # on most other platforms, the best timer is time.time()
#    best_timer = time.time
# REQUIRES: see README.md
# The way to do a full render is deleting all files from the folder www_minetest_path/chunkymapdata such as /var/www/html/minetest/chunkymapdata (or chunkymap in current directory on Windows)

#minetestmapper-numpy.py calculates the region as follows:
#(XMIN','XMAX','ZMIN','ZMAX'), default = (-2000,2000,-2000,2000)
#sector_xmin,sector_xmax,sector_zmin,sector_zmax = numpy.array(args.region)/16
#sector_ymin = args.minheight/16
#sector_ymax = args.maxheight/16
#region server-specific options

#as per http://interactivepython.org/runestone/static/pythonds/BasicDS/ImplementingaQueueinPython.html
#class SimpleQueue:
    #def __init__(self):
        #self.items = []

    #def isEmpty(self):
        #return self.items == []

    #def enqueue(self, item):
        #self.items.insert(0,item)

    #def dequeue(self):
        #return self.items.pop()

    #def size(self):
        #return len(self.items)


class InstalledFile:
    source_dir_path = None
    dest_dir_path = None
    file_name = None

    def __init__(self, file_name, source_dir_path, dest_dir_path):
        self.file_name=file_name
        self.source_dir_path=source_dir_path
        self.dest_dir_path=dest_dir_path

        
def get_dict_deepcopy(old_dict):
    new_dict = None
    if type(old_dict) is dict:
        new_dict = {}
        for this_key in old_dict.iterkeys():
            new_dict[this_key] = old_dict[this_key]
    return new_dict

def is_dict_subset(new_dict, old_dict, verbose_messages_enable, verbose_dest_description="unknown file"):
    is_changed = False
    if old_dict is not None:
        if new_dict is not None:
            old_dict_keys = self.old_dict.keys()
            for this_key in self.new_dict.iterkeys():
                if (this_key not in old_dict_keys):
                    is_changed = True
                    if verbose_messages_enable:
                        print("SAVING '"+verbose_dest_description+"' since "+str(this_key)+" not in saved version.")
                    break
                elif new_dict[this_key] != old_dict[this_key]:
                    is_changed = True
                    if verbose_messages_enable:
                        print("SAVING '"+verbose_dest_description+"' since "+str(this_key)+" not same as saved version.")
                    break
        #else new_dict is None so no change detected (no new information)
    else:
        if new_dict is not None:
            is_changed = True
    return is_changed

def ivec2_equals(pos1, pos2):
    return (int(pos1[0])==int(pos2[0])) and (int(pos1[1])==int(pos2[1]))

def get_dict_from_conf_file(path,assignment_operator="="):
    results = None
    results = get_dict_modified_by_conf_file(results, path, assignment_operator)
    return results

def RepresentsInt(s):
    try:
        int(s)
        return True
    except ValueError:
        return False

def RepresentsFloat(s):
    try:
        float(s)
        return True
    except ValueError:
        return False

def view_traceback():
    ex_type, ex, tb = sys.exc_info()
    traceback.print_tb(tb)
    del tb

def print_file(path, min_indent=""):
    line_count = 0
    try:
        if path is not None:
            if os.path.isfile(path):

                if min_indent is None:
                    min_indent = ""
                ins = open(path, 'r')
                line = True
                while line:
                    line = ins.readline()
                    line_count += 1
                    if line:
                        print(min_indent+line)
                ins.close()
                #if line_count==0:
                    #print(min_indent+"print_file WARNING: "+str(line_count)+" line(s) in '"+path+"'")
                #else:
                    #print(min_indent+"# "+str(line_count)+" line(s) in '"+path+"'")
            else:
                print (min_indent+"print_file: file does not exist")
        else:
            print (min_indent+"print_file: path is None")
    except:
        print(min_indent+"print_file: could not finish")
        try:
            ins.close()
        except:
            pass
    return line_count

def get_dict_modified_by_conf_file(this_dict, path,assignment_operator="="):
    results = this_dict
    #print ("Checking "+str(path)+" for settings...")
    if (results is None) or (type(results) is not dict):
        results = {}
    if os.path.isfile(path):
        ins = open(path, 'r')
        line = True
        while line:
            line = ins.readline()
            if line and len(line)>0:
                line_strip=line.strip()
                if len(line_strip)>0 and not line_strip[0]=="#":  # if not comment
                    if not line_strip[0]=="-":  # ignore yaml arrays
                        ao_index = line_strip.find(assignment_operator)
                        if ao_index>=1:  # intentionally skip zero-length variable names
                            if ao_index<len(line_strip)-1:  # skip yaml implicit nulls or yaml objects
                                result_name = line_strip[:ao_index].strip()
                                result_value = line_strip[ao_index+1:].strip()
                                result_lower = result_value.lower()
                                if result_value=="None" or result_value=="null" or result_value=="~" or result_value=="NULL":
                                    result_value = None
                                elif result_lower=="true":
                                    result_value = True
                                elif result_lower=="false":
                                    result_value = False
                                elif RepresentsInt(result_value):
                                    result_value = int(result_value)
                                elif RepresentsFloat(result_value):
                                    result_value = float(result_value)
                                #print ("   CHECKING... "+result_name+":"+result_value)
                                results[result_name]=result_value
        ins.close()
    return results

def save_conf_from_dict(path, this_dict, assignment_operator="=", save_nulls_enable=True):
    try:
        outs = open(path, 'w')
        for this_key in this_dict.keys():
            if save_nulls_enable or (this_dict[this_key] is not None):
                if this_dict[this_key] is None:
                    outs.write(this_key+assignment_operator+"null\n")
                else:
                    outs.write(this_key+assignment_operator+str(this_dict[this_key])+"\n")
        outs.close()
    except:
        print("Could not finish saving chunk metadata to '"+str(path)+"': "+str(traceback.format_exc()))
        try:
            outs.close()
        except:
            pass

def get_tuple_from_notation(line, debug_src_name="<unknown object>"):
    result = None
    if line is not None:
        # mark chunk
        tuple_noparen_pos_string = line.strip("() \n\r")
        pos_strings = tuple_noparen_pos_string.split(",")
        if len(pos_strings) == 3:
            try:
                player_x = float(pos_strings[0])
                player_y = float(pos_strings[1])
                player_z = float(pos_strings[2])
            except:
                player_x = int(pos_strings[0])
                player_y = int(pos_strings[1])
                player_z = int(pos_strings[2])
            result = player_x, player_y, player_z
        else:
            print("'"+debug_src_name+"' has bad position data--should be 3-length (x,y,z) in position value: "+str(pos_strings))
    return result

def is_same_fvec3(list_a, list_b):
    result = False
    if list_a is not None and list_b is not None:
        if len(list_a)>=3 and len(list_b)>=3:
            result = (float(list_a[0]) == float(list_b[0])) and (float(list_a[1]) == float(list_b[1])) and (float(list_a[2]) == float(list_b[2]))
    return False


class MTDecaChunk:

    metadata = None
    last_changed_utc_second = None

    def __init__(self):
        self.metadata = {}
        self.metadata["last_saved_utc_second"] = None
        self.metadata["luid_list"] = None  # what chunks this decachunk contains (as saved to 160px image)

    def load_yaml(self, yml_path):
        self.metadata = get_dict_modified_by_conf_file(self.metadata,yml_path,":")

    def save_yaml(self, yml_path):
        save_conf_from_dict(yml_path, self.metadata, assignment_operator=":", save_nulls_enable=False)

class MTChunk:
    #x = None
    #z = None
    metadata = None
    is_fresh = None
    #luid = None

    def __init__(self):
        # NOTE: variables that need to be saved (and only they) should be stored in dict
        self.metadata = {}
        self.is_fresh = False

        self.metadata["is_empty"] = False  # formerly is_marked_empty
        self.metadata["is_marked"] = False
        self.metadata["width"] = None
        self.metadata["height"] = None
        self.metadata["image_w"] = None
        self.metadata["image_h"] = None
        self.metadata["image_left"] = None
        self.metadata["image_top"] = None
        self.metadata["image_right"] = None
        self.metadata["image_bottom"] = None
        self.metadata["is_traversed"] = False
        self.metadata["tags"] = None

    def load_yaml(self, yml_path):
        self.metadata = get_dict_modified_by_conf_file(self.metadata,yml_path,":")

    def save_yaml(self, yml_path):
        save_conf_from_dict(yml_path, self.metadata, assignment_operator=":", save_nulls_enable=False)

    #requires output such as from minetestmapper-numpy.py
    #returns whether save is needed (whether metadata was changed)
    def set_from_genresult(self, this_genresult_path):
        #this_genresult_path = mtchunks.get_chunk_genresult_path(chunk_luid)
        is_changed = False
        old_meta = get_dict_deepcopy(self.metadata)
        if os.path.isfile(this_genresult_path):
            #may have data such as:
            #Result image (w=16 h=16) will be written to chunk_x0z0.png
            #Unknown node names: meze:meze default:stone_with_iron air default:dirt_with_snow default:stone_with_copper default:snow
            #Unknown node ids: 0x0 0x1 0x2 0x3 0x4 0x5 0x6 0x7
            #Drawing image
            #Saving to: chunk_x0z0.png
            #('PNG Region: ', [0, 64, 0, 64])
            #('Pixels PerNode: ', 1)
            #('border: ', 0)
            self.metadata["is_marked"] = True
            ins = open(this_genresult_path, 'r')
            line = True
            while line:
                line = ins.readline()
                if line:
                    line_strip = line.strip()
                    try:
                        if ("does not exist" in line_strip):  # official minetestmapper.py says "World does not exist" but expertmm fork and minetestmapper-numpy.py say "data does not exist"
                            self.metadata["is_empty"] = True
                            break
                        elif "Result image" in line_strip:
                            oparen_index = line_strip.find("(")
                            if (oparen_index>-1):
                                cparen_index = line_strip.find(")", oparen_index+1)
                                if (cparen_index>-1):
                                    operations_string = line_strip[oparen_index+1:cparen_index]
                                    operation_list = operations_string.split(" ")
                                    #if len(operation_list)==2:
                                    for operation_string in operation_list:
                                        if "=" in operation_string:
                                            chunks = operation_string.split("=")
                                            if len(chunks)==2:
                                                if chunks[0].strip()=="w":
                                                    try:
                                                        self.metadata["image_w"]=int(chunks[1].strip())
                                                    except:
                                                        print("Bad value for image w:"+str(chunks[1]))
                                                elif chunks[0].strip()=="h":
                                                    try:
                                                        self.metadata["image_h"]=int(chunks[1].strip())
                                                    except:
                                                        print("Bad value for image h:"+str(chunks[1]))
                                                else:
                                                    print("Bad name for image variable so ignoring variable named '"+str(chunks[0])+"'")
                                            else:
                                                print("Bad assignment (not 2 sides) so ignoring command '"+operation_string+"'")
                                        else:
                                            print("Bad assignment (operator) so ignoring command '"+operation_string+"'")
                                    #else:
                                    #    print("Bad assignment count so ignoring operations string '"+operations_string+"'")
                        elif "PNG Region" in line_strip:
                            obracket_index = line_strip.find("[")
                            if obracket_index>-1:
                                cbracket_index = line_strip.find("]", obracket_index+1)
                                if cbracket_index>-1:
                                    rect_values_string = line_strip[obracket_index+1:cbracket_index]
                                    rect_values_list = rect_values_string.split(",")
                                    if len(rect_values_list)==4:
                                        #pngregion=[pngminx, pngmaxx, pngminz, pngmaxz] #from minetestmapper-numpy.py
                                        self.metadata["image_left"]=int(rect_values_list[0].strip())
                                        self.metadata["image_right"]=int(rect_values_list[1].strip())
                                        self.metadata["image_top"]=int(rect_values_list[2].strip())
                                        self.metadata["image_bottom"]=int(rect_values_list[3].strip())
                                    else:
                                        print("Bad map rect, so ignoring: "+rect_values_string)
                        elif (len(line_strip)>5) and (line_strip[:5]=="xmin:"):
                            self.metadata["image_left"] = int(line_strip[5:].strip())
                        elif (len(line_strip)>5) and (line_strip[:5]=="xmax:"):
                            self.metadata["image_right"] = int(line_strip[5:].strip())
                        elif (len(line_strip)>5) and (line_strip[:5]=="zmin:"):
                            #(zmin is bottom since cartesian)
                            self.metadata["image_bottom"] = int(line_strip[5:].strip())
                        elif (len(line_strip)>5) and (line_strip[:5]=="zmax:"):
                            #(zmax is top since cartesian)
                            self.metadata["image_top"] = int(line_strip[5:].strip())
                    except:
                        print("#failed to parse line:"+str(line_strip))
            ins.close()
        is_changed = is_dict_subset(self.metadata, old_meta, False)
        return is_changed

class MTChunks:
    chunkymap_data_path = None
    chunkymapdata_worlds_path = None
    is_save_output_ok = None
    minetestmapper_fast_sqlite_path = None
    minetestmapper_custom_path = None
    minetestmapper_py_path = None
    colors_path = None
    python_exe_path = None
    chunks = None
    decachunks = None
    total_newly_rendered = None

    #region values for subprocess arguments:
    pixelspernode = 1
    refresh_map_enable = None
    refresh_players_enable = None
    refresh_map_seconds = None
    refresh_players_seconds = None
    last_players_refresh_second = None
    last_map_refresh_second = None
    #endregion values for subprocess arguments:

    loop_enable = None
    verbose_enable = None

    run_count = None
    todo_positions = None  # list of tuples (locations) to render next (for fake recursion)
    todo_index = None
    yaml_name = None
    world_yaml_path = None
    preload_all_enable = None
    chunk_yaml_name_opener_string = None
    chunk_yaml_name_dotext_string = None
    mapvars = None
    saved_mapvars = None
    rendered_count = None
    backend_string = None
    #region_separators = None
    is_backend_detected = None
    chunkymap_players_name = None
    chunkymap_players_path = None
    config = None
    config_name = None
    config_path = None
    data_16px_path = None
    data_160px_path = None
    FLAG_EMPTY_HEXCOLOR = "#010000"
    world_name = None
    chunkymap_thisworld_data_path = None
    genresult_name_opener_string = "chunk_"
    genresult_name_closer_string = "_mapper_result.txt"

    def __init__(self):  #formerly checkpaths() in global scope
        self.decachunks = {}
        self.total_newly_rendered = 0
        os_name="linux"
        if (os.path.sep!="/"):
            os_name="windows"
            print("Windows detected")
        self.is_backend_detected = False
        self.mapvars = {}
        self.config = {}
        self.config_name = "chunkymap.yml"
        self.config_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), self.config_name)
        self.config = get_dict_modified_by_conf_file(self.config, self.config_path, ":")
        is_config_changed = False
        if not os.path.isfile(self.config_path):
            is_config_changed = True
            print("Creating '"+self.config_path+"'")
        #if self.config is None:
        self.mapvars["total_generated_count"] = 0
        self.rendered_count = 0
        self.preload_all_enable = True
        self.todo_index = -1
        self.todo_positions = list()
        self.run_count = 0
        self.verbose_enable = True
        self.loop_enable = True
        self.refresh_map_enable = True
        self.refresh_players_enable = True
        self.chunks = {}
        if "www_minetest_path" not in self.config.keys():
            self.config["www_minetest_path"] = "/var/www/html/minetest"
            if os_name=="windows":
                self.config["www_minetest_path"] = None
                prioritized_try_paths = list()
                prioritized_try_paths.append("C:\\wamp\\www")
                prioritized_try_paths.append("C:\\www")
                prioritized_try_paths.append("C:\\Program Files\\Apache Software Foundation\\Apache2.2\\htdocs")

                #prioritized_try_paths.append("C:\\Program Files\\Apache Software Foundation\\Apache2.2\\htdocs\\folder_test\\website")
                for try_path in prioritized_try_paths:
                    try:
                        if os.path.isdir(try_path):
                            self.config["www_minetest_path"] = try_path
                            break
                    except:
                        pass
                if self.config["www_minetest_path"] is None:
                    self.config["www_minetest_path"] = os.path.dirname(os.path.abspath(__file__))
            input_string = raw_input("Minetest website (blank for ["+self.config["www_minetest_path"]+"]): ")
            if (len(input_string)>0):
                self.config["www_minetest_path"] = input_string
            is_config_changed = True
            #print("Set www_minetest_path to '"+self.config["www_minetest_path"]+"'")
        #else:
        print("Using www_minetest_path '"+self.config["www_minetest_path"]+"'")
        print("")

        self.refresh_map_seconds = 30 #does one chunk at a time so as not to interrupt player updates too often
        self.refresh_players_seconds = 5
        self.chunk_yaml_name_opener_string = "chunk_"
        self.chunk_yaml_name_dotext_string = ".yml"
        #self.region_separators = [" "," "," "]

        input_string = ""


        profile_path = None
        if os_name=="windows":
            profile_path = os.environ['USERPROFILE']
        else:
            profile_path = os.environ['HOME']

        if "profile_minetest_path" not in self.config.keys():
            self.config["profile_minetest_path"] = os.path.join(profile_path,".minetest")
            if (os_name=="windows"):
                self.config["profile_minetest_path"] = "C:\\games\\Minetest"
            input_string = raw_input("user minetest path containing worlds folder (blank for ["+self.config["profile_minetest_path"]+"]): ")
            if (len(input_string)>0):
                self.config["profile_minetest_path"] = input_string
            is_config_changed = True
        print("Using profile_minetest_path '"+self.config["profile_minetest_path"]+"'")
        if not os.path.isdir(self.config["profile_minetest_path"]):
            print("(WARNING: missing, so please close and update profile_minetest_path in '"+self.config_path+"' before next run)")
        print("")
        if "worlds_path" not in self.config.keys():
            self.config["worlds_path"] = os.path.join(self.config["profile_minetest_path"],"worlds")
            is_config_changed = True

        auto_chosen_world = False
        is_missing_world = False
        if "world_path" in self.config.keys():
            if not os.path.isdir(self.config["world_path"]):
                is_missing_world = True
        if ("world_path" not in self.config.keys()) or is_missing_world:
            print ("LOOKING FOR WORLDS IN " + self.config["worlds_path"])
            for base_path, dirnames, filenames in os.walk(self.config["worlds_path"]):
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
                            self.config["world_path"] = os.path.join(base_path, subdirname) #  os.path.join(self.config["worlds_path"], "try7amber")
                            auto_chosen_world = True
                            break
                        world_number += 1
                    index += 1
                if auto_chosen_world:
                    is_config_changed = True
                    break
            if is_missing_world:
                print("MISSING WORLD '"+self.config["world_path"]+"'")
                if auto_chosen_world:
                    print("(so a default was picked below that you can change)")
                else:
                    print("(and no world could be found in worlds_path '"+self.config["worlds_path"]+"')")

            input_string = raw_input("World path (or world name if above; blank for ["+self.config["world_path"]+"]): ")
            if (len(input_string)>0):

                try_path = os.path.join(self.config["worlds_path"], input_string)
                this_world_path = input_string
                if (not os.path.isdir(this_world_path)) and os.path.isdir(try_path):
                    this_world_path = try_path
                self.config["world_path"] = this_world_path
                auto_chosen_world = False
            is_config_changed = True
        print ("Using world_path '"+self.config["world_path"]+"'")
        if not os.path.isdir(self.config["world_path"]):
            print("(ERROR: missing, so please close immediately and update world_path in '"+self.config_path+"' before next run)")
        print("")

        self.python_exe_path = "python"
        if os_name=="windows":
            try:
                alt_path = "C:\\python27\python.exe"
                if os.path.isfile(alt_path):
                    self.python_exe_path = alt_path
                #else may be in path--assume installer worked
            except:
                pass  # do nothing


        worldmt_path = os.path.join(self.config["world_path"], "world.mt")
        self.backend_string="sqlite3"
        if (os.path.isfile(worldmt_path)):
            ins = open(worldmt_path, 'r')
            line = True
            while line:
                line = ins.readline()
                if line:
                    line_strip = line.strip()
                    if len(line_strip)>0 and line_strip[0]!="#":
                        if line_strip[:7]=="backend":
                            ao_index = line_strip.find("=")
                            if ao_index>-1:
                                self.backend_string = line_strip[ao_index+1:].strip()
                                self.is_backend_detected = True
                                break
            ins.close()

        else:
            print("ERROR: failed to read '"+worldmt_path+"'")
        self.is_save_output_ok = False   # Keeping output after analyzing it is no longer necessary since results are saved to YAML, but keeping output provides debug info since is the output of minetestmapper-numpy.py
        if self.is_backend_detected:
            print("Detected backend '"+self.backend_string+"' from '"+worldmt_path+"'")
        else:
            print("WARNING: Database backend cannot be detected (unable to ensure image generator script will render map)")

        self.minetestmapper_fast_sqlite_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "minetestmapper-numpy.py")

        self.minetestmapper_custom_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "minetestmapper-expertmm.py")
        self.minetestmapper_py_path = self.minetestmapper_fast_sqlite_path
        if (self.backend_string!="sqlite3"):
            self.minetestmapper_py_path = self.minetestmapper_custom_path
        print("Chose image generator script: "+self.minetestmapper_py_path)
        if not os.path.isfile(self.minetestmapper_py_path):
            print("ERROR: script does not exist, so exiting "+__file__+".")
            sys.exit()
        self.colors_path = os.path.join(os.path.dirname(os.path.abspath(self.minetestmapper_py_path)), "colors.txt")
        if not os.path.isfile(self.colors_path):
            print("ERROR: missing '"+self.colors_path+"', so exiting "+__file__+".")
            sys.exit()

        self.chunkymap_data_path=os.path.join(self.config["www_minetest_path"],"chunkymapdata")
        self.chunkymapdata_worlds_path=os.path.join(self.chunkymap_data_path, "worlds")
        print("Using chunkymap_data_path '"+self.chunkymap_data_path+"'")
        #if not os.path.isdir(self.chunkymap_data_path):
        #    os.mkdir(self.chunkymap_data_path)
        htaccess_path = os.path.join(self.chunkymap_data_path,".htaccess")
        if not os.path.isdir(self.chunkymap_data_path):
            os.makedirs(self.chunkymap_data_path)
            print("Created '"+self.chunkymap_data_path+"'")
        if not os.path.isfile(htaccess_path):
            self.deny_http_access(self.chunkymap_data_path)
            print("  (created .htaccess)")

        htaccess_path = os.path.join(self.chunkymapdata_worlds_path,".htaccess")
        if not os.path.isdir(self.chunkymapdata_worlds_path):
            os.makedirs(self.chunkymapdata_worlds_path)
            print("Created '"+self.chunkymapdata_worlds_path+"'")
        if not os.path.isfile(htaccess_path):
            self.deny_http_access(self.chunkymapdata_worlds_path)
            print("  (created .htaccess)")



        self.world_name = os.path.basename(self.config["world_path"])
        self.chunkymap_thisworld_data_path = os.path.join(self.chunkymapdata_worlds_path, self.world_name)
        if not os.path.isdir(self.chunkymap_thisworld_data_path):
            os.makedirs(self.chunkymap_thisworld_data_path)
            print("Created '"+self.chunkymap_thisworld_data_path+"'")
        if not os.path.isfile(htaccess_path):
            self.deny_http_access(self.chunkymap_thisworld_data_path)
            print("  (created .htaccess)")

        self.data_16px_path = os.path.join(self.chunkymap_thisworld_data_path, "16px")
        if not os.path.isdir(self.data_16px_path):
            os.makedirs(self.data_16px_path)
            print("Created '"+self.data_16px_path+"'")
        if not os.path.isfile(htaccess_path):
            self.deny_http_access(self.data_16px_path)
            print("  (created .htaccess)")

        self.data_160px_path = os.path.join(self.chunkymap_thisworld_data_path, "160px")
        if not os.path.isdir(self.data_160px_path):
            os.makedirs(self.data_160px_path)
            print("Created '"+self.data_160px_path+"'")
        if not os.path.isfile(htaccess_path):
            self.deny_http_access(self.data_160px_path)
            print("  (created .htaccess)")

        #TODO: deny recursively under these folders? doesn't seem that important for security so maybe not (no player info is there)


        self.install_default_world_data()

        self.chunkymap_players_name = "players"
        self.chunkymap_players_path = os.path.join(self.chunkymap_thisworld_data_path, self.chunkymap_players_name)
        htaccess_path = os.path.join(self.chunkymap_players_path,".htaccess")
        if not os.path.isdir(self.chunkymap_players_path):
            os.makedirs(self.chunkymap_players_path)
        if not os.path.isfile(htaccess_path):
            self.deny_http_access(self.chunkymap_players_path)


        self.yaml_name = "generated.yml"
        self.world_yaml_path = os.path.join(self.chunkymap_thisworld_data_path, self.yaml_name)

        self.mapvars["chunkx_min"] = 0
        self.mapvars["chunkz_min"] = 0
        self.mapvars["chunkx_max"] = 0
        self.mapvars["chunkz_max"] = 0
        self.mapvars["chunk_size"] = 16
        self.mapvars["maxheight"] = 96
        self.mapvars["minheight"] = -32
        self.mapvars["pixelspernode"] = 1
        self.saved_mapvars = get_dict_from_conf_file(self.world_yaml_path,":")
        is_mapvars_changed = False
        if self.saved_mapvars is None:
            is_mapvars_changed = True
            #self.save_mapvars_if_changed()
        #self.mapvars = get_dict_from_conf_file(self.world_yaml_path,":")
        #NOTE: do not save or load self.mapvars yet, because if world name is different than saved, chunks must all be redone
        if self.saved_mapvars is not None:
            if "chunkx_min" in self.saved_mapvars.keys():
                self.mapvars["chunkx_min"] = self.saved_mapvars["chunkx_min"]
            if "chunkx_max" in self.saved_mapvars.keys():
                self.mapvars["chunkx_max"] = self.saved_mapvars["chunkx_max"]
            if "chunkz_min" in self.saved_mapvars.keys():
                self.mapvars["chunkz_min"] = self.saved_mapvars["chunkz_min"]
            if "chunkz_max" in self.saved_mapvars.keys():
                self.mapvars["chunkz_max"] = self.saved_mapvars["chunkz_max"]

        if self.mapvars is not None:
            if "chunkx_min" in self.mapvars.keys():
                try:
                    self.mapvars["chunkx_min"] = int(self.mapvars["chunkx_min"])
                except:
                    print("WARNING: chunkx_min was not int so set to 0")
                    self.mapvars["chunkx_min"] = 0
            if "chunkx_max" in self.mapvars.keys():
                try:
                    self.mapvars["chunkx_max"] = int(self.mapvars["chunkx_max"])
                except:
                    print("WARNING: chunkx_max was not int so set to 0")
                    self.mapvars["chunkx_max"] = 0
            if "chunkz_min" in self.mapvars.keys():
                try:
                    self.mapvars["chunkz_min"] = int(self.mapvars["chunkz_min"])
                except:
                    print("WARNING: chunkz_min was not int so set to 0")
                    self.mapvars["chunkz_min"] = 0
            if "chunkz_max" in self.mapvars.keys():
                try:
                    self.mapvars["chunkz_max"] = int(self.mapvars["chunkz_max"])
                except:
                    print("WARNING: chunkz_max was not int so set to 0")
                    self.mapvars["chunkz_max"] = 0
        if is_mapvars_changed:
            self.save_mapvars_if_changed()
        if is_config_changed:
            self.save_config()

    #def install_default_world_data(self):
        #source_web_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "web")
        #dest_web_chunkymapdata_world_path = self.chunkymap_thisworld_data_path
        #dest_web_chunkymapdata_world_players_path = os.path.join(self.chunkymap_thisworld_data_path, "players")
        #install_list.append(InstalledFile("singleplayer.png", source_chunkymapdata_players, dest_chunkymapdata_players))


    #formerly install_website
    def install_default_world_data(self):
        source_web_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "web")
        source_web_chunkymapdata_path = os.path.join(source_web_path, "chunkymapdata_default")
        source_web_chunkymapdata_world_path = os.path.join(source_web_chunkymapdata_path, "world")
        source_web_chunkymapdata_images_path = os.path.join(source_web_chunkymapdata_path, "images")
        dest_web_path = self.config["www_minetest_path"]
        dest_web_chunkymapdata_path = os.path.join(self.config["www_minetest_path"],"chunkymapdata")
        dest_web_chunkymapdata_images_path = os.path.join(dest_web_chunkymapdata_path,"images")
        install_list = list()
        install_list.append(InstalledFile("browser.php",source_web_path,dest_web_path))
        install_list.append(InstalledFile("chunkymap.php",source_web_path,dest_web_path))
        install_list.append(InstalledFile("example.php",source_web_path,dest_web_path))
        install_list.append(InstalledFile("zoom-in.png", source_web_chunkymapdata_images_path, dest_web_chunkymapdata_images_path))
        install_list.append(InstalledFile("zoom-out.png", source_web_chunkymapdata_images_path, dest_web_chunkymapdata_images_path))
        install_list.append(InstalledFile("zoom-in_disabled.png", source_web_chunkymapdata_images_path, dest_web_chunkymapdata_images_path))
        install_list.append(InstalledFile("zoom-out_disabled.png", source_web_chunkymapdata_images_path, dest_web_chunkymapdata_images_path))
        install_list.append(InstalledFile("start.png", source_web_chunkymapdata_images_path, dest_web_chunkymapdata_images_path))
        install_list.append(InstalledFile("target_start.png", source_web_chunkymapdata_images_path, dest_web_chunkymapdata_images_path))
        install_list.append(InstalledFile("compass-rose.png", source_web_chunkymapdata_images_path, dest_web_chunkymapdata_images_path))
        source_chunkymapdata_players = os.path.join(source_web_chunkymapdata_world_path, "players")
        dest_chunkymapdata_players = os.path.join(self.chunkymap_thisworld_data_path, "players")
        install_list.append(InstalledFile("singleplayer.png", source_chunkymapdata_players, dest_chunkymapdata_players))
        source_chunkymapdata_markers = os.path.join(source_web_chunkymapdata_world_path, "markers")
        dest_chunkymapdata_markers = os.path.join(self.chunkymap_thisworld_data_path, "markers")
        install_list.append(InstalledFile("0.yml", source_chunkymapdata_markers, dest_chunkymapdata_markers))
        for this_object in install_list:
            source_path = os.path.join(this_object.source_dir_path, this_object.file_name)
            installed_path = os.path.join(this_object.dest_dir_path, this_object.file_name)
            if os.path.isfile(source_path):
                if not os.path.isdir(this_object.dest_dir_path):
                    os.makedirs(this_object.dest_dir_path)
                if not os.path.isfile(installed_path):
                    shutil.copyfile(source_path, installed_path) # DOES replace destination file
                else:
                    source_mtime_seconds = time.ctime(os.path.getmtime(source_path))
                    installed_mtime_seconds = time.ctime(os.path.getmtime(installed_path))
                    if source_mtime_seconds>installed_mtime_seconds:
                        shutil.copyfile(source_path, installed_path) # DOES replace destination file
            else:
                print("WARNING: cannot update file since can't find '"+source_path+"'")


    def deny_http_access(self, dir_path):
        htaccess_name = ".htaccess"
        htaccess_path = os.path.join(dir_path, htaccess_name)
        outs = open(htaccess_path, 'w')
        outs.write("IndexIgnore *"+"\n")
        outs.write("<Files .htaccess>"+"\n")
        outs.write("order allow,deny"+"\n")
        outs.write("deny from all"+"\n")
        outs.write("</Files>"+"\n")
        outs.write("<Files *.php>"+"\n")
        outs.write("order allow,deny"+"\n")
        outs.write("deny from all"+"\n")
        outs.write("</Files>"+"\n")
        outs.close()

    def save_config(self):
        save_conf_from_dict(self.config_path, self.config, ":")

    #locally unique identifier (unique to world only)
    def get_chunk_luid(self, chunky_x, chunky_z):
        return "x"+str(chunky_x)+"z"+str(chunky_z)

    def get_decachunk_image_name_from_chunk(self, chunky_x, chunky_z):
        return "decachunk_"+self.get_decachunk_luid_from_chunk(chunky_x, chunky_z)+".jpg"

    def get_decachunk_image_name_from_decachunk(self, decachunky_x, decachunky_z):
        return "decachunk_"+self.get_decachunk_luid_from_decachunk(decachunky_x, decachunky_z)+".jpg"

    def get_decachunk_luid_from_chunk(self, chunky_x, chunky_z):
        decachunky_x = int(math.floor(chunky_x/10))
        decachunky_z = int(math.floor(chunky_z/10))
        return self.get_chunk_luid(decachunky_x, decachunky_z)

    def get_decachunk_luid_from_decachunk(self, decachunky_x, decachunky_z):
        return self.get_chunk_luid(decachunky_x, decachunky_z)

    def get_decachunk_yaml_name_from_chunk(self, chunky_x, chunky_z):
        return "decachunk_"+self.get_decachunk_luid_from_chunk(chunky_x, chunky_z)+".yml"

    def get_decachunk_yaml_name_from_decachunk(self, decachunky_x, decachunky_z):
        return "decachunk_"+self.get_decachunk_luid_from_decachunk(decachunky_x, decachunky_z)+".yml"

    def get_chunk_image_name(self, chunky_x, chunky_z):
        return "chunk_"+self.get_chunk_luid(chunky_x, chunky_z)+".png"

    #def get_decachunk_image_tmp_path_from_decachunk(self, chunky_x, chunky_z):
        #return os.path.join(os.path.dirname(os.path.abspath(__file__)), self.get_decachunk_image_name_from_decachunk(chunky_x, chunky_z))

    def get_chunk_image_tmp_path(self, chunky_x, chunky_z):
        return os.path.join(os.path.dirname(os.path.abspath(__file__)), self.get_chunk_image_name(chunky_x, chunky_z))

    def get_signal_name(self):
        return "chunkymap-signals.txt"

    def get_signal_path(self):
        return os.path.join(os.path.dirname(os.path.abspath(__file__)), self.get_signal_name())

    def check_decachunk_containing_chunk(self, chunky_x, chunky_z):
        chunk16_coord_list = list()
        decachunky_x = int(math.floor(chunky_x/10))
        decachunky_z = int(math.floor(chunky_z/10))
        chunk16x_min = decachunky_x*10
        chunk16x_max = chunk16x_min + 15  # NOTE: + 15 even if negative since originally, floor was used
        chunk16z_min = decachunky_z*10
        chunk16z_max = chunk16z_min + 15  # NOTE: + 15 even if negative since originally, floor was used
        is_any_part_queued = False
        chunky_z = chunk16x_min
        while chunky_z <= chunk16z_max:
            chunky_x = chunk16x_min
            while chunky_x <=  chunk16x_max:
                coords = (chunky_x, chunky_z)
                chunk16_coord_list.append( coords )
                if self.todo_index<len(self.todo_positions):
                    for index in range(self.todo_index,len(self.todo_positions)):
                        if ivec2_equals(self.todo_positions[self.todo_index], coords):
                            is_any_part_queued = True
                            break
                if is_any_part_queued:
                    break
                chunky_x += 1
            if is_any_part_queued:
                break
            chunky_z += 1
        if not is_any_part_queued:
            print("    Rendering 160px decachunk "+str((decachunky_x, decachunky_z)))
            decachunk_global_coords = decachunky_x*160, decachunky_z*160
            im = Image.new("RGB", (160, 160), self.FLAG_EMPTY_HEXCOLOR)
            decachunk_yaml_path = self.get_decachunk_yaml_path_from_decachunk(decachunky_x, decachunky_z)
            decachunk_image_path = self.get_decachunk_image_path_from_decachunk(decachunky_x, decachunky_z)
            combined_count = 0
            contains_chunk_luids = list()
            for coord in chunk16_coord_list:
                chunky_x, chunky_z = coord
                chunk_image_path = self.get_chunk_image_path(chunky_x, chunky_z)
                if os.path.isfile(chunk_image_path):
                    participle="initializing"
                    try:
                        participle="opening path"
                        chunk_im = Image.open(open(chunk_image_path, 'rb'))  # double-open to make sure file is finished writing
                        #NOTE: PIL automatically closes, otherwise you can do something like https://bytes.com/topic/python/answers/24308-pil-do-i-need-close
                        #fp = open(file_name, "rb")
                        #im = Image.open(fp) # open from file object
                        #im.load() # make sure PIL has read the data
                        #fp.close()
                        chunk_global_coords = chunky_x*16, chunky_z*16
                        chunk_local_coords = chunk_global_coords[0]-decachunk_global_coords[0], chunk_global_coords[1]-decachunk_global_coords[1]
                        offset = chunk_local_coords[0], 160-chunk_local_coords[1]  # convert to inverted cartesian since that's the coordinate system of images
                        im.paste(chunk_im, offset)
                        contains_chunk_luids.append(self.get_chunk_luid(chunky_x, chunky_z))
                    except:
                        print("Could not finish "+participle+" in check_decachunk_containing_chunk:")
                        view_traceback()
            decachunk_folder_path = self.get_decachunk_folder_path_from_decachunk(decachunky_x, decachunky_z)
            if not os.path.isdir(decachunk_folder_path):
                os.makedirs(decachunk_folder_path)
                print("    Made folder '"+decachunk_folder_path+"'")
            else:
                print("    Found folder '"+decachunk_folder_path+"'")
            print("    Saving '"+decachunk_image_path+"'")
            im.save(decachunk_image_path)
            decachunk_luid = self.get_decachunk_luid_from_decachunk(decachunky_x, decachunky_z)
            self.prepare_decachunk_meta_from_decachunk(decachunky_x, decachunky_z)
            this_second = int(time.time())
            #if int(self.decachunks[decachunk_luid].metadata["last_saved_utc_second"]) != this_second:
            self.decachunks[decachunk_luid].metadata["last_saved_utc_second"] = this_second  # time.time() returns float even if OS doesn't give a time in increments smaller than seconds
            if len(contains_chunk_luids)>0:
                self.decachunks[decachunk_luid].metadata["contains_chunk_luids"] = ','.join(contains_chunk_luids)
            else:
                self.decachunks[decachunk_luid].metadata["contains_chunk_luids"] = None
            self.decachunks[decachunk_luid].save_yaml(decachunk_yaml_path)

    def get_chunk_folder_path(self, chunky_x, chunky_z):
        result = None
        decachunky_x = int(math.floor(chunky_x/10))
        decachunky_z = int(math.floor(chunky_z/10))
        result = os.path.join( os.path.join(self.data_16px_path, str(decachunky_x)), str(decachunky_z) )
        return result

    def get_decachunk_folder_path_from_chunk(self, chunky_x, chunky_z):
        result = None
        if chunky_x is not None and chunky_z is not None:
            hectochunky_x = int(math.floor(chunky_x/100))
            hectochunky_x = int(math.floor(chunky_z/100))
            result = os.path.join( os.path.join(self.data_160px_path, str(hectochunky_x)), str(hectochunky_x) )
        return result

    def get_decachunk_folder_path_from_decachunk(self, decachunky_x, decachunky_z):
        result = None
        if decachunky_x is not None and decachunky_z is not None:
            hectochunky_x = int(math.floor(decachunky_x/10))
            hectochunky_x = int(math.floor(decachunky_z/10))
            result = os.path.join( os.path.join(self.data_160px_path, str(hectochunky_x)), str(hectochunky_x) )
        return result

    def create_chunk_folder(self, chunky_x, chunky_z):
        path = self.get_chunk_folder_path(chunky_x, chunky_z)
        if not os.path.isdir(path):
            os.makedirs(path)

    def get_decachunk_image_path_from_chunk(self, chunky_x, chunky_z):
        return os.path.join(self.get_decachunk_folder_path_from_chunk(chunky_x, chunky_z), self.get_decachunk_image_name_from_chunk(chunky_x, chunky_z))

    def get_decachunk_yaml_path_from_chunk(self, chunky_x, chunky_z):
        return os.path.join(self.get_decachunk_folder_path_from_chunk(chunky_x, chunky_z), self.get_decachunk_yaml_name_from_chunk(chunky_x, chunky_z))

    def get_decachunk_image_path_from_decachunk(self, decachunky_x, decachunky_z):
        return os.path.join(self.get_decachunk_folder_path_from_decachunk(decachunky_x, decachunky_z), self.get_decachunk_image_name_from_decachunk(decachunky_x, decachunky_z))

    def get_decachunk_yaml_path_from_decachunk(self, decachunky_x, decachunky_z):
        return os.path.join(self.get_decachunk_folder_path_from_decachunk(decachunky_x, decachunky_z), self.get_decachunk_yaml_name_from_decachunk(decachunky_x, decachunky_z))

    def get_chunk_image_path(self, chunky_x, chunky_z):
        return os.path.join(self.get_chunk_folder_path(chunky_x, chunky_z), self.get_chunk_image_name(chunky_x, chunky_z))

    def get_chunk_genresult_name(self, chunky_x, chunky_z):
        chunk_luid = self.get_chunk_luid(chunky_x, chunky_z)
        return self.genresult_name_opener_string+chunk_luid+self.genresult_name_closer_string

    def get_chunk_luid_from_genresult_name(self, file_name):
        return file_name[len(self.genresult_name_opener_string):-1*len(self.genresult_name_closer_string)]

    def get_chunk_genresult_tmp_folder(self, chunky_x, chunky_z):
        #coords = self.get_coords_from_luid(chunk_luid)
        #if coords is not None:
        #    chunky_x, chunky_z = coords
        tmp_path = self.get_chunk_genresults_base_path()
        decachunky_x = int(math.floor(chunky_x/10))
        decachunky_z = int(math.floor(chunky_z/10))
        tmp_path = os.path.join( os.path.join(tmp_path, str(decachunky_x)), str(decachunky_z) )
        return tmp_path

    def get_chunk_genresults_base_path(self):
        #formerly get_chunk_genresults_tmp_folder(self, chunk_luid)
        return os.path.join(os.path.dirname(os.path.abspath(__file__)), "chunkymap-genresults")

    def get_chunk_genresult_tmp_path(self, chunky_x, chunky_z):
        return os.path.join(self.get_chunk_genresult_tmp_folder(chunky_x, chunky_z), self.get_chunk_genresult_name(chunky_x, chunky_z))

    def get_chunk_luid_from_yaml_name(self, file_name):
        return file_name[len(self.chunk_yaml_name_opener_string):-1*len(self.chunk_yaml_name_dotext_string)]


    def get_chunk_yaml_name(self, chunky_x, chunky_z):
        chunk_luid = self.get_chunk_luid(chunky_x, chunky_z)
        return self.chunk_yaml_name_opener_string+chunk_luid+self.chunk_yaml_name_dotext_string

    def is_chunk_yaml_present(self, chunky_x, chunky_z):
        return os.path.isfile(self.get_chunk_yaml_path(chunky_x, chunky_z))

    def get_chunk_yaml_path(self, chunky_x, chunky_z):
        return os.path.join(self.get_chunk_folder_path(chunky_x, chunky_z), self.get_chunk_yaml_name(chunky_x, chunky_z))

    def is_chunk_yaml_marked(self, chunky_x, chunky_z):
        yaml_path = self.get_chunk_yaml_path(chunky_x, chunky_z)
        result = False
        if os.path.isfile(yaml_path):
            result = True
            #ins = open(yaml_path, 'r')
            #line = True
            #while line:
            #    line = ins.readline()
            #    if line:
            #        line_strip = line.strip()
            #        if "is_empty:" in line_strip:
            #            result = True
            #            break
            #ins.close()
        return result

    def is_chunk_yaml_marked_empty(self, chunky_x, chunky_z):
        result = False
        yaml_path = self.get_chunk_yaml_path(chunky_x, chunky_z)
        if os.path.isfile(yaml_path):
            self.prepare_chunk_meta(chunky_x, chunky_z)  # DOES get existing data if any file exists
            chunk_luid = self.get_chunk_luid(chunky_x, chunky_z)
            if "is_empty" in self.chunks[chunk_luid].metadata.keys():
                result = self.chunks[chunk_luid].metadata["is_empty"]

        return result

    def remove_chunk_image(self, chunky_x, chunky_z):
        result = False
        tmp_png_path = self.get_chunk_image_path(chunky_x, chunky_z)
        if os.path.isfile(tmp_png_path):
            result = True
            os.remove(tmp_png_path)
        return result

    def remove_chunk(self, chunky_x, chunky_z):
        result = False
        chunk_luid = get_chunk_luid(chunky_x, chunky_z)
        out_path = self.get_chunk_genresult_tmp_path(chunky_x, chunky_z)
        tmp_png_path = self.get_chunk_image_path(chunky_x, chunky_z)
        yml_path = self.get_chunk_yaml_path(chunky_x, chunky_z)
        if os.path.isfile(tmp_png_path):
            os.remove(tmp_png_path)
            result = True
        if os.path.isfile(yml_path):
            os.remove(yml_path)
            result = True
        if os.path.isfile(out_path):
            os.remove(out_path)
            result = True
        #TODO: if folder becomes empty, remove it
        return result

    def is_chunk_rendered_on_dest(self, chunky_x, chunky_z):  #formerly is_chunk_empty_on_dest (reversed)
        is_rendered = False
        dest_png_path = self.get_chunk_image_path(chunky_x, chunky_z)
        if os.path.isfile(dest_png_path):
            is_rendered = True
        return is_rendered

    def prepare_decachunk_meta_from_chunk(self, chunky_x, chunky_z):
        chunk_luid = self.get_decachunk_luid_from_chunk(chunky_x, chunky_z)
        if chunk_luid not in self.decachunks.keys():
            self.decachunks[chunk_luid] = MTDecaChunk()
            #self.chunks[chunk_luid].luid = chunk_luid
            yaml_path = self.get_decachunk_yaml_path_from_chunk(chunky_x, chunky_z)
            if os.path.isfile(yaml_path):
                self.decachunks[chunk_luid].load_yaml(yaml_path)

    def prepare_decachunk_meta_from_decachunk(self, decachunky_x, decachunky_z):
        chunk_luid = self.get_decachunk_luid_from_decachunk(decachunky_x, decachunky_z)
        if chunk_luid not in self.decachunks.keys():
            self.decachunks[chunk_luid] = MTDecaChunk()
            #self.chunks[chunk_luid].luid = chunk_luid
            yaml_path = self.get_decachunk_yaml_path_from_decachunk(decachunky_x, decachunky_z)
            if os.path.isfile(yaml_path):
                self.decachunks[chunk_luid].load_yaml(yaml_path)

    def prepare_chunk_meta(self, chunky_x, chunky_z):
        chunk_luid = self.get_chunk_luid(chunky_x, chunky_z)
        if chunk_luid not in self.chunks.keys():
            self.chunks[chunk_luid] = MTChunk()
            #self.chunks[chunk_luid].luid = chunk_luid
            yaml_path = self.get_chunk_yaml_path(chunky_x, chunky_z)
            if os.path.isfile(yaml_path):
                self.chunks[chunk_luid].load_yaml(yaml_path)


    # normally call check_chunk instead, which renders chunk only if necessary
    def _render_chunk(self, chunky_x, chunky_z):
        min_indent = "  "  # increased below
        result = False
        chunk_luid = self.get_chunk_luid(chunky_x, chunky_z)
        png_name = self.get_chunk_image_name(chunky_x, chunky_z)
        tmp_png_path = self.get_chunk_image_tmp_path(chunky_x, chunky_z)
        genresult_name = self.get_chunk_genresult_name(chunky_x, chunky_z)
        genresult_tmp_folder_path = self.get_chunk_genresult_tmp_folder(chunky_x, chunky_z)
        if not os.path.isdir(genresult_tmp_folder_path):
            os.makedirs(genresult_tmp_folder_path)
        genresult_path = self.get_chunk_genresult_tmp_path(chunky_x, chunky_z)
        x_min = chunky_x * self.mapvars["chunk_size"]
        x_max = chunky_x * self.mapvars["chunk_size"] + self.mapvars["chunk_size"] - 1
        z_min = chunky_z * self.mapvars["chunk_size"]
        z_max = chunky_z * self.mapvars["chunk_size"] + self.mapvars["chunk_size"] - 1

        #print (min_indent+"generating chunky_x = " + str(x_min) + " to " + str(x_max) + " ,  chunky_z = " + str(z_min) + " to " + str(z_max))
        geometry_value_string = str(x_min)+":"+str(z_min)+"+"+str(int(x_max)-int(x_min)+1)+"+"+str(int(z_max)-int(z_min)+1)  # +1 since max-min is exclusive and width must be inclusive for minetestmapper.py
        cmd_suffix = ""
        cmd_suffix = " > \""+genresult_path+"\""
        #self.mapper_id = "minetestmapper-region"
        cmd_no_out_string = self.python_exe_path + " \""+self.minetestmapper_py_path + "\" --region " + str(x_min) + " " + str(x_max) + " " + str(z_min) + " " + str(z_max) + " --maxheight "+str(self.mapvars["maxheight"])+" --minheight "+str(self.mapvars["minheight"])+" --pixelspernode "+str(self.mapvars["pixelspernode"])+" \""+self.config["world_path"]+"\" \""+tmp_png_path+"\""
        cmd_string = cmd_no_out_string + cmd_suffix

        if self.minetestmapper_py_path==self.minetestmapper_custom_path:#if self.backend_string!="sqlite3": #if self.mapper_id=="minetestmapper-region":
            #  Since minetestmapper-numpy has trouble with leveldb:
            #    such as sudo minetest-mapper --input "/home/owner/.minetest/worlds/FCAGameAWorld" --geometry -32:-32+64+64 --output /var/www/html/minetest/try1.png
            #    where geometry option is like --geometry x:y+w+h
            #    mapper_id = "minetest-mapper"
            #    NOTE: minetest-mapper is part of the minetest-data package, which can be installed alongside the git version of minetestserver
            #    BUT *buntu Trusty version of it does NOT have geometry option
            #    cmd_string = "/usr/games/minetest-mapper --input \""+self.config["world_path"]+"\" --draworigin --geometry "+geometry_value_string+" --output \""+tmp_png_path+"\""+cmd_suffix
            #    such as sudo python minetestmapper --input "/home/owner/.minetest/worlds/FCAGameAWorld" --geometry -32:-32+64+64 --output /var/www/html/minetest/try1.png
            # OR try PYTHON version (looks for expertmm fork which has geometry option like C++ version does):
            #script_path = "/home/owner/minetest/util/minetestmapper.py"
            #region_capable_script_path = "/home/owner/minetest/util/chunkymap/minetestmapper.py"
            #    region_capable_script_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "minetestmapper.py")
            #    if os.path.isfile(region_capable_script_path):
            #        script_path=region_capable_script_path
            #if os.path.isfile(region_capable_script_path):
                #script_path = region_capable_script_path
            geometry_string = str(x_min)+":"+str(z_min)+"+"+str(int(x_max)-int(x_min)+1)+"+"+str(int(z_max)-int(z_min)+1)  # +1 since max-min is exclusive and width must be inclusive for minetestmapper.py
            #expertmm_region_string = str(x_min) + ":" + str(x_max) + "," + str(z_min) + ":" + str(z_max)
            #cmd_string="sudo python "+script_path+" --input \""+self.config["world_path"]+"\" --geometry "+geometry_value_string+" --output \""+tmp_png_path+"\""+cmd_suffix
            cmd_no_out_string = self.python_exe_path+" "+self.minetestmapper_py_path+" --bgcolor '"+self.FLAG_EMPTY_HEXCOLOR+"' --input \""+self.config["world_path"]+"\" --geometry "+geometry_string+" --output \""+tmp_png_path+"\""
            cmd_string = cmd_no_out_string + cmd_suffix
            #sudo python /home/owner/minetest/util/minetestmapper.py --bgcolor '#010000' --input "/home/owner/.minetest/worlds/FCAGameAWorld" --output /var/www/html/minetest/chunkymapdata/entire.png > entire-mtmresult.txt
            #sudo python /home/owner/minetest/util/chunkymap/minetestmapper.py --input "/home/owner/.minetest/worlds/FCAGameAWorld" --geometry 0:0+16+16 --output /var/www/html/minetest/chunkymapdata/chunk_x0z0.png > /home/owner/minetest/util/chunkymap-genresults/chunk_x0z0_mapper_result.txt
            #    sudo mv entire-mtmresult.txt /home/owner/minetest/util/chunkymap-genresults/

        dest_png_path = self.get_chunk_image_path(chunky_x, chunky_z)
        #is_empty_chunk = is_chunk_yaml_marked(chunky_x, chunky_z) and is_chunk_yaml_marked_empty(chunky_x, chunky_z)
        #if self.verbose_enable:
        #    #print(min_indent+"")
        #    print(min_indent+"Running '"+cmd_string+"'...")
        #else:
        print (min_indent+"Calling map tile renderer for: "+str((chunky_x, chunky_z)))
        min_indent += "  "
        try:
            if os.path.isfile(tmp_png_path):
                os.remove(tmp_png_path)
            subprocess.call(cmd_string, shell=True)  # TODO: remember not to allow arbitrary command execution, which could happen if input contains ';' when using shell=True
            #is_empty_before = True
            #is_marked_before = False
            self.prepare_chunk_meta(chunky_x, chunky_z)  # DOES load existing yml if exists
            old_meta = get_dict_deepcopy(self.chunks[chunk_luid].metadata)
            is_marked_before = self.chunks[chunk_luid].metadata["is_marked"]
            is_empty_before = self.chunks[chunk_luid].metadata["is_empty"]
            #if chunk_luid in self.chunks.keys():
                #is_marked_before = True
                #if (self.chunks[chunk_luid].metadata is not None) and ("is_empty" in self.chunks[chunk_luid].metadata):
                #    is_empty_before = self.chunks[chunk_luid].metadata["is_empty"]
            this_chunk = self.chunks[chunk_luid]
            if os.path.isfile(tmp_png_path):
                result = True
                this_chunk.metadata["is_empty"] = False
                try:
                    if (os.path.isfile(dest_png_path)):
                        os.remove(dest_png_path)
                except:
                    print (min_indent+"Could not finish deleting '"+dest_png_path+"'")
                try:
                    self.create_chunk_folder(chunky_x, chunky_z)
                    os.rename(tmp_png_path, dest_png_path)
                    print(min_indent+"(moved to '"+dest_png_path+"')")
                    self.total_newly_rendered += 1
                    self.prepare_chunk_meta(chunky_x, chunky_z)  # DOES load existing yml if exists
                    self.chunks[chunk_luid].is_fresh = True
                    self.chunks[chunk_luid].metadata["is_empty"] = False
                except:
                    print (min_indent+"Could not finish moving '"+tmp_png_path+"' to '"+dest_png_path+"'")
            else:
                if self.is_chunk_traversed_by_player(chunk_luid):
                    print (min_indent+"WARNING: no chunk data though traversed by player:")
                    print(min_indent+"standard output stream:")
                    line_count = print_file(genresult_path, min_indent+"  ")
                    if line_count>0:
                        print(min_indent+"  #EOF: "+str(line_count)+" line(s) in '"+genresult_path+"'")
                        pass
                    else:
                        print(min_indent+"  #EOF: "+str(line_count)+" line(s) in '"+genresult_path+"'")
                        subprocess.call(cmd_no_out_string+" 2> \""+genresult_path+"\"", shell=True)
                        print(min_indent+"standard error stream:")
                        line_count = print_file(genresult_path, min_indent+"  ")
                        if (line_count<1):
                            print(min_indent+"  #EOF: "+str(line_count)+" line(s) in '"+genresult_path+"'")
                        print(min_indent+"  (done output of '"+cmd_no_out_string+"')")
                        try:
                            if os.path.exists(tmp_png_path):
                                os.rename(tmp_png_path, dest_png_path)
                        except:
                            pass
            try:
                is_changed = this_chunk.set_from_genresult(genresult_path)
                if is_marked_before:
                    if (not is_empty_before) and this_chunk.metadata["is_empty"]:
                        print("ERROR: chunk changed from nonempty to empty (may happen if output of mapper was not recognized)")
                    elif this_chunk.metadata["is_empty"] and os.path.isfile(dest_png_path):
                        print("ERROR: chunk marked empty though has data (may happen if output of mapper was not recognized)")
                #chunk_yaml_path = self.get_chunk_yaml_path(chunky_x, chunky_z)
                #self.create_chunk_folder(chunky_x, chunky_z)
                #this_chunk.save_yaml(chunk_yaml_path)
                #if is_changed:
                if not is_dict_subset(self.chunks[chunk_luid].metadata, old_meta, False):  # , True, "chunk_yaml_path")
                    self.save_chunk_meta(chunky_x, chunky_z)
                #print(min_indent+"(saved yaml to '"+chunk_yaml_path+"')")
                if not self.is_save_output_ok:
                    if os.path.isfile(genresult_path):
                        os.remove(genresult_path)
            except:
                print (min_indent+"Could not finish deleting/moving output")
                view_traceback()
        except:
            print(min_indent+"Could not finish deleting/moving temp files")
            view_traceback()


        return result

    def save_chunk_meta(self, chunky_x, chunky_z):
        chunk_yaml_path = self.get_chunk_yaml_path(chunky_x, chunky_z)
        chunk_luid = self.get_chunk_luid(chunky_x, chunky_z)
        if not chunk_luid in self.chunks:
            self.prepare_chunk_meta(chunky_x, chunky_z)
        self.create_chunk_folder(chunky_x, chunky_z)
        self.chunks[chunk_luid].save_yaml(chunk_yaml_path)
        print(min_indent+"(saved yaml to '"+chunk_yaml_path+"')")

    def check_players(self):
        print("PROCESSING PLAYERS")

        players_path = os.path.join(self.config["world_path"], "players")
        player_count = 0
        player_written_count = 0
        players_moved_count = 0
        players_didntmove_count = 0
        players_saved_count = 0
        for base_path, dirnames, filenames in os.walk(players_path):
            for file_name in filenames:
                file_path = os.path.join(players_path,file_name)
                #print ("  EXAMINING "+file_name)
                #badstart_string = "."
                player_name = None
                player_position = None
                #if (file_name[:len(badstart_string)]!=badstart_string):
                if (file_name[:1]!="."):
                    ins = open(file_path, 'r')
                    line = True
                    is_enough_data = False
                    while line:
                        line = ins.readline()
                        if line:
                            ao_index = line.find("=")
                            if ao_index > 0:
                                found_name = line[:ao_index].strip()
                                found_value = line[ao_index+1:].strip()
                                if found_name=="name":
                                    player_name = found_value
                                elif found_name=="position":
                                    player_position = found_value

                                if (player_name is not None) and (player_position is not None):
                                    is_enough_data = True
                                    break
                    ins.close()
                    player_dest_path = os.path.join(self.chunkymap_players_path,file_name+".yml")
                    player_x = None
                    player_y = None
                    player_z = None
                    chunk_x = None
                    chunk_y = None
                    chunk_z = None

                    player_position_tuple = get_tuple_from_notation(player_position, file_name)
                    if player_position_tuple is not None:
                        #Divide by 10 because I don't know why (minetest issue, maybe to avoid float rounding errors upon save/load)
                        player_position_tuple = player_position_tuple[0]/10.0, player_position_tuple[1]/10.0, player_position_tuple[2]/10.0
                        player_x, player_y, player_z = player_position_tuple
                        player_x = float(player_x)
                        player_y = float(player_y)
                        player_z = float(player_z)
                        chunky_x = int((int(player_x)/self.mapvars["chunk_size"]))
                        chunky_y = int((int(player_y)/self.mapvars["chunk_size"]))
                        chunky_z = int((int(player_z)/self.mapvars["chunk_size"]))
                        chunk_luid = self.get_chunk_luid(chunky_x, chunky_z)
                        self.prepare_chunk_meta(chunky_x, chunky_z)  # DOES load existing yml if exists
                        if not self.chunks[chunk_luid].metadata["is_traversed"]:
                            self.chunks[chunk_luid].metadata["is_traversed"] = True
                            self.save_chunk_meta(chunky_x, chunky_z)

                    #if is_enough_data:
                    #if player_name!="singleplayer":
                    map_player_dict = get_dict_from_conf_file(player_dest_path,":")
                    #map_player_position_tuple = None
                    saved_player_x = None
                    saved_player_y = None
                    saved_player_y = None
                    if map_player_dict is not None:
                        #map_player_position_tuple = saved_player_x, saved_player_y, saved_player_z
                        if "x" in map_player_dict.keys():
                            saved_player_x = float(map_player_dict["x"])
                        if "y" in map_player_dict.keys():
                            saved_player_y = float(map_player_dict["y"])
                        if "z" in map_player_dict.keys():
                            saved_player_z = float(map_player_dict["z"])

                    #if (map_player_dict is None) or not is_same_fvec3( map_player_position_tuple, player_position_tuple):
                    if (map_player_dict is None) or (saved_player_x is None) or (saved_player_z is None) or (int(saved_player_x)!=int(player_x)) or (int(saved_player_y)!=int(player_y)) or (int(saved_player_z)!=int(player_z)):
                        # don't check y since y is elevation in minetest, don't use float since subblock position doesn't matter to map
                        if map_player_dict is not None and saved_player_x is not None and saved_player_y is not None and saved_player_z is not None:
                            #print("PLAYER MOVED: "+str(player_name)+" moved from "+str(map_player_position_tuple)+" to "+str(player_position_tuple))
                            if self.verbose_enable:
                                print("PLAYER MOVED: "+str(player_name)+" moved from "+str(saved_player_x)+","+str(saved_player_y)+","+str(saved_player_z)+" to "+str(player_x)+","+str(player_y)+","+str(player_z))
                            players_moved_count += 1
                        else:
                            if self.verbose_enable:
                                print("SAVING YAML for player '"+str(player_name)+"'")
                            players_saved_count += 1
                        outs = open(player_dest_path, 'w')
                        if player_name is not None:
                            outs.write("name:"+player_name+"\n")  # python automatically uses correct newline for your os when you put "\n"
                        #if player_position is not None:
                        #    outs.write("position:"+player_position+"\n")
                        if player_x is not None:
                            outs.write("x:"+str(player_x)+"\n")
                        if player_y is not None:
                            outs.write("y:"+str(player_y)+"\n")
                        if player_z is not None:
                            outs.write("z:"+str(player_z)+"\n")
                        outs.write("is_enough_data:"+str(is_enough_data))
                        outs.close()
                        player_written_count += 1
                    else:
                        #if self.verbose_enable:
                            #print("DIDN'T MOVE: "+str(player_name))
                        players_didntmove_count += 1
                    player_count += 1
        #if not self.verbose_enable:
        print("PLAYERS:")
        print("  saved: "+str(player_written_count)+" (moved:"+str(players_moved_count)+"; new:"+str(players_saved_count)+")")
        print("  didn't move: "+str(players_didntmove_count))

    def is_chunk_traversed_by_player(self, chunk_luid):
        result = False
        if chunk_luid in self.chunks.keys():
            result = self.chunks[chunk_luid].metadata["is_traversed"]
        return result

    def is_chunk_fresh(self, chunk_luid):
        result = False
        if chunk_luid in self.chunks.keys():
            result = self.chunks[chunk_luid].is_fresh
        return result


    #Returns: (boolean) whether the chunk image is present on dest (rendered now or earlier)--only possible if there is chunk data at the given location
    def check_chunk(self, chunky_x, chunky_z):
        min_indent = "  "
        result = [False,""]
        chunk_luid = self.get_chunk_luid(chunky_x, chunky_z)

        #if (is_different_world):  #instead, see above where all chunk files and player files are deleted
        #    self.remove_chunk(chunky_x, chunky_z)

        is_traversed_by_player = self.is_chunk_traversed_by_player(chunk_luid)  #ok if stale, since is only used for whether empty chunk should be regenerated

        is_render_needed = False

        if not self.is_chunk_fresh(chunk_luid):
            if is_traversed_by_player:
                if self.is_chunk_yaml_marked(chunky_x, chunky_z):
                    if self.is_chunk_yaml_marked_empty(chunky_x, chunky_z):
                        is_render_needed = True
                        result[1] = "RENDERING since nonfresh empty traversed"
                        if self.verbose_enable:
                            print (min_indent+chunk_luid+": "+result[1])
                        #else:
                            #sys.stdout.write('.')
                    else:
                        if self.is_chunk_rendered_on_dest(chunky_x, chunky_z):
                            result[1] = "SKIPPING since RENDERED nonfresh nonempty traversed"
                            if self.verbose_enable:
                                print (min_indent+chunk_luid+": "+result[1])
                        else:
                            is_render_needed = True
                            result[1] = "RENDERING since NONRENDERED nonfresh nonempty traversed"
                            if self.verbose_enable:
                                theoretical_path = self.get_chunk_image_path(chunky_x, chunky_z)
                                print (min_indent+chunk_luid+": "+result[1])
                                print (min_indent+"  {dest_png_path:"+theoretical_path+"}")
                #end if marked
                else:
                    is_render_needed = True
                    result[1] = "RENDERING since nonfresh unmarked traversed"
                    if self.verbose_enable:
                        print (min_indent+chunk_luid+": "+result[1])
                    #else:
                        #sys.stdout.write('.')
            #end if traversed
            else:
                if (self.is_chunk_yaml_marked(chunky_x, chunky_z)):
                    if (self.is_chunk_yaml_marked_empty(chunky_x, chunky_z)):
                        result[1] = "SKIPPING since nonfresh empty nontraversed"
                        if self.verbose_enable:
                            print (min_indent+chunk_luid+": "+result[1])
                    else:
                        if (self.is_chunk_rendered_on_dest(chunky_x, chunky_z)):
                            result[1] = "SKIPPING since RENDERED nonfresh nonempty nontraversed (delete png to re-render)"
                            if self.verbose_enable:
                               print (min_indent+chunk_luid+":"+result[1])
                        else:
                            is_render_needed = True
                            theoretical_path = self.get_chunk_image_path(chunky_x, chunky_z)
                            result[1] = "RENDERING since NONRENDRERED nonfresh nonempty nontraversed"
                            if self.verbose_enable:
                                print (min_indent+chunk_luid+": "+result[1])
                                print (min_indent+"  {dest_png_path:"+theoretical_path+"}")
                else:
                    is_render_needed = True
                    result[1] = "RENDERING since nonfresh unmarked nontraversed"
                    if self.verbose_enable:
                        print (min_indent+chunk_luid+": "+result[1])
                    #else:
                        #sys.stdout.write('.')
        else:
            result[1] = "SKIPPING since RENDERED fresh"
            if self.verbose_enable:
                print (min_indent+chunk_luid+": "+result[1]+" (rendered after starting "+__file__+")")
            #if (not self.is_chunk_yaml_marked(chunky_x, chunky_z)):
                #is_render_needed = True

        # This should never happen since keeping the output of minetestmapper-numpy.py (after analyzing that output) is deprecated:
        #if self.is_genresult_marked(chunk_luid) and not self.is_chunk_yaml_present(chunky_x, chunky_z):
        #    tmp_chunk = MTChunk()
        #    tmp_chunk.luid = chunk_luid
        #    genresult_path = self.get_chunk_genresult_tmp_path(chunky_x, chunky_z)
        #    tmp_chunk.set_from_genresult(genresult_path)
        #    chunk_yaml_path = self.get_chunk_yaml_path(chunky_x, chunky_z)
        #    self.create_chunk_folder(chunky_x, chunky_z)
        #    tmp_chunk.save_yaml(chunk_yaml_path)
        #    print(min_indent+"(saved yaml to '"+chunk_yaml_path+"')")


        if is_render_needed:
            self.rendered_count += 1
            if not self.verbose_enable:
                print(min_indent+chunk_luid+": "+result[1])
            if (self._render_chunk(chunky_x, chunky_z)):
                result[0] = True
        else:
            if self.is_chunk_rendered_on_dest(chunky_x, chunky_z):
                result[0] = True
                tmp_png_path = self.get_chunk_image_path(chunky_x, chunky_z)
                #NOTE: do NOT set result[1] since specific reason was already set above
                if self.verbose_enable:
                    print(min_indent+chunk_luid+": Skipping existing map tile file " + tmp_png_path + " (delete it to re-render)")
            #elif is_empty_chunk:
                #print("Skipping empty chunk " + chunk_luid)
            #else:
                #print(min_indent+chunk_luid+": Not rendered on dest.")
        return result

    def _check_map_pseudorecursion_branchfrom(self, chunky_x, chunky_z):
        chunk_luid = self.get_chunk_luid(chunky_x, chunky_z)
        branched_pos = chunky_x-1, chunky_z
        #only add if not in list already, to prevent infinite re-branching
        if branched_pos not in self.todo_positions:
            self.todo_positions.append(branched_pos)
        branched_pos = chunky_x+1, chunky_z
        if branched_pos not in self.todo_positions:
            self.todo_positions.append(branched_pos)
        branched_pos = chunky_x, chunky_z-1
        if branched_pos not in self.todo_positions:
            self.todo_positions.append(branched_pos)
        branched_pos = chunky_x, chunky_z+1
        if branched_pos not in self.todo_positions:
            self.todo_positions.append(branched_pos)

    def check_map_pseudorecursion_iterate(self):  # , redo_empty_enable=False):
        min_indent = ""
        if self.todo_index<0:
            self.check_map_pseudorecursion_start()
            if self.verbose_enable:
                print(min_indent+"(initialized "+str(len(self.todo_positions))+" branche(s))")
        if self.todo_index>=0:
            if self.todo_index<len(self.todo_positions):
                this_pos = self.todo_positions[self.todo_index]
                chunky_x, chunky_z = this_pos
                chunk_luid = self.get_chunk_luid(chunky_x, chunky_z)
                prev_total_newly_rendered = self.total_newly_rendered
                is_present, reason_string = self.check_chunk(chunky_x, chunky_z)

                if is_present:
                    self.mapvars["total_generated_count"] += 1
                    if chunky_x<self.mapvars["chunkx_min"]:
                        self.mapvars["chunkx_min"]=chunky_x
                    if chunky_x>self.mapvars["chunkx_max"]:
                        self.mapvars["chunkx_max"]=chunky_x
                    if chunky_z<self.mapvars["chunkz_min"]:
                        self.mapvars["chunkz_min"]=chunky_z
                    if chunky_z>self.mapvars["chunkz_max"]:
                        self.mapvars["chunkz_max"]=chunky_z
                    #end while square outline (1-chunk-thick outline) generated any png files
                    self.save_mapvars_if_changed()
                    prev_len = len(self.todo_positions)
                    self._check_map_pseudorecursion_branchfrom(chunky_x, chunky_z)
                    #must check_decachunk_containing_chunk AFTER _check_map_pseudorecursion_branchfrom so check_decachunk_containing_chunk can see if there are more to do before rendering superchunk
                    if self.total_newly_rendered>prev_total_newly_rendered:
                        self.check_decachunk_containing_chunk(chunky_x, chunky_z)
                    if self.verbose_enable:
                        print(min_indent+"["+str(self.todo_index)+"] branching from "+str((chunky_x, chunky_z))+" (added "+str(len(self.todo_positions)-prev_len)+")")
                else:
                    if self.verbose_enable:
                        print(min_indent+"["+str(self.todo_index)+"] not branching from "+str((chunky_x, chunky_z)))
                self.todo_index += 1
            if self.todo_index>=len(self.todo_positions):  # check again since may have branched above, making this untrue
                self.save_mapvars_if_changed()
                self.todo_index = -1
        else:
            if self.verbose_enable:
                print(min_indent+"(no branches)")

    def get_coords_from_luid(self,chunk_luid):
        result = None
        if chunk_luid is not None:
            xopener_index = chunk_luid.find("x")
            zopener_index = chunk_luid.find("z")
            if xopener_index>=0 and zopener_index>xopener_index:
                x_string = chunk_luid[xopener_index+1:zopener_index]
                z_string = chunk_luid[zopener_index+1:]
                try:
                    chunky_x = int(x_string)
                    try:
                        chunky_z = int(z_string)
                        result = chunky_x, chunky_z
                    except:
                        pass
                except:
                    pass
        return result
    
    def apply_auto_tags_by_worldgen_mods(self, chunky_x, chunky_z):
        worldgen_mod_list = list()
        worldgen_mod_list.append("technic_worldgen")
        worldgen_mod_list.append("mg")
        worldgen_mod_list.append("moreores")
        worldgen_mod_list.append("lapis")
        worldgen_mod_list.append("sea")
        worldgen_mod_list.append("moretrees")
        worldgen_mod_list.append("caverealms")
        #worldgen_mod_list.append("nature_classic")  # NOTE: plantlife_modpack has this and other stuff, but just mention this one in tags since it is unique to the modpack
        worldgen_mod_list.append("plantlife_modpack")  #ok if installed as modpack instead of putting individual mods in mods folder
        
        chunk_luid = self.get_chunk_luid(chunky_x, chunky_z)
        if chunk_luid not in self.chunks.keys():
            self.prepare_chunk_meta(chunky_x, chunky_z)
        auto_tags_string=""
        existing_tags_string=""
        tags_list = None
        if ("tags" in self.chunks[chunk_luid].metadata) and (self.chunks[chunk_luid].metadata["tags"] is not None):
            existing_tags_string=self.chunks[chunk_luid].metadata["tags"]
            tags_list=existing_tags_string.split(",")
            for index in range(0,len(tags_list)):
                tags_list[index]=tags_list[index].strip()
        else:
            tags_list = list()
        #TODO: finish this
        #for mod_name in worldgen_mod_list:
            #mod_path = self.asdf
            #if os.path.isdir( 
        #if is_changed:
        #    self.save_chunk_meta(chunky_x, chunky_z)
    
    def correct_genresults_paths(self):
        count = 0
        folder_path = self.get_chunk_genresults_base_path()
        #for base_path, dirnames, filenames in os.walk(folder_path):
        for file_name in os.listdir(folder_path):
            #for file_name in filenames:
            file_path = os.path.join(folder_path,file_name)
            if os.path.isfile(file_path):
                #print ("  EXAMINING "+file_name)
                #badstart_string = "."
                player_name = None
                player_position = None
                #if (file_name[:len(badstart_string)]!=badstart_string):
                if (file_name[:1]!="."):
                    if len(file_name)>=len(self.genresult_name_opener_string)+4+len(self.genresult_name_closer_string):
                        chunk_luid = self.get_chunk_luid_from_genresult_name(file_name)
                        coords = self.get_coords_from_luid(chunk_luid)
                        if coords is not None:
                            chunky_x, chunky_z = coords
                            corrected_folder_path = self.get_chunk_genresult_tmp_folder(chunky_x, chunky_z)
                            if not os.path.isdir(corrected_folder_path):
                                print("    creating \""+corrected_folder_path+"\"")
                                os.makedirs(corrected_folder_path)
                            #corrected_file_path = os.path.join(corrected_folder_path, file_name)
                            corrected_file_path = self.get_chunk_genresult_tmp_path(chunky_x, chunky_z)
                            if os.path.isfile(corrected_file_path):
                                os.remove(corrected_file_path)
                            try:
                                os.rename(file_path, corrected_file_path)
                            except:
                                #TODO: why does this happen (file does not exist)???
                                print("    Could not finish moving \""+file_path+"\" to \""+corrected_file_path+"\"")

                            count += 1
                        else:
                            print("WARNING: found unusable genresults file '"+file_name+"' in ")
        if count>0:
            print("")
            print("MOVED "+str(count)+" genresult file(s)")
            print("")
            print("")
        

    def check_map_pseudorecursion_start(self):
        if self.todo_index<0:
            print("PROCESSING MAP DATA (BRANCH PATTERN)")
            if os.path.isfile(self.minetestmapper_py_path) and os.path.isfile(self.colors_path):
                self.rendered_count = 0
                self.todo_positions = list()
                self.todo_positions.append((0,0))
                #self.mapvars = get_dict_from_conf_file(self.world_yaml_path,":")
                self.verify_correct_map()
                decachunk_luid_list = list()
                if self.preload_all_enable:
                    self.preload_all_enable = False
                    self.correct_genresults_paths()
                    minlen=len(self.chunk_yaml_name_opener_string)+4+len(self.chunk_yaml_name_dotext_string)  # +4 for luid, such as x1z2 (ok since just a minimum)
                    #for base_path, dirnames, filenames in os.walk(self.data_16px_path):
                        #for dirname in dirnames:
                    #for decachunk_x_basepath, decachunk_x_dirnames, decachunk_x_filenames in os.walk(self.data_16px_path):
                    for decachunk_x_name in os.listdir(self.data_16px_path):
                        decachunk_x_path = os.path.join(self.data_16px_path, decachunk_x_name)
                        #for decachunk_z_basepath, decachunk_z_dirnames, decachunk_z_filenames in os.walk(decachunk_x_dirnames):
                        if decachunk_x_path[:1]!="." and os.path.isdir(decachunk_x_path):
                            for decachunk_z_name in os.listdir(decachunk_x_path):
                                decachunk_z_path = os.path.join(decachunk_x_path, decachunk_z_name)
                                if decachunk_z_path[:1]!="." and os.path.isdir(decachunk_z_path):
                                    #for chunk_filename in decachunk_z_filenames:
                                    for chunk_filename in os.listdir(decachunk_z_path):
                                        chunk_path = os.path.join(decachunk_z_path, chunk_filename)
                                        #file_path = os.path.join(self.chunkymap_thisworld_data_path,file_name)
                                        if chunk_filename[:1]!="." and os.path.isfile(chunk_path):
                                            #print ("  EXAMINING "+file_name)
                                            #badstart_string = "."
                                            #if (file_name[:len(badstart_string)]!=badstart_string):
                                            if len(chunk_filename) > minlen:
                                                chunk_luid = self.get_chunk_luid_from_yaml_name(chunk_filename)
                                                coords = self.get_coords_from_luid(chunk_luid)
                                                if coords is not None:
                                                    chunky_x, chunky_z = coords
                                                    decachunk_luid = self.get_decachunk_luid_from_chunk(chunky_x, chunky_z)
                                                    if decachunk_luid not in decachunk_luid_list:
                                                        decachunk_luid_list.append(decachunk_luid)
                                                    if "chunk_size" not in self.mapvars:
                                                        print("ERROR: '"+chunk_luid+"' has missing mapvars among {"+str(self.mapvars)+"}")
                                                        break
                                                    print("Checking chunk "+str(coords)+" *"+str(self.mapvars["chunk_size"])+"")
                                                    self.prepare_chunk_meta(chunky_x, chunky_z)
                                                    
                                                    #if ("tags" not in self.chunks[chunk_luid].metadata):
                                                        #self.chunks[chunk_luid].metadata["tags"] = "moreores,caverealms"
                                                        #self.save_chunk_meta(chunky_x, chunky_z)
                                                        #print("  saved tags to '"+chunk_path+"'")
                    for decachunk_luid in decachunk_luid_list:
                        coords = self.get_coords_from_luid(decachunk_luid)
                        if coords is not None:
                            decachunky_x, decachunky_z = coords
                            chunky_x = decachunky_x*10
                            chunky_z = decachunky_z*10
                            if not os.path.isfile(self.get_decachunk_image_path_from_chunk(chunky_x, chunky_z)):
                                self.check_decachunk_containing_chunk(chunky_x, chunky_z)
                        else:
                            print("ERROR: could not get coords from decachunk luid "+decachunk_luid)
                for chunk_luid in self.chunks.keys():
                    coords = self.get_coords_from_luid(chunk_luid)
                    if coords is not None:
                        chunky_x, chunky_z = coords
                        if self.chunks[chunk_luid].metadata["is_traversed"] and not self.is_chunk_rendered_on_dest(chunky_x, chunky_z):
                            if self.chunks[chunk_luid].metadata["is_empty"]:
                                self.chunks[chunk_luid].metadata["is_empty"] = False
                                self.save_chunk_meta(chunky_x, chunky_z)
                            #if coords is not None:
                            self.todo_positions.append(coords)
                            #ins = open(file_path, 'r')
                            #line = True
                            #while line:
                                #line = ins.readline()
                                #if line:
                            #ins.close()
                    else:
                        print("ERROR: could not get coords from luid '"+chunk_luid+"'")
                self.todo_index = 0
                #while (todo_index<len(self.todo_positions)):
                self.verify_correct_map()

    def verify_correct_map(self):
        #NOTE: NO LONGER NEEDED since each world has its own folder in chunkymapdata/worlds folder
        pass
        #if os.path.isfile(self.minetestmapper_py_path) and os.path.isfile(self.colors_path):
            #if self.mapvars is not None and set(['world_name']).issubset(self.mapvars):
                ##if self.verbose_enable:
                ##    print ("  (FOUND self.config["world_name"])")
                #if self.config["world_name"] != self.config["world_name"]:
                    #print("")
                    #print("")
                    #print("")
                    #print("")
                    #print("")
                    #print ("Removing ALL map data since from WORLD NAME is different (map '"+str(self.config["world_name"])+"' is not '"+str(self.config["world_name"])+"')...")
                    #print("")
                    #if os.path.isdir(self.chunkymap_thisworld_data_path):
                        #for base_path, dirnames, filenames in os.walk(self.chunkymap_thisworld_data_path):
                            #for file_name in filenames:
                                #if file_name[0] != ".":
                                    #file_path = os.path.join(self.chunkymap_thisworld_data_path,file_name)
                                    #if self.verbose_enable:
                                        #print ("  EXAMINING "+file_name)
                                    #badstart_string = "chunk"
                                    #if (len(file_name) >= len(badstart_string)) and (file_name[:len(badstart_string)]==badstart_string):
                                        #os.remove(file_path)
                                    #elif file_name==self.yaml_name:
                                        #os.remove(file_path)
                    #players_path = os.path.join(self.chunkymap_thisworld_data_path, "players")
                    #if os.path.isdir(players_path):
                        #for base_path, dirnames, filenames in os.walk(players_path):
                            #for file_name in filenames:
                                #if file_name[0] != ".":
                                    #file_path = os.path.join(self.chunkymap_thisworld_data_path,file_name)
                                    #if self.verbose_enable:
                                        #print ("  EXAMINING "+file_name)
                                    #badend_string = ".yml"
                                    #if (len(file_name) >= len(badend_string)) and (file_name[len(file_name)-len(badend_string):]==badend_string):
                                        #os.remove(file_path)
                    #self.mapvars["chunkx_min"]=0
                    #self.mapvars["chunkx_max"]=0
                    #self.mapvars["chunkz_min"]=0
                    #self.mapvars["chunkz_max"]=0
                    #self.save_mapvars_if_changed()
                    ##do not neet to run self.save_mapvars_if_changed() since already removed the yml

    def save_mapvars_if_changed(self):
        is_changed = False
        #is_different_world = False
        if self.saved_mapvars is None:
            print ("SAVING '" + self.world_yaml_path + "' since nothing was loaded or it did not exist")
            is_changed = True
        else:
            for this_key in self.mapvars.iterkeys():
                if this_key != "total_generated_count":  # don't care if generated count changed since may have been regenerated
                    if (this_key not in self.saved_mapvars.keys()):
                        is_changed = True
                        print ("SAVING '" + self.world_yaml_path + "' since " + str(this_key) + " not in saved_mapvars")
                        break
                    elif (str(self.saved_mapvars[this_key]) != str(self.mapvars[this_key])):
                        is_changed = True
                        print ("SAVING '" + self.world_yaml_path + "' since new " + this_key + " value " + str(self.mapvars[this_key]) + " not same as saved value " + str(self.saved_mapvars[this_key]) + "")
                        break
        if is_changed:
            save_conf_from_dict(self.world_yaml_path,self.mapvars,":")
            self.saved_mapvars = get_dict_from_conf_file(self.world_yaml_path,":")
            #self.mapvars = get_dict_from_conf_file(self.world_yaml_path,":")
        else:
            if self.verbose_enable:
                print ("  (Not saving '"+self.world_yaml_path+"' since same value of each current variable is already in file as loaded)")

    def check_map_inefficient_squarepattern(self):
        if os.path.isfile(self.minetestmapper_py_path) and os.path.isfile(self.colors_path):
            self.rendered_count = 0


            self.mapvars = get_dict_from_conf_file(self.world_yaml_path,":")


            self.verify_correct_map()

            self.mapvars["chunkx_min"] = 0
            self.mapvars["chunkz_min"] = 0
            self.mapvars["chunkx_max"] = 0
            self.mapvars["chunkz_max"] = 0
            if self.saved_mapvars is not None:
                if "chunkx_min" in self.saved_mapvars.keys():
                    self.mapvars["chunkx_min"] = self.saved_mapvars["chunkx_min"]
                if "chunkx_max" in self.saved_mapvars.keys():
                    self.mapvars["chunkx_max"] = self.saved_mapvars["chunkx_max"]
                if "chunkz_min" in self.saved_mapvars.keys():
                    self.mapvars["chunkz_min"] = self.saved_mapvars["chunkz_min"]
                if "chunkz_max" in self.saved_mapvars.keys():
                    self.mapvars["chunkz_max"] = self.saved_mapvars["chunkz_max"]

            self.mapvars["total_generated_count"] = 0

            newchunk_luid_list = list()
            this_iteration_generates_count = 1
            #if str(self.config["world_name"]) != str(self.config["world_name"]):
            #    is_different_world = True
            #    print("FULL RENDER since chosen world name '"+self.config["world_name"]+"' does not match previously rendered world name '"+self.config["world_name"]+"'")
            print("PROCESSING MAP DATA (SQUARE)")
            while this_iteration_generates_count > 0:
                this_iteration_generates_count = 0
                self.read_then_remove_signals()
                if not self.refresh_map_enable:
                    break
                for chunky_z in range (self.mapvars["chunkz_min"],self.mapvars["chunkz_max"]+1):
                    self.read_then_remove_signals()
                    if not self.refresh_map_enable:
                        break
                    for chunky_x in range(self.mapvars["chunkx_min"],self.mapvars["chunkx_max"]+1):
                        self.read_then_remove_signals()
                        if not self.refresh_map_enable:
                            break
                        #python ~/minetest/util/minetestmapper-numpy.py --region -1200 800 -1200 800 --drawscale --maxheight 100 --minheight -50 --pixelspernode 1 ~/.minetest/worlds/FCAGameAWorld ~/map.png
                        #sudo mv ~/map.png /var/www/html/minetest/images/map.png

                        #only generate the edges (since started with region 0 0 0 0) and expanding from there until no png is created:
                        is_outline = (chunky_x==self.mapvars["chunkx_min"]) or (chunky_x==self.mapvars["chunkx_max"]) or (chunky_z==self.mapvars["chunkz_min"]) or (chunky_z==self.mapvars["chunkz_max"])
                        if is_outline:
                            is_present, reason_string = self.check_chunk(chunky_x, chunky_z)
                            if is_present:
                                this_iteration_generates_count += 1
                                self.mapvars["total_generated_count"] += 1
                    if self.verbose_enable:
                        print ("")  # blank line before next chunky_z so output is more readable
                self.mapvars["chunkx_min"] -= 1
                self.mapvars["chunkz_min"] -= 1
                self.mapvars["chunkx_max"] += 1
                self.mapvars["chunkz_max"] += 1
            #end while square outline (1-chunk-thick outline) generated any png files
            self.save_mapvars_if_changed()
            if not self.verbose_enable:
                print("  rendered: "+str(self.rendered_count)+" (only checks for new chunks)")
        else:
            print ("MAP ERROR: failed since this folder must contain colors.txt and minetestmapper-numpy.py")

    def read_then_remove_signals(self):
        signal_path = self.get_signal_path()
        if os.path.isfile(signal_path):
            signals = get_dict_from_conf_file(signal_path,":")
            if signals is not None:
                print("ANALYZING "+str(len(signals))+" signal(s)")
                for this_key in signals.keys():
                    is_signal_ok = True
                    if this_key=="loop_enable":
                        if not signals[this_key]:
                            self.loop_enable = False
                        else:
                            is_signal_ok = False
                            print("WARNING: Got signal to change loop_enable to True, so doing nothing")
                    elif this_key=="refresh_players_enable":
                        if type(signals[this_key]) is bool:
                            self.refresh_players_enable = signals[this_key]
                        else:
                            is_signal_ok = False
                            print("ERROR: expected bool for "+this_key)
                    elif this_key=="refresh_map_seconds":
                        if (type(signals[this_key]) is float) or (type(signals[this_key]) is int):
                            if float(signals[this_key])>=1.0:
                                self.refresh_map_seconds = float(signals[this_key])
                            else:
                                is_signal_ok = False
                                print("ERROR: expected >=1 seconds for refresh_map_seconds (int or float)")
                        else:
                            is_signal_ok = False
                            print("ERROR: expected int for "+this_key)
                    elif this_key=="refresh_players_seconds":
                        if (type(signals[this_key]) is float) or (type(signals[this_key]) is int):
                            if float(signals[this_key])>=1.0:
                                self.refresh_players_seconds = float(signals[this_key])
                            else:
                                print("ERROR: expected >=1 seconds for refresh_players_seconds (int or float)")
                        else:
                            is_signal_ok = False
                            print("ERROR: expected int for "+this_key)
                    elif this_key=="recheck_rendered":
                        if type(signals[this_key]) is bool:
                            if signals[this_key]:
                                for chunk_luid in self.chunks.keys():
                                    self.chunks[chunk_luid].is_fresh = False
                        else:
                            is_signal_ok = False
                            print("ERROR: expected bool for "+this_key)
                    elif this_key=="refresh_map_enable":
                        if type(signals[this_key]) is bool:
                            self.refresh_map_enable = signals[this_key]
                        else:
                            is_signal_ok = False
                            print("ERROR: expected bool for "+this_key)
                    elif this_key=="verbose_enable":
                        if type(signals[this_key]) is bool:
                            self.verbose_enable = signals[this_key]
                        else:
                            is_signal_ok = False
                            print("ERROR: expected true or false after colon for "+this_key)

                    else:
                        is_signal_ok = False
                        print("ERROR: unknown signal '"+this_key+"'")
                    if is_signal_ok:
                        print("RECEIVED SIGNAL "+str(this_key)+":"+str(signals[this_key]))
            else:
                print("WARNING: blank '"+signal_path+"'")
            try:
                os.remove(signal_path)
            except:
                print("ERROR: "+__file__+" must have permission to remove '"+signal_path+"'. Commands will be repeated unless command was loop_enable:false.")  # so exiting to avoid inability to avoid repeating commands at next launch.")
                #self.loop_enable = False

    def run_loop(self):
        #self.last_run_second = best_timer()
        self.loop_enable = True
        self.verbose_enable = False
        is_first_iteration = True
        while self.loop_enable:
            before_second = best_timer()
            run_wait_seconds = self.refresh_map_seconds
            if self.refresh_players_seconds < run_wait_seconds:
                run_wait_seconds = self.refresh_players_seconds
            print("")
            print("Ran "+str(self.run_count)+" time(s)")
            self.read_then_remove_signals()
            if self.loop_enable:
                if self.refresh_players_enable:
                    if self.last_players_refresh_second is None or (best_timer()-self.last_players_refresh_second > self.refresh_players_seconds ):
                        #if self.last_players_refresh_second is not None:
                            #print ("waited "+str(best_timer()-self.last_players_refresh_second)+"s for map update")
                        self.last_players_refresh_second = best_timer()
                        self.check_players()
                    else:
                        print("waiting before doing player update")
                else:
                    print("player update is not enabled")
                if self.refresh_map_enable:
                    is_first_run = True
                    map_render_latency = 0.3
                    is_done_iterating = self.todo_index<0
                    if (not is_first_iteration) or (self.last_map_refresh_second is None) or (best_timer()-self.last_map_refresh_second > self.refresh_map_seconds) or (not is_done_iterating):
                        while is_first_run or ( ((best_timer()+map_render_latency)-self.last_players_refresh_second) < self.refresh_players_seconds ):
                            self.read_then_remove_signals()
                            if not self.refresh_map_enable:
                                break
                            is_first_run = False
                            is_first_iteration = self.todo_index<0
                            #if (self.last_map_refresh_second is None) or (best_timer()-self.last_map_refresh_second > self.refresh_map_seconds):
                            #if self.last_map_refresh_second is not None:
                                #print ("waited "+str(best_timer()-self.last_map_refresh_second)+"s for map update")
                            self.last_map_refresh_second = best_timer()
                            self.check_map_pseudorecursion_iterate()
                            if self.todo_index<0:  # if done iterating
                                break
                            map_render_latency = best_timer() - self.last_map_refresh_second
                            #self.check_map_inefficient_squarepattern()
                    else:
                        print("waiting before doing map update")
                else:
                    print("map update is not enabled")
                run_wait_seconds -= (best_timer()-before_second)
                is_done_iterating = self.todo_index<0
                if ( (float(run_wait_seconds)>0.0) and (is_done_iterating)):
                    print ("sleeping for "+str(run_wait_seconds)+"s")
                    time.sleep(run_wait_seconds)
                self.run_count += 1
            else:
                self.verbose_enable = True

    def run(self):
        if self.refresh_players_enable:
            self.check_players()
        if self.refresh_map_enable:
            self.check_map_inefficient_squarepattern()
            #self.check_map_pseudorecursion_iterate()

if __name__ == '__main__':
    mtchunks = MTChunks()
    signal_path = mtchunks.get_signal_path()
    stop_line = "loop_enable:False"
    parser = argparse.ArgumentParser(description='A mapper for minetest')
    parser.add_argument('--skip-map', type = bool, metavar = ('skip_map'), default = False, help = 'draw map tiles and save YAML files for chunkymap.php to use')
    parser.add_argument('--skip-players', type = bool, metavar = ('skip_players'), default = False, help = 'update player YAML files for chunkymap.php to use')
    parser.add_argument('--no-loop', type = bool, metavar = ('no_loop'), default = False, help = 'keep running until "'+signal_path+'" contains the line '+stop_line)
    args = parser.parse_args()

    if not args.skip_players:
        if not args.skip_map:
            print("Drawing players and map")
        else:
            mtchunks.refresh_map_enable = False
            print("Drawing players only")
    else:
        if not args.skip_map:
            mtchunks.refresh_players_enable = False
            print("Drawing map only")
        else:
            mtchunks.refresh_players_enable = False
            mtchunks.refresh_map_enable = False
            print("Nothing to do since "+str(args))
    if mtchunks.refresh_players_enable or mtchunks.refresh_map_enable:
        if args.no_loop:
            mtchunks.run()
        else:
            print("To stop chunkymap-regen loop, save a line '"+stop_line+"' to '"+signal_path+"'")
            mtchunks.run_loop()
