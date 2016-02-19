#!/usr/bin/env python2
import os
import subprocess

# REQUIRES: see README.md

#minetestmapper-numpy.py calculates the region as follows:
#(XMIN','XMAX','ZMIN','ZMAX'), default = (-2000,2000,-2000,2000)
#sector_xmin,sector_xmax,sector_zmin,sector_zmax = numpy.array(args.region)/16
#sector_ymin = args.minheight/16
#sector_ymax = args.maxheight/16
#region server-specific options

full_render = False  # the preferred method of full render is deleting all files from the folder chunkymap_data_path such as /var/www/html/minetest/chunkymapdata (or chunkymap in current directory on Windows)

input_string = ""
username = "owner"
os_name="linux"
if (os.path.sep!="/"):
    os_name="windows"
#input_string = input("Which username contains minetest/util/minetestmapper-numpy.py (minetest not .minetest) ["+username+"]?")
if (len(input_string)>0):
    username = input_string

website_root="/var/www/html/minetest"
#input_string = input("What is the root folder of your minetest website ["+website_root+"]?")
if (len(input_string)>0):
    website_root = input_string

world_name = "FCAGameAWorld"
#input_string = input("What is the game name ["+world_name+"]")
if (len(input_string)>0):
    world_name = input_string
#region server-specific options
profiles_path = "/home"
if os_name=="windows":
    profiles_path = "C:\\Users"
profile_path = os.path.join(profiles_path, username)
#if (not os.path.isdir(profile_path)):
#    profile_path = os.path.join(profiles_path, "jgustafson")
dotminetest_path = os.path.join(profile_path,".minetest")
if (os_name=="windows"): dotminetest_path = "C:\\games\\Minetest"
worlds_path = os.path.join(dotminetest_path,"worlds")
world_path = os.path.join(worlds_path, world_name)
auto_chosen_world = False
if not os.path.isdir(world_path):
    #for item in os.walk(worlds_path):
    print "LOOKING FOR WORLDS IN " + worlds_path
    for dirname, dirnames, filenames in os.walk(worlds_path):
        index = 0
        for j in range(0,len(dirnames)):
            i = len(dirnames) - 0 - 1
            if dirnames[i][0] == ".":
                print "  SKIPPING "+dirnames[i]
                dirnames.remove_at(i)
        for subdirname in dirnames:
            print "  EXAMINING "+subdirname
            if (index == len(dirnames)-1):  # skip first one because the one on my computer is big
                world_name = subdirname
                world_path = os.path.join(dirname, subdirname) #  os.path.join(worlds_path, "try7amber")
                print "  CHOSE "+world_path
                auto_chosen_world = True
                break
            index += 1
        if auto_chosen_world:
            break
python_exe_path = "python"

try:
    alt_path = "C:\\python27\python.exe"
    if os.path.isfile(alt_path):
        python_exe_path = alt_path
except:
    pass  # do nothing, probably linux

mtmn_path = os.path.join( profile_path, "minetest/util/minetestmapper-numpy.py" )
colors_path = os.path.join( profile_path, "minetest/util/colors.txt" )
if os_name=="windows":
    mtmn_path = os.path.join(os.path.dirname(__file__), "minetestmapper-numpy.py")
    colors_path = os.path.join(os.path.dirname(__file__), "colors.txt")
    website_root = os.path.dirname(__file__)

class MTChunk:
    x = None
    z = None
    is_player_here = None

    def __init__(self):
        self.is_player_here = False


is_save_output_ok = True

def get_dict_from_conf_file(path,assignment_operator="="):
    results = None
    print "Checking "+str(path)+" for settings..."
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
                                result_name = line_strip[:ao_index]
                                result_value = line_strip[ao_index+1:]
                                print "   CHECKING... "+result_name+":"+result_value
                                results[result_name]=result_value
        ins.close()
    return results


def deny_http_access(dir_path):
    htaccess_name = ".htaccess"
    htaccess_path = os.path.join(dir_path, htaccess_name)
    outs = open(htaccess_path)
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
    

