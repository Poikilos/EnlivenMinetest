#!/usr/bin/env python2
import os
import subprocess
import traceback
import argparse
import time
import sys
import timeit
from timeit import default_timer as best_timer

#best_timer = timeit.default_timer
#if sys.platform == "win32":
    # on Windows, the best timer is time.clock()
#    best_timer = time.clock
#else:
    # on most other platforms, the best timer is time.time()
#    best_timer = time.time
# REQUIRES: see README.md
# The way to do a full render is deleting all files from the folder self.chunkymap_data_path such as /var/www/html/minetest/chunkymapdata (or chunkymap in current directory on Windows)

#minetestmapper-numpy.py calculates the region as follows:
#(XMIN','XMAX','ZMIN','ZMAX'), default = (-2000,2000,-2000,2000)
#sector_xmin,sector_xmax,sector_zmin,sector_zmax = numpy.array(args.region)/16
#sector_ymin = args.self.minheight/16
#sector_ymax = args.self.maxheight/16
#region server-specific options

#as per http://interactivepython.org/runestone/static/pythonds/BasicDS/ImplementingaQueueinPython.html
class SimpleQueue:
    def __init__(self):
        self.items = []

    def isEmpty(self):
        return self.items == []

    def enqueue(self, item):
        self.items.insert(0,item)

    def dequeue(self):
        return self.items.pop()

    def size(self):
        return len(self.items)

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

def get_dict_modified_by_conf_file(this_dict, path,assignment_operator="="):
    results = None
    #print ("Checking "+str(path)+" for settings...")
    if os.path.isfile(path):
        results = this_dict
        if (results is None) or (type(results) is not dict):
            results = {}
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



class MTChunk:
    x = None
    z = None
    metadata = None
    is_fresh = None
    luid = None
    #width = None
    #height = None
    #is_marked = None
    #is_empty = None
    #image_w = None
    #image_h = None
    #image_left = None
    #image_top = None
    #image_right = None
    #image_bottom = None

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

    def load_yaml(self, yml_path):
        self.metadata = get_dict_modified_by_conf_file(self.metadata,yml_path,":")

    def save_yaml(self, yml_path):
        save_conf_from_dict(yml_path, self.metadata, assignment_operator=":", save_nulls_enable=False)
        #try:
            #outs = open(yml_path, 'w')
            #outs.write("is_empty:"+str(self.is_empty)+"\n")
            #outs.write("is_marked:"+str(self.is_marked)+"\n")
            #if self.width is not None:
                #outs.write("width:"+str(self.width)+"\n")
            #if self.height is not None:
                #outs.write("height:"+str(self.height)+"\n")
            #if self.image_w is not None:
                #outs.write("image_w:"+str(self.image_w)+"\n")
            #if self.image_h is not None:
                #outs.write("image_h:"+str(self.image_h)+"\n")
            #if self.image_left is not None:
                #outs.write("image_left:"+str(self.image_left)+"\n")
            #if self.image_top is not None:
                #outs.write("image_top:"+str(self.image_top)+"\n")
            #if self.image_right is not None:
                #outs.write("image_right:"+str(self.image_right)+"\n")
            #if self.image_bottom is not None:
                #outs.write("image_bottom:"+str(self.image_bottom)+"\n")
            #outs.close()
        #except:
            #print("Could not finish saving chunk metadata to '"+str(yml_path)+"': "+str(traceback.format_exc()))

    #requires output such as from minetestmapper-numpy.py
    def set_from_genresult(self, this_genresult_path):
        #this_genresult_path = mtchunks.get_chunk_genresult_path(chunk_luid)
        result = False
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


