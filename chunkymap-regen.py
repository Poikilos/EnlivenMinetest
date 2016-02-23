#!/usr/bin/env python2
import os
import subprocess

# REQUIRES: see README.md
# The way to do a full render is deleting all files from the folder self.chunkymap_data_path such as /var/www/html/minetest/chunkymapdata (or chunkymap in current directory on Windows)

#minetestmapper-numpy.py calculates the region as follows:
#(XMIN','XMAX','ZMIN','ZMAX'), default = (-2000,2000,-2000,2000)
#sector_xmin,sector_xmax,sector_zmin,sector_zmax = numpy.array(args.region)/16
#sector_ymin = args.self.minheight/16
#sector_ymax = args.self.maxheight/16
#region server-specific options

class MTChunk:
    x = None
    z = None
    is_player_here = None
    is_fresh = None

    def __init__(self):
        self.is_player_here = False
        self.is_fresh = False

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
    chunk_size = 80
    #values for command arguments:
    maxheight = 50
    minheight = -25
    pixelspernode = 1
    #ALSO save to YAML:
    #total_generated_count = 0
    #endregion values to save to YAML
    
    def __init__(self):  #formerly checkpaths() in global scope
        self.chunks = {}
        self.username = "owner"
        self.website_root="/var/www/html/minetest"
        self.world_name = "FCAGameAWorld"
        os_name="linux"

        input_string = ""
        if (os.path.sep!="/"):
            os_name="windows"
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
        if os_name=="windows":
            self.profiles_path = "C:\\Users"
        self.profile_path = os.path.join(self.profiles_path, self.username)
        #if (not os.path.isdir(self.profile_path)):
        #    self.profile_path = os.path.join(self.profiles_path, "jgustafson")
        self.dotminetest_path = os.path.join(self.profile_path,".minetest")
        if (os_name=="windows"): self.dotminetest_path = "C:\\games\\Minetest"
        self.worlds_path = os.path.join(self.dotminetest_path,"worlds")
        self.world_path = os.path.join(self.worlds_path, self.world_name)
        auto_chosen_world = False
        if not os.path.isdir(self.world_path):
            #for item in os.walk(self.worlds_path):
            print ("LOOKING FOR WORLDS IN " + self.worlds_path)
            for dirname, dirnames, filenames in os.walk(self.worlds_path):
                index = 0
                for j in range(0,len(dirnames)):
                    i = len(dirnames) - 0 - 1
                    if dirnames[i][0] == ".":
                        print ("  SKIPPING "+dirnames[i])
                        dirnames.remove_at(i)
                for subdirname in dirnames:
                    print ("  EXAMINING "+subdirname)
                    if (index == len(dirnames)-1):  # skip first one because the one on my computer is big
                        self.world_name = subdirname
                        self.world_path = os.path.join(dirname, subdirname) #  os.path.join(self.worlds_path, "try7amber")
                        print ("  CHOSE "+self.world_path)
                        auto_chosen_world = True
                        break
                    index += 1
                if auto_chosen_world:
                    break
        self.python_exe_path = "python"
                
        self.is_save_output_ok = True   # this is probably required to avoid minutely writes


        try:
            alt_path = "C:\\python27\python.exe"
            if os.path.isfile(alt_path):
                self.python_exe_path = alt_path
        except:
            pass  # do nothing, probably linux

        self.mtmn_path = os.path.join( self.profile_path, "minetest/util/minetestmapper-numpy.py" )
        self.colors_path = os.path.join( self.profile_path, "minetest/util/colors.txt" )
        if os_name=="windows":
            self.mtmn_path = os.path.join(os.path.dirname(__file__), "minetestmapper-numpy.py")
            self.colors_path = os.path.join(os.path.dirname(__file__), "colors.txt")
            self.website_root = os.path.dirname(__file__)

        self.chunkx_min = 0
        self.chunkz_min = 0
        self.chunkx_max = 0
        self.chunkz_max = 0

        self.chunk_size = 80
        self.maxheight = 50
        self.minheight = -25
        self.pixelspernode = 1

    def get_dict_from_conf_file(self, path,assignment_operator="="):
        results = None
        print ("Checking "+str(path)+" for settings...")
        if os.path.isfile(path):
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
                                    print ("   CHECKING... "+result_name+":"+result_value)
                                    results[result_name]=result_value
            ins.close()
        return results


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
        return os.path.join(os.path.dirname(__file__), self.get_chunk_image_name(chunk_luid))

    def get_chunk_image_path(self, chunk_luid):
        return os.path.join(self.chunkymap_data_path, self.get_chunk_image_name(chunk_luid))

    def get_chunk_genresult_name(self, chunk_luid):
        return "chunk_"+chunk_luid+"_mapper_result.txt"

    def get_chunk_genresult_tmp_path(self, chunk_luid):
        return os.path.join(os.path.dirname(__file__), self.get_chunk_genresult_name(chunk_luid))

    def get_chunk_genresult_path(self, chunk_luid):
        return os.path.join(self.chunkymap_data_path, self.get_chunk_genresult_name(chunk_luid))

    def is_genresult_marked(self, chunk_luid):
        result = False
        dest_genresult_path = self.get_chunk_genresult_path(chunk_luid)
        #is_empty_chunk = False
        if os.path.isfile(dest_genresult_path):
            result = True
        return result

    def is_genresult_marked_empty(self, chunk_luid):
        dest_genresult_path = self.get_chunk_genresult_path(chunk_luid)
        result = False
        if os.path.isfile(dest_genresult_path):
            ins = open(dest_genresult_path)
            line = True
            while line:
                line = ins.readline()
                if line:
                    line_strip = line.strip()
                    if "data does not exist" in line_strip:
                        result = True
                        break
            ins.close()
        return result

    def remove_genresult(self, chunk_luid):
        result = False
        dest_genresult_path = self.get_chunk_genresult_path(chunk_luid)
        if os.path.isfile(dest_genresult_path):
            result = True
            os.remove(dest_genresult_path)
        return result

    def remove_chunk_image(self, chunk_luid):
        result = False
        png_path = self.get_chunk_image_path(chunk_luid)
        if os.path.isfile(png_path):
            result = True
            os.remove(png_path)
        return result
            
    def remove_chunk(self, chunk_luid):
        result = False
        out_path = self.get_chunk_genresult_path(chunk_luid)
        png_path = self.get_chunk_image_path(chunk_luid)
        if os.path.isfile(out_path):
            os.remove(out_path)
            result = True
        if os.path.isfile(png_path):
            os.remove(png_path)
            result = True
        return result

    def is_chunk_rendered_on_dest(self, chunk_luid):  #formerly is_chunk_empty_on_dest (reversed)
        is_rendered = False
        #is_chunk_out_empty = self.is_genresult_marked_empty(chunk_luid)
        #dest_genresult_path = self.get_chunk_genresult_path(chunk_luid)
        dest_png_path = self.get_chunk_image_name(chunk_luid)
        if os.path.isfile(dest_png_path):
            #os.remove(dest_genresult_path)
            is_rendered = True
        return is_rendered
    
    def prepare_chunk_meta(self, chunk_luid):
        if chunk_luid not in self.chunks.keys():
            self.chunks[chunk_luid] = MTChunk()
        
    def render_chunk(self, x, z):
        result = False
        chunk_luid = self.get_chunk_luid(x,z)
        png_name = self.get_chunk_image_name(chunk_luid)
        png_path = self.get_chunk_image_tmp_path(chunk_luid)
        cmd_suffix = ""
        genresult_name = self.get_chunk_genresult_name(chunk_luid)
        genresult_path = self.get_chunk_genresult_tmp_path(chunk_luid)
        if self.is_save_output_ok:
            cmd_suffix = " > \""+genresult_path+"\""
        x_min = x * self.chunk_size
        x_max = x * self.chunk_size + self.chunk_size - 1
        z_min = z * self.chunk_size
        z_max = z * self.chunk_size + self.chunk_size - 1
            
        #print ("generating x = " + str(x_min) + " to " + str(x_max) + " ,  z = " + str(z_min) + " to " + str(z_max))
        cmd_string = self.python_exe_path + " \""+self.mtmn_path + "\" --region " + str(x_min) + " " + str(x_max) + " " + str(z_min) + " " + str(z_max) + " --maxheight "+str(self.maxheight)+" --minheight "+str(self.minheight)+" --pixelspernode "+str(self.pixelspernode)+" \""+self.world_path+"\" \""+png_path+"\"" + cmd_suffix
        dest_png_path = self.get_chunk_image_path(chunk_luid)
        dest_genresult_path = self.get_chunk_genresult_path(chunk_luid)
        #is_empty_chunk = is_genresult_marked(chunk_luid) and is_genresult_marked_empty(chunk_luid)
        print (cmd_string)
        subprocess.call(cmd_string, shell=True)  # TODO: remember not to allow arbitrary command execution, which could happen if input contains ';' when using shell=True
        if os.path.isfile(png_path):
            result = True
            try:
                if (os.path.isfile(dest_png_path)):
                    os.remove(dest_png_path)
            except:
                print ("Could not finish deleting '"+dest_png_path+"'")
            try:
                os.rename(png_path, dest_png_path)
                print("(moved to '"+dest_png_path+"')")
                self.prepare_chunk_meta(chunk_luid)
                self.chunks[chunk_luid].is_fresh = True
            except:
                print ("Could not finish moving '"+png_path+"' to '"+dest_png_path+"'")
        try:
            if (os.path.isfile(dest_genresult_path)):
                os.remove(dest_genresult_path)
            if self.is_save_output_ok:
                os.rename(genresult_path, dest_genresult_path)
                print("(moved to '"+dest_genresult_path+"')")
            else:
                if os.path.isfile(genresult_path):
                    os.remove(genresult_path)
        except:
            print ("Could not finish deleting/moving output")
        
        return result
        
    def check_players(self):
        self.chunkymap_data_path=os.path.join(self.website_root,"chunkymapdata")
        chunkymap_players_name = "players"
        chunkymap_players_path = os.path.join(self.chunkymap_data_path, chunkymap_players_name)
        htaccess_path = os.path.join(chunkymap_players_path,".htaccess")
        if not os.path.isdir(chunkymap_players_path):
            os.makedirs(chunkymap_players_path)
        if not os.path.isfile(htaccess_path):
            self.deny_http_access(chunkymap_players_path)

            players_path = os.path.join(self.world_path, "players")
            for dirname, dirnames, filenames in os.walk(players_path):
                for filename in filenames:
                    file_fullname = os.path.join(players_path,filename)
                    #print ("  EXAMINING "+filename)
                    badstart_string = "."
                    player_name = None
                    player_position = None
                    if (filename[:len(badstart_string)]!=badstart_string):
                        ins = open(file_fullname)
                        line = True
                        has_enough_data = False
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
                                        has_enough_data = True
                                        break
                        ins.close()
                        player_dest_path = os.path.join(chunkymap_players_path,filename+".yml")
                        if player_position is not None:
                            # mark chunk
                            tuple_noparen_pos_string = player_position.strip("() \n\r")
                            pos_strings = tuple_noparen_pos_string.split(",")
                            if len(pos_strings) == 3:
                                player_x = int(pos_strings[player_x])
                                player_y = int(pos_strings[player_y])
                                player_z = int(pos_strings[player_z])
                                chunk_x = int((float(player_x)/self.chunk_size))
                                chunk_y = int((float(player_y)/self.chunk_size))
                                chunk_z = int((float(player_z)/self.chunk_size))
                                chunk_luid = self.get_chunk_luid(chunk_x, chunk_z)
                                self.prepare_chunk_meta()
                                self.chunks[chunk_luid].is_player_here = True
                            else:
                                print("Player '"+filename+"' has bad position data--should be 3-length (x,y,z) in position value: "+str(pos_strings))
                                
                        if has_enough_data:
                            #if player_name!="singleplayer":
                            map_player_dict = self.get_dict_from_conf_file(player_dest_path,":")
                            if (map_player_dict is None) or (map_player_dict["position"]!=player_position):
                                outs = open(player_dest_path, 'w')
                                outs.write("name:"+player_name+"\n")  # python automatically uses correct newline for your os when you put "\n"
                                outs.write("position:"+player_position+"\n")
                                outs.close()        
    def is_player_at_luid(self, chunk_luid):
        result = False
        if chunk_luid in self.chunks.keys():
            result = self.chunks[chunk_luid].is_player_here
        return result
        
    def is_chunk_fresh(self, chunk_luid):
        result = False
        if chunk_luid in self.chunks.keys():
            result = self.chunks[chunk_luid].is_fresh
        return result

    def run(self):
        if os.path.isfile(self.mtmn_path) and os.path.isfile(self.colors_path):
            self.check_players()
            self.chunkymap_data_path=os.path.join(self.website_root,"chunkymapdata")
            yaml_name = "generated.yml"
            yaml_path = os.path.join(self.chunkymap_data_path, yaml_name)
            if not os.path.isdir(self.chunkymap_data_path):
                os.mkdir(self.chunkymap_data_path)

            htaccess_path = os.path.join(self.chunkymap_data_path,".htaccess")
            if not os.path.isdir(self.chunkymap_data_path):
                os.makedirs(self.chunkymap_data_path)
            if not os.path.isfile(htaccess_path):
                self.deny_http_access(self.chunkymap_data_path)
            
            mapvars = self.get_dict_from_conf_file(yaml_path,":")
            #is_testonly == (os_name=="windows")

            if mapvars is not None and set(['self.world_name']).issubset(mapvars):
                #print ("  (FOUND self.world_name)")
                if mapvars["self.world_name"] != self.world_name:
                    print ("REMOVING data since from different world (map '"+str(mapvars["self.world_name"])+"' is not '"+str(self.world_name)+"')...")
                    for dirname, dirnames, filenames in os.walk(self.chunkymap_data_path):
                        index = 0
                        for j in range(0,len(filenames)):
                            i = len(filenames) - 0 - 1
                            if filenames[i][0] == ".":
                                print ("  SKIPPING "+filenames[i])
                                filenames.remove_at(i)
                        for filename in filenames:
                            file_fullname = os.path.join(self.chunkymap_data_path,filename)
                            print ("  EXAMINING "+filename)
                            badstart_string = "chunk"
                            if (len(filename) >= len(badstart_string)) and (filename[:len(badstart_string)]==badstart_string):
                                os.remove(file_fullname)
                            elif filename==yaml_name:
                                os.remove(file_fullname)

            self.chunkx_min = 0
            self.chunkz_min = 0
            self.chunkx_max = 0
            self.chunkz_max = 0
            total_generated_count = 0

            newchunk_luid_list = list()
            outline_generates_count = 1
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
                            
                            is_player_here = self.is_player_at_luid(chunk_luid)
                            
                            is_render_needed = False
                            
                            if not self.is_chunk_fresh(chunk_luid):
                                if is_player_here:
                                    if self.is_genresult_marked(chunk_luid):
                                        if self.is_genresult_marked_empty(chunk_luid):
                                            is_render_needed = True
                                            print (chunk_luid+": RENDERING non-fresh marked empty chunk (player present in it)")
                                        else:
                                            print (chunk_luid+": SKIPPING non-fresh marked chunk (player present in it)")
                                    else:
                                        is_render_needed = True
                                        print (chunk_luid+": RENDERING non-fresh unmarked chunk (player present in it)")
                                else:
                                    if (not self.is_genresult_marked(chunk_luid)):
                                        is_render_needed = True
                                        print (chunk_luid+": RENDERING non-fresh unmarked chunk (skipped other checks since player not present in it)")
                                    else:
                                        print (chunk_luid+": SKIPPING non-fresh marked chunk (skipped other checks since player not present in it)")
                            else:
                                print (chunk_luid+": SKIPPING fresh chunk")
                                #if (not self.is_genresult_marked(chunk_luid)):
                                    #is_render_needed = True
                            
                            if is_render_needed:
                                if (self.render_chunk(x,z)):
                                    total_generated_count += 1
                                    outline_generates_count += 1
                            else:
                                if self.is_chunk_rendered_on_dest(chunk_luid):
                                    total_generated_count += 1
                                    outline_generates_count += 1
                                    png_path = self.get_chunk_image_path(chunk_luid)
                                    print(chunk_luid+": Skipping existing map tile file " + png_path + " (delete it to re-render)")
                                #elif is_empty_chunk:
                                    #print("Skipping empty chunk " + chunk_luid)
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
            is_changed = False
            if mapvars is None:
                print ("SAVING '" + yaml_path + "' since nothing was loaded or it did not exist")
                is_changed = True
            else:
                for this_key in new_map_dict.iterkeys():
                    if (this_key not in mapvars.keys()):
                        is_changed = True
                        print ("SAVING '" + yaml_path + "' since " + str(this_key) + " not in mapvars")
                        break
                    elif (str(mapvars[this_key]) != str(new_map_dict[this_key])):
                        is_changed = True
                        print ("SAVING '" + yaml_path + "' since new " + this_key + " value " + str(mapvars[this_key]) + " not same as saved value " + str(mapvars[this_key]) + "")
                        break
            if is_changed:
                outs = open(yaml_path, 'w')
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
                print ("(Not saving '"+yaml_path+"' since same value of each current variable is already in file as loaded)")
        else:
            print ("failed since this folder must contain colors.txt and minetestmapper-numpy.py")

def main():
    #args = parse_args()
    mtchunks = MTChunks()
    mtchunks.run()

if __name__ == '__main__':
    main()