if os.path.isfile(mtmn_path) and os.path.isfile(colors_path):
    
    
    chunkymap_data_path=os.path.join(website_root,"chunkymapdata")
    yaml_name = "generated.yml"
    yaml_path = os.path.join(chunkymap_data_path, yaml_name)
    if not os.path.isdir(chunkymap_data_path):
        os.mkdir(chunkymap_data_path)
    chunkymap_players_name = "players"
    chunkymap_players_path = os.path.join(chunkymap_data_path, chunkymap_players_name)
    
    htaccess_path = os.path.join(chunkymap_data_path,".htaccess")
    if not os.path.isfile(htaccess_path):
        deny_http_access(chunkymap_data_path)
    htaccess_path = os.path.join(chunkymap_players_path,".htaccess")
    if not os.path.isfile(htaccess_path):
        deny_http_access(chunkymap_players_path)
    
    if not os.path.isdir(chunkymap_players_path):
        os.mkdir(chunkymap_players_path)
    players_path = os.path.join(world_path, "players")
    for dirname, dirnames, filenames in os.walk(players_path):
        for filename in filenames:
            file_fullname = os.path.join(players_path,filename)
            #print "  EXAMINING "+filename
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
                if has_enough_data:
                    #if player_name!="singleplayer":
                    map_player_dict = get_dict_from_conf_file(player_dest_path,":")
                    if (map_player_dict is None) or (map_player_dict["position"]!=player_position):
                        outs = open(player_dest_path, 'w')
                        outs.write("name:"+player_name+"\n")  # python automatically uses correct newline for your os when you put "\n"
                        outs.write("position:"+player_position+"\n")
                        outs.close()

    mapvars = get_dict_from_conf_file(yaml_path,":")
    #is_testonly == (os_name=="windows")

    if mapvars is not None and set(['world_name']).issubset(mapvars):
        #print "  (FOUND world_name)"
        if mapvars["world_name"] != world_name:
            print ("REMOVING data since from different world (map '"+str(mapvars["world_name"])+"' is not '"+str(world_name)+"')...")
            for dirname, dirnames, filenames in os.walk(chunkymap_data_path):
                index = 0
                for j in range(0,len(filenames)):
                    i = len(filenames) - 0 - 1
                    if filenames[i][0] == ".":
                        print "  SKIPPING "+filenames[i]
                        filenames.remove_at(i)
                for filename in filenames:
                    file_fullname = os.path.join(chunkymap_data_path,filename)
                    print "  EXAMINING "+filename
                    badstart_string = "chunk"
                    if (len(filename) >= len(badstart_string)) and (filename[:len(badstart_string)]==badstart_string):
                        os.remove(file_fullname)
                    elif filename==yaml_name:
                        os.remove(file_fullname)



    chunks = {}

    #region values to save to YAML
    chunk_size = 80
    chunkx_min = 0
    chunkz_min = 0
    chunkx_max = 0
    chunkz_max = 0
    total_generated_count = 0

    #values for command arguments:
    maxheight = 50
    minheight = -25
    pixelspernode = 1
    #ALSO save to YAML:
    #world_name
    #world_path
    #endregion values to save to YAML

    square_generates_count = 1
    while square_generates_count > 0:
        square_generates_count = 0
        for z in range (chunkz_min,chunkz_max+1):
            for x in range(chunkx_min,chunkx_max+1):
                #python ~/minetest/util/minetestmapper-numpy.py --region -1200 800 -1200 800 --drawscale --maxheight 100 --minheight -50 --pixelspernode 1 ~/.minetest/worlds/FCAGameAWorld ~/map.png
                #sudo mv ~/map.png /var/www/html/minetest/images/map.png

                #only generate the edges (since started with region 0 0 0 0) and expanding from there until no png is created:
                is_outline = (x==chunkx_min) or (x==chunkx_max) or (z==chunkz_min) or (z==chunkz_max)
                if is_outline:
                    chunk_luid = "x"+str(x)+"z"+str(z)
                    png_name = "chunk_"+chunk_luid+".png"
                    png_path = os.path.join(os.path.dirname(__file__), png_name)
                    x_min = x * chunk_size
                    x_max = x * chunk_size + chunk_size - 1
                    z_min = z * chunk_size
                    z_max = z * chunk_size + chunk_size - 1

                    cmd_suffix = ""
                    mapper_out_name = "chunk_"+chunk_luid+"_mapper_result.txt"
                    mapper_out_path = os.path.join(os.path.dirname(__file__), mapper_out_name)
                    if is_save_output_ok:
                        cmd_suffix = " > \""+mapper_out_path+"\""
                    #print "generating x = " + str(x_min) + " to " + str(x_max) + " ,  z = " + str(z_min) + " to " + str(z_max)
                    cmd_string = python_exe_path + " \""+mtmn_path + "\" --region " + str(x_min) + " " + str(x_max) + " " + str(z_min) + " " + str(z_max) + " --maxheight "+str(maxheight)+" --minheight "+str(minheight)+" --pixelspernode "+str(pixelspernode)+" \""+world_path+"\" \""+png_path+"\"" + cmd_suffix
                    dest_png_path = os.path.join(chunkymap_data_path, png_name)
                    dest_mapper_out_path = os.path.join(chunkymap_data_path, mapper_out_name)
                    is_empty_chunk = False
                    if os.path.isfile(dest_mapper_out_path):
                        if os.path.isfile(dest_png_path):
                            os.remove(dest_mapper_out_path)
                    if os.path.isfile(dest_mapper_out_path):
                        ins = open(dest_mapper_out_path)
                        line = True
                        while line:
                            line = ins.readline()
                            if line:
                                line_strip = line.strip()
                                if "data does not exist" in line_strip:
                                    is_empty_chunk = True
                                    break
                        ins.close()
                    if full_render or ((not os.path.isfile(dest_png_path)) and (not is_empty_chunk)):
                        print cmd_string
                        subprocess.call(cmd_string, shell=True)  # TODO: remember not to allow arbitrary command execution, which could happen if input contains ';' when using shell=True
                        if os.path.isfile(png_path):
                            total_generated_count += 1
                            square_generates_count += 1

                            try:
                                if (os.path.isfile(dest_png_path)):
                                    os.remove(dest_png_path)
                            except:
                                print "Could not finish deleting '"+dest_png_path+"'"
                            try:
                                os.rename(png_path, dest_png_path)
                                print("(moved to '"+dest_png_path+"')")
                            except:
                                print "Could not finish moving '"+png_path+"' to '"+dest_png_path+"'"
                        try:
                            if (os.path.isfile(dest_mapper_out_path)):
                                os.remove(dest_mapper_out_path)
                            if is_save_output_ok:
                                os.rename(mapper_out_path, dest_mapper_out_path)
                                print("(moved to '"+dest_mapper_out_path+"')")
                            else:
                                if os.path.isfile(mapper_out_path):
                                    os.remove(mapper_out_path)
                        except:
                            print "Could not finish deleting/moving output"
                    else:
                        if os.path.isfile(dest_png_path):
                            total_generated_count += 1
                            square_generates_count += 1
                            print("Skipping existing map tile file " + png_name + " (delete it to re-render)")
                        elif is_empty_chunk:
                            print("Skipping empty chunk " + chunk_luid + " since not full_render")
            print ""  # blank line before next z so output is human readable
        chunkx_min -= 1
        chunkz_min -= 1
        chunkx_max += 1
        chunkz_max += 1
    #end while square outline (1-chunk-thick outline) generated any png files
    outs = open(yaml_path, 'w')
    outs.write("world_name:"+str(world_name) + "\n")
    outs.write("chunk_size:"+str(chunk_size) + "\n")
    outs.write("pixelspernode:"+str(pixelspernode) + "\n")
    outs.write("chunkx_min:"+str(chunkx_min) + "\n")
    outs.write("chunkz_min:"+str(chunkz_min) + "\n")
    outs.write("chunkx_max:"+str(chunkx_max) + "\n")
    outs.write("chunkz_max:"+str(chunkz_max) + "\n")
    #values for command arguments:
    outs.write("maxheight:"+str(maxheight) + "\n")
    outs.write("minheight:"+str(minheight) + "\n")
    #ALSO save to YAML:
    outs.write("world_path:"+str(world_path) + "\n")
    outs.write("chunkymap_data_path:"+str(chunkymap_data_path) + "\n")
    outs.write("total_generated_count:"+str(total_generated_count) + "\n")

    outs.close()
else:
    print "failed since this folder must contain colors.txt and minetestmapper-numpy.py"