class MTChunks:

    website_root = None
    username = None
    os_name = None
    chunkymap_data_path = None
    profiles_path = None
    profile_path = None
    worlds_path = None
    is_save_output_ok = None
    mt_util_path = None
    minetestmapper_fast_sqlite_path = None
    minetestmapper_custom_path = None
    minetestmapper_py_path = None
    colors_path = None
    python_exe_path = None
    chunks = None

    #region values to save to YAML
    world_name = None
    world_path = None
    chunkx_min = 0
    chunkz_min = 0
    chunkx_max = 0
    chunkz_max = 0
    chunk_size = None
    #values for command arguments:
    maxheight = 50
    minheight = -25
    pixelspernode = 1
    refresh_map_enable = None
    refresh_players_enable = None
    refresh_map_seconds = None
    refresh_players_seconds = None
    last_players_refresh_second = None
    last_map_refresh_second = None
    #ALSO save to YAML:
    total_generated_count = None
    #endregion values to save to YAML

    loop_enable = None
    verbose_enable = None

    world_blacklist = None
    run_count = None
    todo_positions = None  # list of tuples (locations) to render next (for fake recursion)
    todo_index = None
    yaml_name = None
    world_yaml_path = None
    chunkymap_data_path = None
    preload_all_enable = None
    chunk_yaml_name_opener_string = None
    chunk_yaml_name_dotext_string = None
    mapvars = None
    rendered_count = None
    backend_string = None
    #region_separators = None
    is_backend_detected = None

    def __init__(self):  #formerly checkpaths() in global scope
        self.is_backend_detected = False
        self.total_generated_count = 0
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
        #self.username = "owner"
        self.website_root="/var/www/html/minetest"
        self.world_name = "FCAGameAWorld"
        self.os_name="linux"
        self.refresh_map_seconds = 30 #does one chunk at a time so as not to interrupt player updates too often
        self.refresh_players_seconds = 5
        self.chunk_yaml_name_opener_string = "chunk_"
        self.chunk_yaml_name_dotext_string = ".yml"
        #self.region_separators = [" "," "," "]

        input_string = ""
        if (os.path.sep!="/"):
            self.os_name="windows"
            print("Windows detected")
        #input_string = input("Which self.username contains minetest/util/minetestmapper-numpy.py (minetest not .minetest) ["+self.username+"]?")
        if (len(input_string)>0):
            self.username = input_string

        #input_string = input("What is the root folder of your minetest website ["+self.website_root+"]?")
        if (len(input_string)>0):
            self.website_root = input_string

        #input_string = input("What is the game name ["+self.world_name+"]")
        if (len(input_string)>0):
            self.world_name = input_string
        #region server-specific options
        self.profiles_path = "/home"
        if self.os_name=="windows":
            self.profiles_path = "C:\\Users"
        if self.username is not None:
            self.profile_path = os.path.join(self.profiles_path, self.username)
        else:
            if self.os_name=="windows":
                self.profiles_path = "C:\\Users"
                self.profile_path = os.environ['USERPROFILE']
            else:
                self.profile_path = os.environ['HOME']

        #if (not os.path.isdir(self.profile_path)):
        #    self.profile_path = os.path.join(self.profiles_path, "jgustafson")
        self.dotminetest_path = os.path.join(self.profile_path,".minetest")
        if (self.os_name=="windows"):
            self.dotminetest_path = "C:\\games\\Minetest"
        print("Using dotminetest_path '"+self.dotminetest_path+"'")
        self.worlds_path = os.path.join(self.dotminetest_path,"worlds")
        self.world_path = os.path.join(self.worlds_path, self.world_name)
        
        auto_chosen_world = False
        self.world_blacklist = list()
        self.world_blacklist.append("CarbonUnit")
        #self.world_blacklist.append("abiyahhgamebv7world1")
        if not os.path.isdir(self.world_path):
            #for item in os.walk(self.worlds_path):
            print ("LOOKING FOR WORLDS IN " + self.worlds_path)
            for dirname, dirnames, filenames in os.walk(self.worlds_path):
                #index = 0
                #for j in range(0,len(dirnames)):
                #    i = len(dirnames) - 0 - 1
                #    if dirnames[i][0] == ".":
                #        print ("  SKIPPING "+dirnames[i])
                #        dirnames.remove_at(i)
                for subdirname in dirnames:
                    print ("  EXAMINING "+subdirname)
                    if subdirname[0]!=".":
                        #if (index == len(dirnames)-1):  # skip first one because the one on my computer is big
                        if subdirname not in self.world_blacklist:
                            self.world_name = subdirname
                            self.world_path = os.path.join(dirname, subdirname) #  os.path.join(self.worlds_path, "try7amber")
                            print ("  CHOSE "+self.world_path)
                            auto_chosen_world = True
                            break
                        #index += 1
                if auto_chosen_world:
                    break
        self.python_exe_path = "python"
        worldmt_path = os.path.join(self.world_path, "world.mt")
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
        self.is_save_output_ok = True   # Keeping output after analyzing it is no longer necessary since results are saved to YAML, but keeping output provides debug info since is the output of minetestmapper-numpy.py
        if self.is_backend_detected:
            print("Detected backend '"+self.backend_string+"' from '"+worldmt_path+"'")
        else:
            print("WARNING: Database backend cannot be detected (unable to ensure image generator script will render map)")
        try:
            alt_path = "C:\\python27\python.exe"
            if os.path.isfile(alt_path):
                self.python_exe_path = alt_path
            #else may be in path--assume installer worked
        except:
            pass  # do nothing, probably linux
        mt_path = os.path.join( self.profile_path, "minetest")
        self.mt_util_path = os.path.join( mt_path, "util")
        self.minetestmapper_fast_sqlite_path = os.path.join( self.mt_util_path, "minetestmapper-numpy.py" )
        if self.os_name=="windows":
            self.minetestmapper_fast_sqlite_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "minetestmapper-numpy.py")
        
        self.minetestmapper_custom_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "minetestmapper.py")
        self.mt_chunkymap_path = os.path.join(self.mt_util_path, "chunkymap")
        try_path = os.path.join(self.mt_chunkymap_path, "minetestmapper.py")
        if os.path.isfile(try_path):
            self.minetestmapper_custom_path
        self.minetestmapper_py_path = self.minetestmapper_fast_sqlite_path
        if (self.backend_string!="sqlite3"):
            self.minetestmapper_py_path = self.minetestmapper_custom_path
        print("Chose image generator script: "+self.minetestmapper_py_path)
        if not os.path.isfile(self.minetestmapper_py_path):
            print("ERROR: script does not exist, exiting "+__file__+".")
            sys.exit()
        self.colors_path = os.path.join( self.mt_util_path, "colors.txt" )
        if self.os_name=="windows":
            self.colors_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "colors.txt")
            self.website_root = None
            prioritized_try_paths = list()
            prioritized_try_paths.append("C:\\wamp\\www")
            prioritized_try_paths.append("C:\\www")
            prioritized_try_paths.append("C:\\Program Files\\Apache Software Foundation\\Apache2.2\\htdocs")

            #prioritized_try_paths.append("C:\\Program Files\\Apache Software Foundation\\Apache2.2\\htdocs\\folder_test\\website")
            for try_path in prioritized_try_paths:
                try:
                    if os.path.isdir(try_path):
                        self.website_root = try_path
                        break
                except:
                    pass
            if self.website_root is None:
                self.website_root = os.path.dirname(os.path.abspath(__file__))
        print("Set website_root to "+self.website_root)

        self.chunkymap_data_path=os.path.join(self.website_root,"chunkymapdata")
        self.yaml_name = "generated.yml"
        self.world_yaml_path = os.path.join(self.chunkymap_data_path, self.yaml_name)

        self.chunkx_min = 0
        self.chunkz_min = 0
        self.chunkx_max = 0
        self.chunkz_max = 0
        self.mapvars = get_dict_from_conf_file(self.world_yaml_path,":")
        if self.mapvars is not None:
            if "chunkx_min" in self.mapvars.keys():
                self.chunkx_min = self.mapvars["chunkx_min"]
            if "chunkx_max" in self.mapvars.keys():
                self.chunkx_max = self.mapvars["chunkx_max"]
            if "chunkz_min" in self.mapvars.keys():
                self.chunkz_min = self.mapvars["chunkz_min"]
            if "chunkz_max" in self.mapvars.keys():
                self.chunkz_max = self.mapvars["chunkz_max"]

        self.chunk_size = 16
        self.maxheight = 64
        self.minheight = -32
        self.pixelspernode = 1




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


    #locally unique identifier (unique to world only)
    def get_chunk_luid(self, x,z):
        return "x"+str(x)+"z"+str(z)

    def get_chunk_image_name(self, chunk_luid):
        return "chunk_"+chunk_luid+".png"

    def get_chunk_image_tmp_path(self, chunk_luid):
        return os.path.join(os.path.dirname(os.path.abspath(__file__)), self.get_chunk_image_name(chunk_luid))

    def get_signal_name(self):
        return "chunkymap-signals.txt"

    def get_signal_path(self):
        return os.path.join(os.path.dirname(os.path.abspath(__file__)), self.get_signal_name())

    def get_chunk_image_path(self, chunk_luid):
        return os.path.join(self.chunkymap_data_path, self.get_chunk_image_name(chunk_luid))

    def get_chunk_genresult_name(self, chunk_luid):
        return "chunk_"+chunk_luid+"_mapper_result.txt"

    def get_chunk_genresults_tmp_folder(self, chunk_luid):
        return os.path.join(os.path.dirname(os.path.abspath(__file__)), "chunkymap-genresults")

    def get_chunk_genresult_tmp_path(self, chunk_luid):
        return os.path.join(self.get_chunk_genresults_tmp_folder(chunk_luid), self.get_chunk_genresult_name(chunk_luid))

    def get_chunk_luid_from_yaml_name(self, yml_name):
        return yml_name[len(self.chunk_yaml_name_opener_string):-1*len(self.chunk_yaml_name_dotext_string)]

    def get_chunk_yaml_name(self, chunk_luid):
        return self.chunk_yaml_name_opener_string+chunk_luid+self.chunk_yaml_name_dotext_string

    def is_chunk_yaml_present(self, chunk_luid):
        return os.path.isfile(self.get_chunk_yaml_path(chunk_luid))

    def get_chunk_yaml_path(self, chunk_luid):
        return os.path.join(self.chunkymap_data_path, self.get_chunk_yaml_name(chunk_luid))

    def is_chunk_yaml_marked(self, chunk_luid):
        yaml_path = self.get_chunk_yaml_path(chunk_luid)
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

    def is_chunk_yaml_marked_empty(self, chunk_luid):
        yaml_path = self.get_chunk_yaml_path(chunk_luid)
        result = False
        if os.path.isfile(yaml_path):
            ins = open(yaml_path, 'r')
            line = True
            while line:
                line = ins.readline()
                if line:
                    line_strip = line.strip()
                    prevalue_string="is_empty:"
                    if line_strip[:len(prevalue_string)]==prevalue_string:
                        result = bool(line_strip[len(prevalue_string):].strip())
                        break
            ins.close()
        return result

    def remove_chunk_image(self, chunk_luid):
        result = False
        tmp_png_path = self.get_chunk_image_path(chunk_luid)
        if os.path.isfile(tmp_png_path):
            result = True
            os.remove(tmp_png_path)
        return result

    def remove_chunk(self, chunk_luid):
        result = False
        out_path = self.get_chunk_genresult_tmp_path(chunk_luid)
        tmp_png_path = self.get_chunk_image_path(chunk_luid)
        yml_path = self.get_chunk_yaml_path(chunk_luid)
        if os.path.isfile(tmp_png_path):
            os.remove(tmp_png_path)
            result = True
        if os.path.isfile(yml_path):
            os.remove(yml_path)
            result = True
        if os.path.isfile(out_path):
            os.remove(out_path)
            result = True
        return result

    def is_chunk_rendered_on_dest(self, chunk_luid):  #formerly is_chunk_empty_on_dest (reversed)
        is_rendered = False
        dest_png_path = self.get_chunk_image_path(chunk_luid)
        if os.path.isfile(dest_png_path):
            is_rendered = True
        return is_rendered

    def prepare_chunk_meta(self, chunk_luid):
        if chunk_luid not in self.chunks.keys():
            self.chunks[chunk_luid] = MTChunk()
            self.chunks[chunk_luid].luid = chunk_luid
            yaml_path = self.get_chunk_yaml_path(chunk_luid)
            if os.path.isfile(yaml_path):
                self.chunks[chunk_luid].load_yaml(yaml_path)

    def print_file(path, indent=""):
        if os.path.isfile(path):
            if indent is None:
                indent = ""
            try:
                ins = open(path, 'r')
                line = True
                while line:
                    line = ins.readline()
                    if line:
                        print(indent+line)
                ins.close()
            except:
                print(indent+"print_file: could not finish")
        else:
            print (indent+"print_file: missing path")
        
    # normally call check_chunk instead, which renders chunk only if necessary
    def _render_chunk(self, x, z):
        min_indent = "  "  # increased below
        result = False
        chunk_luid = self.get_chunk_luid(x,z)
        png_name = self.get_chunk_image_name(chunk_luid)
        tmp_png_path = self.get_chunk_image_tmp_path(chunk_luid)
        genresult_name = self.get_chunk_genresult_name(chunk_luid)
        genresult_tmp_folder_path = self.get_chunk_genresults_tmp_folder(chunk_luid)
        if not os.path.isdir(genresult_tmp_folder_path):
            os.makedirs(genresult_tmp_folder_path)
        genresult_path = self.get_chunk_genresult_tmp_path(chunk_luid)
        x_min = x * self.chunk_size
        x_max = x * self.chunk_size + self.chunk_size - 1
        z_min = z * self.chunk_size
        z_max = z * self.chunk_size + self.chunk_size - 1

        #print (min_indent+"generating x = " + str(x_min) + " to " + str(x_max) + " ,  z = " + str(z_min) + " to " + str(z_max))
        geometry_value_string = str(x_min)+":"+str(z_min)+"+"+str(int(x_max)-int(x_min)+1)+"+"+str(int(z_max)-int(z_min)+1)  # +1 since max-min is exclusive and width must be inclusive for minetestmapper.py
        cmd_suffix = ""
        cmd_suffix = " > \""+genresult_path+"\""
        #self.mapper_id = "minetestmapper-region"
        cmd_string = self.python_exe_path + " \""+self.minetestmapper_py_path + "\" --region " + str(x_min) + " " + str(x_max) + " " + str(z_min) + " " + str(z_max) + " --maxheight "+str(self.maxheight)+" --minheight "+str(self.minheight)+" --pixelspernode "+str(self.pixelspernode)+" \""+self.world_path+"\" \""+tmp_png_path+"\"" + cmd_suffix

        if self.minetestmapper_py_path==self.minetestmapper_custom_path:#if self.backend_string!="sqlite3": #if self.mapper_id=="minetestmapper-region": #if self.os_name!="windows":  #since windows client doesn't normally have minetest-mapper
            #  Since minetestmapper-numpy has trouble with leveldb:
            #    such as sudo minetest-mapper --input "/home/owner/.minetest/worlds/FCAGameAWorld" --geometry -32:-32+64+64 --output /var/www/html/minetest/try1.png
            #    where geometry option is like --geometry x:y+w+h
            #    mapper_id = "minetest-mapper"
            #    NOTE: minetest-mapper is part of the minetest-data package, which can be installed alongside the git version of minetestserver
            #    BUT *buntu Trusty version of it does NOT have geometry option
            #    cmd_string = "/usr/games/minetest-mapper --input \""+self.world_path+"\" --draworigin --geometry "+geometry_value_string+" --output \""+tmp_png_path+"\""+cmd_suffix
            #    such as sudo python minetestmapper --input "/home/owner/.minetest/worlds/FCAGameAWorld" --geometry -32:-32+64+64 --output /var/www/html/minetest/try1.png
            # OR try PYTHON version (looks for expertmm fork which has geometry option like C++ version does):
            #script_path = "/home/owner/minetest/util/minetestmapper.py"
            #region_capable_script_path = "/home/owner/minetest/util/chunkymap/minetestmapper.py"
            #if self.os_name=="windows":
            #    region_capable_script_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "minetestmapper.py")
            #    if os.path.isfile(region_capable_script_path):
            #        script_path=region_capable_script_path
            #if os.path.isfile(region_capable_script_path):
                #script_path = region_capable_script_path
            geometry_string = str(x_min)+":"+str(z_min)+"+"+str(int(x_max)-int(x_min)+1)+"+"+str(int(z_max)-int(z_min)+1)  # +1 since max-min is exclusive and width must be inclusive for minetestmapper.py
            #expertmm_region_string = str(x_min) + ":" + str(x_max) + "," + str(z_min) + ":" + str(z_max)
            #cmd_string="sudo python "+script_path+" --input \""+self.world_path+"\" --geometry "+geometry_value_string+" --output \""+tmp_png_path+"\""+cmd_suffix
            cmd_string="sudo python "+self.minetestmapper_py_path+" --input \""+self.world_path+"\" --geometry "+geometry_string+" --output \""+tmp_png_path+"\""+cmd_suffix
            #sudo python /home/owner/minetest/util/minetestmapper.py --input "/home/owner/.minetest/worlds/FCAGameAWorld" --output /var/www/html/minetest/chunkymapdata/entire.png > entire-mtmresult.txt
            #sudo python /home/owner/minetest/util/chunkymap/minetestmapper.py --input "/home/owner/.minetest/worlds/FCAGameAWorld" --geometry 0:0+16+16 --output /var/www/html/minetest/chunkymapdata/chunk_x0z0.png > /home/owner/minetest/util/chunkymap-genresults/chunk_x0z0_mapper_result.txt
            #    sudo mv entire-mtmresult.txt /home/owner/minetest/util/chunkymap-genresults/

        dest_png_path = self.get_chunk_image_path(chunk_luid)
        #is_empty_chunk = is_chunk_yaml_marked(chunk_luid) and is_chunk_yaml_marked_empty(chunk_luid)
        #if self.verbose_enable:
        #    #print(min_indent+"")
        #    print(min_indent+"Running '"+cmd_string+"'...")
        #else:
        print (min_indent+"Calling map tile renderer for: "+str((x,z)))
        min_indent += "  "
        try:
            if os.path.isfile(tmp_png_path):
                os.remove(tmp_png_path)
            subprocess.call(cmd_string, shell=True)  # TODO: remember not to allow arbitrary command execution, which could happen if input contains ';' when using shell=True
            if os.path.isfile(tmp_png_path):
                result = True
                try:
                    if (os.path.isfile(dest_png_path)):
                        os.remove(dest_png_path)
                except:
                    print (min_indent+"Could not finish deleting '"+dest_png_path+"'")
                try:
                    os.rename(tmp_png_path, dest_png_path)
                    print(min_indent+"(moved to '"+dest_png_path+"')")
                    self.prepare_chunk_meta(chunk_luid)  # DOES load existing yml if exists
                    self.chunks[chunk_luid].is_fresh = True
                    self.chunks[chunk_luid].metadata["is_empty"] = False
                except:
                    print (min_indent+"Could not finish moving '"+tmp_png_path+"' to '"+dest_png_path+"'")
            else:
                if self.is_chunk_traversed_by_player(chunk_luid):
                    print (min_indent+"WARNING: no chunk data though traversed by player:")
                    print_file(genresult_path, min_indent+"  ")
            try:
                self.prepare_chunk_meta(chunk_luid)  # DOES load existing yml if exists
                this_chunk = self.chunks[chunk_luid]
                #this_chunk = MTChunk()
                #this_chunk.luid = chunk_luid
                this_chunk.set_from_genresult(genresult_path)
                chunk_yaml_path = self.get_chunk_yaml_path(chunk_luid)
                this_chunk.save_yaml(chunk_yaml_path)
                print(min_indent+"(saved yaml to '"+chunk_yaml_path+"')")
                if not self.is_save_output_ok:
                    if os.path.isfile(genresult_path):
                        os.remove(genresult_path)

            except:
                print (min_indent+"Could not finish deleting/moving output")
        except:
            print(min_indent+"Could not finish deleting/moving temp files")


        return result


    def check_players(self):
        # NOT NEEDED: if os.path.isfile(self.minetestmapper_py_path) and os.path.isfile(self.colors_path):
        print("PROCESSING PLAYERS")
        self.chunkymap_data_path=os.path.join(self.website_root,"chunkymapdata")
        chunkymap_players_name = "players"
        chunkymap_players_path = os.path.join(self.chunkymap_data_path, chunkymap_players_name)
        htaccess_path = os.path.join(chunkymap_players_path,".htaccess")
        if not os.path.isdir(chunkymap_players_path):
            os.makedirs(chunkymap_players_path)
        if not os.path.isfile(htaccess_path):
            self.deny_http_access(chunkymap_players_path)

        players_path = os.path.join(self.world_path, "players")
        player_count = 0
        player_written_count = 0
        players_moved_count = 0
        players_didntmove_count = 0
        players_saved_count = 0
        for dirname, dirnames, filenames in os.walk(players_path):
            for filename in filenames:
                file_fullname = os.path.join(players_path,filename)
                #print ("  EXAMINING "+filename)
                badstart_string = "."
                player_name = None
                player_position = None
                if (filename[:len(badstart_string)]!=badstart_string):
                    ins = open(file_fullname, 'r')
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
                    player_dest_path = os.path.join(chunkymap_players_path,filename+".yml")
                    player_x = None
                    player_y = None
                    player_z = None
                    chunk_x = None
                    chunk_y = None
                    chunk_z = None

                    player_position_tuple = get_tuple_from_notation(player_position, filename)
                    if player_position_tuple is not None:
                        #Divide by 10 because I don't know why (minetest issue)
                        player_position_tuple = player_position_tuple[0]/10.0, player_position_tuple[1]/10.0, player_position_tuple[2]/10.0
                        player_x, player_y, player_z = player_position_tuple
                        player_x = float(player_x)
                        player_y = float(player_y)
                        player_z = float(player_z)
                        chunk_x = int((int(player_x)/self.chunk_size))
                        chunk_y = int((int(player_y)/self.chunk_size))
                        chunk_z = int((int(player_z)/self.chunk_size))
                        chunk_luid = self.get_chunk_luid(chunk_x, chunk_z)
                        self.prepare_chunk_meta(chunk_luid)  # DOES load existing yml if exists
                        if not self.chunks[chunk_luid].metadata["is_traversed"]:
                            self.chunks[chunk_luid].metadata["is_traversed"] = True
                            chunk_yaml_path = self.get_chunk_yaml_path(chunk_luid)
                            self.chunks[chunk_luid].save_yaml(chunk_yaml_path)

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
    def check_chunk(self, x, z):
        min_indent = "  "
        result = [False,""]
        chunk_luid = self.get_chunk_luid(x,z)

        #if (is_different_world):  #instead, see above where all chunk files and player files are deleted
        #    self.remove_chunk(chunk_luid)

        is_traversed_by_player = self.is_chunk_traversed_by_player(chunk_luid)  #ok if stale, since is only used for whether empty chunk should be regenerated

        is_render_needed = False

        if not self.is_chunk_fresh(chunk_luid):
            if is_traversed_by_player:
                if self.is_chunk_yaml_marked(chunk_luid):
                    if self.is_chunk_yaml_marked_empty(chunk_luid):
                        is_render_needed = True
                        result[1] = "RENDERING since nonfresh empty traversed"
                        if self.verbose_enable:
                            print (min_indent+chunk_luid+": "+result[1])
                        #else:
                            #sys.stdout.write('.')
                    else:
                        if self.is_chunk_rendered_on_dest(chunk_luid):
                            result[1] = "SKIPPING since RENDERED nonfresh nonempty traversed"
                            if self.verbose_enable:
                                print (min_indent+chunk_luid+": "+result[1])
                        else:
                            is_render_needed = True
                            result[1] = "RENDERING since NONRENDERED nonfresh nonempty traversed"
                            if self.verbose_enable:
                                theoretical_path = self.get_chunk_image_path(chunk_luid)
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
                if (self.is_chunk_yaml_marked(chunk_luid)):
                    if (self.is_chunk_yaml_marked_empty(chunk_luid)):
                        result[1] = "SKIPPING since nonfresh empty nontraversed"
                        if self.verbose_enable:
                            print (min_indent+chunk_luid+": "+result[1])
                    else:
                        if (self.is_chunk_rendered_on_dest(chunk_luid)):
                            result[1] = "SKIPPING since RENDERED nonfresh nonempty nontraversed (delete png to re-render)"
                            if self.verbose_enable:
                               print (min_indent+chunk_luid+":"+result[1]) 
                        else:
                            is_render_needed = True
                            theoretical_path = self.get_chunk_image_path(chunk_luid)
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
            #if (not self.is_chunk_yaml_marked(chunk_luid)):
                #is_render_needed = True

        # This should never happen since keeping the output of minetestmapper-numpy.py (after analyzing that output) is deprecated:
        #if self.is_genresult_marked(chunk_luid) and not self.is_chunk_yaml_present(chunk_luid):
        #    tmp_chunk = MTChunk()
        #    tmp_chunk.luid = chunk_luid
        #    genresult_path = self.get_chunk_genresult_tmp_path(chunk_luid)
        #    tmp_chunk.set_from_genresult(genresult_path)
        #    chunk_yaml_path = self.get_chunk_yaml_path(chunk_luid)
        #    tmp_chunk.save_yaml(chunk_yaml_path)
        #    print(min_indent+"(saved yaml to '"+chunk_yaml_path+"')")


        if is_render_needed:
            self.rendered_count += 1
            if not self.verbose_enable:
                print(min_indent+chunk_luid+": "+result[1])
            if (self._render_chunk(x,z)):
                result[0] = True
        else:
            if self.is_chunk_rendered_on_dest(chunk_luid):
                result[0] = True
                tmp_png_path = self.get_chunk_image_path(chunk_luid)
                #NOTE: do NOT set result[1] since specific reason was already set above
                if self.verbose_enable:
                    print(min_indent+chunk_luid+": Skipping existing map tile file " + tmp_png_path + " (delete it to re-render)")
            #elif is_empty_chunk:
                #print("Skipping empty chunk " + chunk_luid)
            #else:
                #print(min_indent+chunk_luid+": Not rendered on dest.")
        return result

    def _check_map_pseudorecursion_branchfrom(self, x, z):
        chunk_luid = self.get_chunk_luid(x,z)
        branched_pos = x-1,z
        #only add if not in list already, to prevent infinite re-branching
        if branched_pos not in self.todo_positions:
            self.todo_positions.append(branched_pos)
        branched_pos = x+1,z
        if branched_pos not in self.todo_positions:
            self.todo_positions.append(branched_pos)
        branched_pos = x,z-1
        if branched_pos not in self.todo_positions:
            self.todo_positions.append(branched_pos)
        branched_pos = x,z+1
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
                x,z = this_pos
                chunk_luid = self.get_chunk_luid(x,z)
                is_present, reason_string = self.check_chunk(x,z)

                if is_present:
                    self.total_generated_count += 1
                    if x<self.chunkx_min:
                        self.chunkx_min=x
                    if x>self.chunkx_max:
                        self.chunkx_max=x
                    if z<self.chunkz_min:
                        self.chunkz_min=z
                    if z>self.chunkz_max:
                        self.chunkz_max=z
                    #end while square outline (1-chunk-thick outline) generated any png files
                    self.save_mapvars_if_changed()
                    prev_len = len(self.todo_positions)
                    self._check_map_pseudorecursion_branchfrom(x,z)
                    if self.verbose_enable:
                        print(min_indent+"["+str(self.todo_index)+"] branching from "+str((x,z))+" (added "+str(len(self.todo_positions)-prev_len)+")")
                else:
                    if self.verbose_enable:
                        print(min_indent+"["+str(self.todo_index)+"] not branching from "+str((x,z)))
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
                    x = int(x_string)
                    try:
                        z = int(z_string)
                        result = x,z
                    except:
                        pass
                except:
                    pass
        return result

    def check_map_pseudorecursion_start(self):
        if self.todo_index<0:
            print("PROCESSING MAP DATA (BRANCH PATTERN)")
            if os.path.isfile(self.minetestmapper_py_path) and os.path.isfile(self.colors_path):
                self.rendered_count = 0
                self.todo_positions = list()
                self.todo_positions.append((0,0))
                self.mapvars = get_dict_from_conf_file(self.world_yaml_path,":")
                self.verify_correct_map()
                if self.preload_all_enable:
                    self.preload_all_enable = False
                    minlen=len(self.chunk_yaml_name_opener_string)+4+len(self.chunk_yaml_name_dotext_string)  # +4 for luid, such as x1z2
                    for dirname, dirnames, filenames in os.walk(self.chunkymap_data_path):
                        for filename in filenames:
                            file_fullname = os.path.join(self.chunkymap_data_path,filename)
                            #print ("  EXAMINING "+filename)
                            badstart_string = "."
                            if (filename[:len(badstart_string)]!=badstart_string):
                                if len(filename) > minlen:
                                    chunk_luid = self.get_chunk_luid_from_yaml_name(filename)
                                    coords = self.get_coords_from_luid(chunk_luid)
                                    if coords is not None:
                                        print("Checking chunk "+str(coords)+" *"+str(self.chunk_size)+"")
                                        self.prepare_chunk_meta(chunk_luid)
                for chunk_luid in self.chunks.keys():
                    if self.chunks[chunk_luid].metadata["is_traversed"] and not self.is_chunk_rendered_on_dest(chunk_luid):
                        if self.chunks[chunk_luid].metadata["is_empty"]:
                            self.chunks[chunk_luid].metadata["is_empty"] = False
                            self.chunks[chunk_luid].save_yaml(self.get_chunk_yaml_path(chunk_luid))
                        coords = self.get_coords_from_luid(chunk_luid)
                        if coords is not None:
                            self.todo_positions.append(coords)
                        else:
                            print("ERROR: could not get coords from luid '"+chunk_luid+"'")
                        #ins = open(file_fullname, 'r')
                        #line = True
                        #while line:
                            #line = ins.readline()
                            #if line:
                        #ins.close()
                self.todo_index = 0
                #while (todo_index<len(self.todo_positions)):
                self.verify_correct_map()

    def verify_correct_map(self):
        if os.path.isfile(self.minetestmapper_py_path) and os.path.isfile(self.colors_path):
            if self.mapvars is not None and set(['world_name']).issubset(self.mapvars):
                #if self.verbose_enable:
                #    print ("  (FOUND self.world_name)")
                if self.mapvars["world_name"] != self.world_name:
                    print("")
                    print("")
                    print("")
                    print("")
                    print("")
                    print ("Removing ALL map data since from WORLD NAME is different (map '"+str(self.mapvars["world_name"])+"' is not '"+str(self.world_name)+"')...")
                    print("")
                    for dirname, dirnames, filenames in os.walk(self.chunkymap_data_path):
                        #index = 0
                        #for j in range(0,len(filenames)):
                        #    i = len(filenames) - 0 - 1
                        #    if filenames[i][0] == ".":
                        #        print ("  SKIPPING "+filenames[i])
                        #        filenames.remove_at(i)
                        for filename in filenames:
                            if filename[0] != ".":
                                file_fullname = os.path.join(self.chunkymap_data_path,filename)
                                if self.verbose_enable:
                                    print ("  EXAMINING "+filename)
                                badstart_string = "chunk"
                                if (len(filename) >= len(badstart_string)) and (filename[:len(badstart_string)]==badstart_string):
                                    os.remove(file_fullname)
                                elif filename==self.yaml_name:
                                    os.remove(file_fullname)
                    for dirname, dirnames, filenames in os.walk(os.path.join(self.chunkymap_data_path, "players")):
                        #for j in range(0,len(filenames)):
                        #    i = len(filenames) - 0 - 1
                        #    if filenames[i][0] == ".":
                        #    if self.verbose_enable:
                        #        print ("  SKIPPING "+filenames[i])
                        #        filenames.remove_at(i)
                        for filename in filenames:
                            if filename[0] != ".":
                                file_fullname = os.path.join(self.chunkymap_data_path,filename)
                                if self.verbose_enable:
                                    print ("  EXAMINING "+filename)
                                badend_string = ".yml"
                                if (len(filename) >= len(badend_string)) and (filename[len(filename)-len(badend_string):]==badend_string):
                                    os.remove(file_fullname)
                    self.chunkx_min=0
                    self.chunkx_max=0
                    self.chunkz_min=0
                    self.chunkz_max=0
                    #do not neet to run self.save_mapvars_if_changed() since already removed the yml

    def save_mapvars_if_changed(self):
        is_changed = False
        #is_different_world = False
        new_map_dict = {}
        new_map_dict["world_name"]=str(self.world_name)
        new_map_dict["chunk_size"]=str(self.chunk_size)
        new_map_dict["pixelspernode"]=str(self.pixelspernode)
        new_map_dict["chunkx_min"]=str(self.chunkx_min)
        new_map_dict["chunkx_max"]=str(self.chunkx_max)
        new_map_dict["chunkz_min"]=str(self.chunkz_min)
        new_map_dict["chunkz_max"]=str(self.chunkz_max)
        new_map_dict["maxheight"]=str(self.maxheight)
        new_map_dict["minheight"]=str(self.minheight)
        new_map_dict["world_path"]=str(self.world_path)
        new_map_dict["chunkymap_data_path"]=str(self.chunkymap_data_path)
        new_map_dict["total_generated_count"]=str(self.total_generated_count)
        if self.mapvars is None:
            print ("SAVING '" + self.world_yaml_path + "' since nothing was loaded or it did not exist")
            is_changed = True
        else:
            for this_key in new_map_dict.iterkeys():
                if this_key != "total_generated_count":  # don't care if generated count changed since may have been regenerated
                    if (this_key not in self.mapvars.keys()):
                        is_changed = True
                        print ("SAVING '" + self.world_yaml_path + "' since " + str(this_key) + " not in mapvars")
                        break
                    elif (str(self.mapvars[this_key]) != str(new_map_dict[this_key])):
                        is_changed = True
                        print ("SAVING '" + self.world_yaml_path + "' since new " + this_key + " value " + str(new_map_dict[this_key]) + " not same as saved value " + str(self.mapvars[this_key]) + "")
                        break
        if is_changed:
            save_conf_from_dict(self.world_yaml_path,new_map_dict,":")
            #outs = open(self.world_yaml_path, 'w')
            #outs.write("world_name:"+str(self.world_name) + "\n")
            #outs.write("chunk_size:"+str(self.chunk_size) + "\n")
            #outs.write("pixelspernode:"+str(self.pixelspernode) + "\n")
            #outs.write("chunkx_min:"+str(self.chunkx_min) + "\n")
            #outs.write("chunkx_max:"+str(self.chunkx_max) + "\n")
            #outs.write("chunkz_min:"+str(self.chunkz_min) + "\n")
            #outs.write("chunkz_max:"+str(self.chunkz_max) + "\n")
            ##values for command arguments:
            #outs.write("maxheight:"+str(self.maxheight) + "\n")
            #outs.write("minheight:"+str(self.minheight) + "\n")
            ##ALSO save to YAML:
            #outs.write("world_path:"+str(self.world_path) + "\n")
            #outs.write("chunkymap_data_path:"+str(self.chunkymap_data_path) + "\n")
            #outs.write("total_generated_count:"+str(self.total_generated_count) + "\n")
            #outs.close()
            #self.mapvars = get_dict_from_conf_file(self.world_yaml_path,":")
        else:
            if self.verbose_enable:
                print ("  (Not saving '"+self.world_yaml_path+"' since same value of each current variable is already in file as loaded)")

    def check_map_inefficient_squarepattern(self):
        if os.path.isfile(self.minetestmapper_py_path) and os.path.isfile(self.colors_path):
            self.rendered_count = 0
            if not os.path.isdir(self.chunkymap_data_path):
                os.mkdir(self.chunkymap_data_path)

            htaccess_path = os.path.join(self.chunkymap_data_path,".htaccess")
            if not os.path.isdir(self.chunkymap_data_path):
                os.makedirs(self.chunkymap_data_path)
            if not os.path.isfile(htaccess_path):
                self.deny_http_access(self.chunkymap_data_path)

            self.mapvars = get_dict_from_conf_file(self.world_yaml_path,":")
            #is_testonly == (self.os_name=="windows")

            self.verify_correct_map()

            self.chunkx_min = 0
            self.chunkz_min = 0
            self.chunkx_max = 0
            self.chunkz_max = 0
            if self.mapvars is not None:
                if "chunkx_min" in self.mapvars.keys():
                    self.chunkx_min = self.mapvars["chunkx_min"]
                if "chunkx_max" in self.mapvars.keys():
                    self.chunkx_max = self.mapvars["chunkx_max"]
                if "chunkz_min" in self.mapvars.keys():
                    self.chunkz_min = self.mapvars["chunkz_min"]
                if "chunkz_max" in self.mapvars.keys():
                    self.chunkz_max = self.mapvars["chunkz_max"]
            self.total_generated_count = 0

            newchunk_luid_list = list()
            this_iteration_generates_count = 1
            #if str(self.world_name) != str(self.mapvars["world_name"]):
            #    is_different_world = True
            #    print("FULL RENDER since chosen world name '"+self.world_name+"' does not match previously rendered world name '"+self.mapvars["world_name"]+"'")
            print("PROCESSING MAP DATA (SQUARE)")
            while this_iteration_generates_count > 0:
                this_iteration_generates_count = 0
                self.read_then_remove_signals()
                if not self.refresh_map_enable:
                    break
                for z in range (self.chunkz_min,self.chunkz_max+1):
                    self.read_then_remove_signals()
                    if not self.refresh_map_enable:
                        break
                    for x in range(self.chunkx_min,self.chunkx_max+1):
                        self.read_then_remove_signals()
                        if not self.refresh_map_enable:
                            break
                        #python ~/minetest/util/minetestmapper-numpy.py --region -1200 800 -1200 800 --drawscale --maxheight 100 --minheight -50 --pixelspernode 1 ~/.minetest/worlds/FCAGameAWorld ~/map.png
                        #sudo mv ~/map.png /var/www/html/minetest/images/map.png

                        #only generate the edges (since started with region 0 0 0 0) and expanding from there until no png is created:
                        is_outline = (x==self.chunkx_min) or (x==self.chunkx_max) or (z==self.chunkz_min) or (z==self.chunkz_max)
                        if is_outline:
                            is_present, reason_string = self.check_chunk(x,z)
                            if is_present:
                                this_iteration_generates_count += 1
                                self.total_generated_count += 1
                    if self.verbose_enable:
                        print ("")  # blank line before next z so output is more readable
                self.chunkx_min -= 1
                self.chunkz_min -= 1
                self.chunkx_max += 1
                self.chunkz_max += 1
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
