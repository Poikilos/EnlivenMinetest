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
                if not line_strip[0]=="#":  # if not comment
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
        print("Could not finish saving chunk metadata to '"+str(yml_path)+"': "+str(traceback.format_exc()))

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
    chunk_dict = None
    is_player_in_this_chunk = None
    is_fresh = None
    #width = None
    #height = None
    #is_marked = None
    #is_marked_empty = None
    #image_w = None
    #image_h = None
    #image_left = None
    #image_top = None
    #image_right = None
    #image_bottom = None

    def __init__(self):
        # NOTE: variables that need to be saved (and only they) should be stored in dict
        self.chunk_dict = {}

        self.is_player_in_this_chunk = False
        self.is_fresh = False
        
        self.chunk_dict["is_marked_empty"] = False
        self.chunk_dict["is_marked"] = False
        self.chunk_dict["width"] = None
        self.chunk_dict["height"] = None
        self.chunk_dict["image_w"] = None
        self.chunk_dict["image_h"] = None
        self.chunk_dict["image_left"] = None
        self.chunk_dict["image_top"] = None
        self.chunk_dict["image_right"] = None
        self.chunk_dict["image_bottom"] = None

    def load_yaml(self, yml_path):
        self.chunk_dict = get_dict_modified_by_conf_file(self.chunk_dict,yml_path,":")

    def save_yaml(self, yml_path):
        save_conf_from_dict(yml_path, self.chunk_dict, assignment_operator=":", save_nulls_enable=False)
        #try:
            #outs = open(yml_path, 'w')
            #outs.write("is_marked_empty:"+str(self.is_marked_empty)+"\n")
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
            self.chunk_dict["is_marked"] = True
            ins = open(this_genresult_path, 'r')
            line = True
            while line:
                line = ins.readline()
                if line:
                    line_strip = line.strip()
                    if "data does not exist" in line_strip:
                        self.chunk_dict["is_marked_empty"] = True
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
                                                    self.chunk_dict["image_w"]=int(chunks[1].strip())
                                                except:
                                                    print("Bad value for image w:"+str(chunks[1]))
                                            elif chunks[0].strip()=="h":
                                                try:
                                                    self.chunk_dict["image_h"]=int(chunks[1].strip())
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
                                    self.chunk_dict["image_left"]=int(rect_values_list[0].strip())
                                    self.chunk_dict["image_right"]=int(rect_values_list[1].strip())
                                    self.chunk_dict["image_top"]=int(rect_values_list[2].strip())
                                    self.chunk_dict["image_bottom"]=int(rect_values_list[3].strip())
                                else:
                                    print("Bad map rect, so ignoring: "+rect_values_string)
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
    mtmn_path = None
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
    #total_generated_count = 0
    #endregion values to save to YAML
    
    loop_enable = None
    is_verbose = None

    world_blacklist = None

    def __init__(self):  #formerly checkpaths() in global scope
        self.is_verbose = True
        self.loop_enable = True
        self.refresh_map_enable = True
        self.refresh_players_enable = True
        self.chunks = {}
        self.username = "owner"
        self.website_root="/var/www/html/minetest"
        self.world_name = "FCAGameAWorld"
        self.os_name="linux"
        self.refresh_map_seconds = 10
        self.refresh_players_seconds = 3

        input_string = ""
        if (os.path.sep!="/"):
            self.os_name="windows"
        #input_string = input("Which self.username contains minetest/util/minetestmapper-numpy.py (minetest not .minetest) ["+self.username+"]?")
        if (len(input_string)>0):
            self.username = input_string

        #input_string = input("What is the root folder of your minetest website ["+self.website_root+"]?")
        if (len(input_string)>0):
            self.website_root = input_string
        self.chunkymap_data_path=os.path.join(self.website_root,"chunkymapdata")

        #input_string = input("What is the game name ["+self.world_name+"]")
        if (len(input_string)>0):
            self.world_name = input_string
        #region server-specific options
        self.profiles_path = "/home"
        if self.os_name=="windows":
            self.profiles_path = "C:\\Users"
        self.profile_path = os.path.join(self.profiles_path, self.username)
        #if (not os.path.isdir(self.profile_path)):
        #    self.profile_path = os.path.join(self.profiles_path, "jgustafson")
        self.dotminetest_path = os.path.join(self.profile_path,".minetest")
        if (self.os_name=="windows"): self.dotminetest_path = "C:\\games\\Minetest"
        self.worlds_path = os.path.join(self.dotminetest_path,"worlds")
        self.world_path = os.path.join(self.worlds_path, self.world_name)
        auto_chosen_world = False
        self.world_blacklist = list()
        self.world_blacklist.append("abiyahhgamebv7world1")
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

        self.is_save_output_ok = True   # Keeping output after analyzing it is no longer necessary since results are saved to YAML, but keeping output provides debug info since is the output of minetestmapper-numpy.py

        
        try:
            alt_path = "C:\\python27\python.exe"
            if os.path.isfile(alt_path):
                self.python_exe_path = alt_path
            #else may be in path--assume installer worked
        except:
            pass  # do nothing, probably linux

        self.mtmn_path = os.path.join( self.profile_path, "minetest/util/minetestmapper-numpy.py" )
        self.colors_path = os.path.join( self.profile_path, "minetest/util/colors.txt" )
        if self.os_name=="windows":
            self.mtmn_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "minetestmapper-numpy.py")
            self.colors_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "colors.txt")
            self.website_root = os.path.dirname(os.path.abspath(__file__))

        self.chunkx_min = 0
        self.chunkz_min = 0
        self.chunkx_max = 0
        self.chunkz_max = 0

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

    def get_chunk_yaml_name(self, chunk_luid):
        return "chunk_"+chunk_luid+".yml"

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
            #        if "is_marked_empty:" in line_strip:
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
                    prevalue_string="is_marked_empty:"
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
            yaml_path = self.get_chunk_yaml_path(chunk_luid)
            if os.path.isfile(yaml_path):
                self.chunks[chunk_luid].load_yaml(yaml_path)

    def render_chunk(self, x, z):
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

        #print ("generating x = " + str(x_min) + " to " + str(x_max) + " ,  z = " + str(z_min) + " to " + str(z_max))
        cmd_suffix = ""
        cmd_suffix = " > \""+genresult_path+"\""
        cmd_string = self.python_exe_path + " \""+self.mtmn_path + "\" --region " + str(x_min) + " " + str(x_max) + " " + str(z_min) + " " + str(z_max) + " --maxheight "+str(self.maxheight)+" --minheight "+str(self.minheight)+" --pixelspernode "+str(self.pixelspernode)+" \""+self.world_path+"\" \""+tmp_png_path+"\"" + cmd_suffix
        dest_png_path = self.get_chunk_image_path(chunk_luid)
        #is_empty_chunk = is_chunk_yaml_marked(chunk_luid) and is_chunk_yaml_marked_empty(chunk_luid)
        print (cmd_string)
        subprocess.call(cmd_string, shell=True)  # TODO: remember not to allow arbitrary command execution, which could happen if input contains ';' when using shell=True
        if os.path.isfile(tmp_png_path):
            result = True
            try:
                if (os.path.isfile(dest_png_path)):
                    os.remove(dest_png_path)
            except:
                print ("Could not finish deleting '"+dest_png_path+"'")
            try:
                os.rename(tmp_png_path, dest_png_path)
                print("(moved to '"+dest_png_path+"')")
                self.prepare_chunk_meta(chunk_luid)  # DOES load existing yml if exists
                self.chunks[chunk_luid].is_fresh = True
            except:
                print ("Could not finish moving '"+tmp_png_path+"' to '"+dest_png_path+"'")
        try:
            self.prepare_chunk_meta(chunk_luid)  # DOES load existing yml if exists
            this_chunk = self.chunks[chunk_luid]
            #this_chunk = MTChunk()
            this_chunk.set_from_genresult(genresult_path)
            chunk_yaml_path = self.get_chunk_yaml_path(chunk_luid)
            this_chunk.save_yaml(chunk_yaml_path)
            this_chunk.save_yaml(chunk_yaml_path)
            print("(saved yaml to '"+chunk_yaml_path+"')")
            if not self.is_save_output_ok:
                if os.path.isfile(genresult_path):
                    os.remove(genresult_path)
                
        except:
            print ("Could not finish deleting/moving output")



        return result
                

    def check_players(self):
        # NOT NEEDED: if os.path.isfile(self.mtmn_path) and os.path.isfile(self.colors_path):
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
                        chunk_x = int((float(player_x)/self.chunk_size))
                        chunk_y = int((float(player_y)/self.chunk_size))
                        chunk_z = int((float(player_z)/self.chunk_size))
                        chunk_luid = self.get_chunk_luid(chunk_x, chunk_z)
                        self.prepare_chunk_meta(chunk_luid)  # DOES load existing yml if exists
                        self.chunks[chunk_luid].is_player_in_this_chunk = True

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
                            if self.is_verbose:
                                print("PLAYER MOVED: "+str(player_name)+" moved from "+str(saved_player_x)+","+str(saved_player_y)+","+str(saved_player_z)+" to "+str(player_x)+","+str(player_y)+","+str(player_z))
                            players_moved_count += 1
                        else:
                            if self.is_verbose:
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
                        if self.is_verbose:
                            print("DIDN'T MOVE: "+str(player_name))
                            players_didntmove_count += 1
                    player_count += 1
        if not self.is_verbose:
            print("PLAYERS:")
            print("  saved: "+str(player_written_count)+" (moved:"+str(players_moved_count)+"; new:"+str(players_saved_count)+")")
            print("  didn't move: "+str(player_name))

    def is_player_at_luid(self, chunk_luid):
        result = False
        if chunk_luid in self.chunks.keys():
            result = self.chunks[chunk_luid].is_player_in_this_chunk
        return result

    def is_chunk_fresh(self, chunk_luid):
        result = False
        if chunk_luid in self.chunks.keys():
            result = self.chunks[chunk_luid].is_fresh
        return result
        
    def check_map(self):
        if os.path.isfile(self.mtmn_path) and os.path.isfile(self.colors_path):
            rendered_count = 0
            self.chunkymap_data_path=os.path.join(self.website_root,"chunkymapdata")
            yaml_name = "generated.yml"
            world_yaml_path = os.path.join(self.chunkymap_data_path, yaml_name)
            if not os.path.isdir(self.chunkymap_data_path):
                os.mkdir(self.chunkymap_data_path)

            htaccess_path = os.path.join(self.chunkymap_data_path,".htaccess")
            if not os.path.isdir(self.chunkymap_data_path):
                os.makedirs(self.chunkymap_data_path)
            if not os.path.isfile(htaccess_path):
                self.deny_http_access(self.chunkymap_data_path)

            mapvars = get_dict_from_conf_file(world_yaml_path,":")
            #is_testonly == (self.os_name=="windows")

            if mapvars is not None and set(['world_name']).issubset(mapvars):
                #if self.is_verbose:
                #    print ("  (FOUND self.world_name)")
                if mapvars["world_name"] != self.world_name:
                    print ("Removing ALL map data since from WORLD NAME is different (map '"+str(mapvars["world_name"])+"' is not '"+str(self.world_name)+"')...")
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
                                if self.is_verbose:
                                    print ("  EXAMINING "+filename)
                                badstart_string = "chunk"
                                if (len(filename) >= len(badstart_string)) and (filename[:len(badstart_string)]==badstart_string):
                                    os.remove(file_fullname)
                                elif filename==yaml_name:
                                    os.remove(file_fullname)
                    for dirname, dirnames, filenames in os.walk(os.path.join(self.chunkymap_data_path, "players")):
                        #for j in range(0,len(filenames)):
                        #    i = len(filenames) - 0 - 1
                        #    if filenames[i][0] == ".":
                        #    if self.is_verbose:
                        #        print ("  SKIPPING "+filenames[i])
                        #        filenames.remove_at(i)
                        for filename in filenames:
                            if filename[0] != ".":
                                file_fullname = os.path.join(self.chunkymap_data_path,filename)
                                if self.is_verbose:
                                    print ("  EXAMINING "+filename)
                                badend_string = ".yml"
                                if (len(filename) >= len(badend_string)) and (filename[len(filename)-len(badend_string):]==badend_string):
                                    os.remove(file_fullname)
            self.chunkx_min = 0
            self.chunkz_min = 0
            self.chunkx_max = 0
            self.chunkz_max = 0
            total_generated_count = 0

            newchunk_luid_list = list()
            outline_generates_count = 1
            is_changed = False
            is_different_world = False
            #if str(self.world_name) != str(mapvars["world_name"]):
            #    is_different_world = True
            #    print("FULL RENDER since chosen world name '"+self.world_name+"' does not match previously rendered world name '"+mapvars["world_name"]+"'")
            print("PROCESSING MAP DATA")
            while outline_generates_count > 0:
                outline_generates_count = 0
                for z in range (self.chunkz_min,self.chunkz_max+1):
                    for x in range(self.chunkx_min,self.chunkx_max+1):
                        #python ~/minetest/util/minetestmapper-numpy.py --region -1200 800 -1200 800 --drawscale --maxheight 100 --minheight -50 --pixelspernode 1 ~/.minetest/worlds/FCAGameAWorld ~/map.png
                        #sudo mv ~/map.png /var/www/html/minetest/images/map.png

                        #only generate the edges (since started with region 0 0 0 0) and expanding from there until no png is created:
                        is_outline = (x==self.chunkx_min) or (x==self.chunkx_max) or (z==self.chunkz_min) or (z==self.chunkz_max)
                        if is_outline:
                            chunk_luid = self.get_chunk_luid(x,z)

                            #if (is_different_world):  #instead, see above where all chunk files and player files are deleted
                            #    self.remove_chunk(chunk_luid)

                            is_player_in_this_chunk = self.is_player_at_luid(chunk_luid)

                            is_render_needed = False

                            if not self.is_chunk_fresh(chunk_luid):
                                if is_player_in_this_chunk:
                                    if self.is_chunk_yaml_marked(chunk_luid):
                                        if self.is_chunk_yaml_marked_empty(chunk_luid):
                                            is_render_needed = True
                                            if self.is_verbose:
                                                print (chunk_luid+": RENDERING nonfresh previously marked empty (player in it)")
                                            else:
                                                sys.stdout.write('.')
                                        else:
                                            if self.is_verbose:
                                                print (chunk_luid+": SKIPPING nonfresh previously marked (player in it)")
                                            #else:
                                                #sys.stdout.write('.')
                                    else:
                                        is_render_needed = True
                                        if self.is_verbose:
                                            print (chunk_luid+": RENDERING nonfresh unmarked (player in it)")
                                        else:
                                            sys.stdout.write('.')
                                else:
                                    if (not self.is_chunk_yaml_marked(chunk_luid)):
                                        is_render_needed = True
                                        if self.is_verbose:
                                            print (chunk_luid+": RENDERING nonfresh unmarked (simple check since has no player)")
                                        else:
                                            sys.stdout.write('.')
                                    else:
                                        if self.is_verbose:
                                            print (chunk_luid+": SKIPPING nonfresh previously marked (simple check since has no player)")
                            else:
                                if self.is_verbose:
                                    print (chunk_luid+": SKIPPING fresh chunk")
                                #if (not self.is_chunk_yaml_marked(chunk_luid)):
                                    #is_render_needed = True

                            # This should never happen since keeping the output of minetestmapper-numpy.py (after analyzing that output) is deprecated:
                            #if self.is_genresult_marked(chunk_luid) and not self.is_chunk_yaml_present(chunk_luid):
                            #    tmp_chunk = MTChunk()
                            #    genresult_path = self.get_chunk_genresult_tmp_path(chunk_luid)
                            #    tmp_chunk.set_from_genresult(genresult_path)
                            #    chunk_yaml_path = self.get_chunk_yaml_path(chunk_luid)
                            #    tmp_chunk.save_yaml(chunk_yaml_path)
                            #    print("(saved yaml to '"+chunk_yaml_path+"')")


                            if is_render_needed:
                                rendered_count += 1
                                if (self.render_chunk(x,z)):
                                    total_generated_count += 1
                                    outline_generates_count += 1
                            else:
                                if self.is_chunk_rendered_on_dest(chunk_luid):
                                    total_generated_count += 1
                                    outline_generates_count += 1
                                    tmp_png_path = self.get_chunk_image_path(chunk_luid)
                                    if self.is_verbose:
                                        print(chunk_luid+": Skipping existing map tile file " + tmp_png_path + " (delete it to re-render)")
                                #elif is_empty_chunk:
                                    #print("Skipping empty chunk " + chunk_luid)
                                #else:
                                    #print(chunk_luid+": Not rendered on dest.")
                    if self.is_verbose:
                        print ("")  # blank line before next z so output is more readable
                self.chunkx_min -= 1
                self.chunkz_min -= 1
                self.chunkx_max += 1
                self.chunkz_max += 1
            #end while square outline (1-chunk-thick outline) generated any png files
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
            new_map_dict["total_generated_count"]=str(total_generated_count)
            if mapvars is None:
                print ("SAVING '" + world_yaml_path + "' since nothing was loaded or it did not exist")
                is_changed = True
            else:
                for this_key in new_map_dict.iterkeys():
                    if (this_key not in mapvars.keys()):
                        is_changed = True
                        print ("SAVING '" + world_yaml_path + "' since " + str(this_key) + " not in mapvars")
                        break
                    elif (str(mapvars[this_key]) != str(new_map_dict[this_key])):
                        is_changed = True
                        print ("SAVING '" + world_yaml_path + "' since new " + this_key + " value " + str(new_map_dict[this_key]) + " not same as saved value " + str(mapvars[this_key]) + "")
                        break
            if is_changed:
                outs = open(world_yaml_path, 'w')
                outs.write("world_name:"+str(self.world_name) + "\n")
                outs.write("chunk_size:"+str(self.chunk_size) + "\n")
                outs.write("pixelspernode:"+str(self.pixelspernode) + "\n")
                outs.write("chunkx_min:"+str(self.chunkx_min) + "\n")
                outs.write("chunkx_max:"+str(self.chunkx_max) + "\n")
                outs.write("chunkz_min:"+str(self.chunkz_min) + "\n")
                outs.write("chunkz_max:"+str(self.chunkz_max) + "\n")
                #values for command arguments:
                outs.write("maxheight:"+str(self.maxheight) + "\n")
                outs.write("minheight:"+str(self.minheight) + "\n")
                #ALSO save to YAML:
                outs.write("world_path:"+str(self.world_path) + "\n")
                outs.write("chunkymap_data_path:"+str(self.chunkymap_data_path) + "\n")
                outs.write("total_generated_count:"+str(total_generated_count) + "\n")
                outs.close()
            else:
                if self.is_verbose:
                    print ("  (Not saving '"+world_yaml_path+"' since same value of each current variable is already in file as loaded)")
            if not self.is_verbose:
                print("  rendered: "+str(rendered_count)+" (only checks for new chunks)")
        else:
            print ("MAP ERROR: failed since this folder must contain colors.txt and minetestmapper-numpy.py")

    def read_then_remove_signals(self):
        signal_path = self.get_signal_path()
        if os.path.isfile(signal_path):
            signals = get_dict_from_conf_file(signal_path)
            if signals is not None:
                for this_key in signals.keys:
                    if this_key=="loop_enable":
                        if not signals[this_key]:
                            self.loop_enable = False
                        else:
                            print("WARNING: Got signal to change loop_enable to True, so doing nothing")
                    elif this_key=="refresh_players_enable":
                        if type(signals[this_key]) is bool:
                            self.refresh_players_enable = signals[this_key]
                        else:
                            print("ERROR: expected bool for "+this_key)
                    elif this_key=="refresh_map_seconds":
                        if (type(signals[this_key]) is float) or (type(signals[this_key]) is int):
                            if float(signals[this_key])>=1.0:
                                self.refresh_map_seconds = float(signals[this_key])
                            else:
                                print("ERROR: expected >=1 seconds for refresh_map_seconds (int or float)")
                        else:
                            print("ERROR: expected int for "+this_key)
                    elif this_key=="refresh_players_seconds":
                        if (type(signals[this_key]) is float) or (type(signals[this_key]) is int):
                            if float(signals[this_key])>=1.0:
                                self.refresh_players_seconds = float(signals[this_key])
                            else:
                                print("ERROR: expected >=1 seconds for refresh_players_seconds (int or float)")
                        else:
                            print("ERROR: expected int for "+this_key)
                    elif this_key=="refresh_map_enable":
                        if type(signals[this_key]) is bool:
                            self.refresh_map_enable = signals[this_key]
                        else:
                            print("ERROR: expected bool for "+this_key)

                    else:
                        print("ERROR: unknown signal '"+this_key+"'")
                    

            else:
                print("WARNING: blank '"+signal_path+"'")
            try:
                os.remove()
            except:
                print("FATAL ERROR: "+__file__+" must have permission to remove '"+signal_path+"' so exiting to avoid inability to avoid repeating commands at next launch.")
                self.loop_enable = False

    def run_loop(self):
        #self.last_run_second = best_timer()
        self.loop_enable = True
        self.is_verbose = False
        while self.loop_enable:
            before_second = best_timer()
            run_wait_seconds = self.refresh_map_seconds
            if self.refresh_players_seconds < run_wait_seconds:
                run_wait_seconds = self.refresh_players_seconds
            print("")
            self.read_then_remove_signals()
            if self.loop_enable:
                if self.refresh_players_enable:
                    if self.last_players_refresh_second is None or (best_timer()-self.last_players_refresh_second > self.refresh_players_seconds ):
                        last_players_refresh_second = best_timer()
                        self.check_players()
                    else:
                        print("waiting before doing player update")
                else:
                    print("player update is not enabled")
                if self.refresh_map_enable:
                    if self.last_map_refresh_second is None or (best_timer()-self.last_map_refresh_second > self.refresh_map_seconds):
                        last_map_refresh_second = best_timer()
                        self.check_map()
                    else:
                        print("waiting before doing map update")
                else:
                    print("map update is not enabled")
            else:
                self.is_verbose = True
            run_wait_seconds -= (best_timer()-before_second)
            if (int(float(run_wait_seconds)+.5)>0.0):
                time.sleep(run_wait_seconds)

    def run(self):
        if self.refresh_players_enable:
            self.check_players()
        if self.refresh_map_enable:
            self.check_map()

if __name__ == '__main__':
    mtchunks = MTChunks()
    signal_path = mtchunks.get_signal_path()
    stop_line = "loop_enable:False"
    parser = argparse.ArgumentParser(description='A mapper for minetest')
    parser.add_argument('--skip-map', type = bool, metavar = ('skip_map'), default = False, help = 'draw map tiles and save YAML files for chunkymap.php to use')
    parser.add_argument('--skip-players', type = bool, metavar = ('skip_players'), default = False, help = 'update player YAML files for chunkymap.php to use')
    parser.add_argument('--loop', type = bool, metavar = ('loop'), default = False, help = 'keep running until "'+signal_path+'" contains the line '+stop_line)
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
        if args.loop:
            print("To stop chunkymap-regen loop, save a line '"+stop_line+"' to '"+signal_path+"'")
            mtchunks.run_loop()
        else:
            mtchunks.run()
