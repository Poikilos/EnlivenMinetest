import subprocess
import os
from minetestinfo import *
#python_exe_path is from:
from pythoninfo import *
#from PIL import Image, ImageDraw, ImageFont, ImageColor
from PIL import Image

class ChunkymapOfflineRenderer:

    minetestmapper_numpy_path = None
    minetestmapper_custom_path = None
    minetestmapper_py_path = None
    backend_string = None
    world_path = None
    world_name = None

    def __init__(self):

        self.backend_string = get_world_var("backend")

        #region the following is also in singleimage.py
        self.minetestmapper_numpy_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "minetestmapper-numpy.py")
        self.minetestmapper_custom_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "minetestmapper-expertmm.py")
        self.minetestmapper_py_path = self.minetestmapper_numpy_path
        #if (self.backend_string!="sqlite3"):
            # minetestmapper-numpy had trouble with leveldb but this fork has it fixed so use numpy always always instead of running the following line
            # self.minetestmapper_py_path = self.minetestmapper_custom_path
        print("Chose image generator script: "+self.minetestmapper_py_path)
        if not os.path.isfile(self.minetestmapper_py_path):
            print("ERROR: script does not exist, so exiting "+__file__+".")
            sys.exit(2)
        self.colors_path = os.path.join(os.path.dirname(os.path.abspath(self.minetestmapper_py_path)), "colors.txt")
        if not os.path.isfile(self.colors_path):
            print("ERROR: missing '"+self.colors_path+"', so exiting "+__file__+".")
            sys.exit(2)
        self.world_path = minetestinfo.get_var("primary_world_path")
        if not os.path.isdir(self.world_path):
            print("ERROR: missing world '"+self.world_path+"', so exiting "+__file__+".")
            sys.exit(2)
        else:
            self.world_name = os.path.basename(self.world_path)
        #endregion the following is also in singleimage.py

    def RenderSingleImage(self):
        genresults_folder_path = os.path.join( os.path.join(os.path.dirname(os.path.abspath(__file__)), "chunkymap-genresults"), self.world_name)
        if not os.path.isdir(genresults_folder_path):
            os.makedirs(genresults_folder_path)
        genresult_path = os.path.join(genresults_folder_path, "singleimage"+genresult_name_closer_string)
        gen_error_path = os.path.join(genresults_folder_path, "singleimage"+gen_error_name_closer_string)
        cmd_suffix = " 1> \""+genresult_path+"\""
        cmd_suffix += " 2> \""+gen_error_path+"\""

        #blank since singleimage mode:
        #geometry_string = str(min_x)+":"+str(min_z)+"+"+str(int(max_x)-int(min_x)+1)+"+"+str(int(max_z)-int(min_z)+1)  # +1 since max-min is exclusive and width must be inclusive for minetestmapper.py
        #geometry_param = " --geometry "+geometry_string
        geometry_param = ""
        #expertmm_region_string = str(min_x) + ":" + str(max_x) + "," + str(min_z) + ":" + str(max_z)

        #cmd_no_out_string = python_exe_path+" "+self.minetestmapper_py_path+" --bgcolor '"+self.FLAG_EMPTY_HEXCOLOR+"' --input \""+minetestinfo.get_var("primary_world_path")+"\" --geometry "+geometry_string+" --output \""+tmp_png_path+"\""
        png_name = "singleimage.png"

        tmp_png_path = os.path.join(genresults_folder_path, png_name)
        squote = ""
        if os_name!="windows":
            squote = "'"
        io_string = " --input \""+self.world_path+"\" --output \""+tmp_png_path+"\""
        if "numpy" in self.minetestmapper_py_path:
            io_string = " \""+self.world_path+"\" \""+tmp_png_path+"\""
            #geometry_param = " --region " + str(min_x) + " " + str(max_x) + " " + str(min_z) + " " + str(max_z)
        cmd_no_out_string = python_exe_path+" "+self.minetestmapper_py_path+" --bgcolor "+squote+FLAG_EMPTY_HEXCOLOR+squote+io_string
        cmd_string = cmd_no_out_string + cmd_suffix
        print("")
        print("")
        print("Running")
        print("    "+cmd_string)
        print("    # (this may take a while...)")
        if os.path.isfile(tmp_png_path):
            os.remove(tmp_png_path)
        subprocess.call(cmd_string, shell=True)
        final_png_path = tmp_png_path
        www_chunkymapdata_path = os.path.join(minetestinfo.get_var("www_minetest_path"), "chunkymapdata")
        www_chunkymapdata_worlds_path = os.path.join(www_chunkymapdata_path, "worlds")
        www_chunkymapdata_world_path = os.path.join(www_chunkymapdata_worlds_path, self.world_name)

        is_locked = False
        if os.path.isfile(gen_error_path):
            ins = open(gen_error_path, 'r')
            line = True
            while line:
                line = ins.readline()
                if line:
                    line_lower = line.lower()
                    if (" lock " in line_lower) or ("/lock " in line_lower):
                        is_locked = True
                        lock_line = line
                        result = None
                        break
            ins.close()

        if os.path.isfile(tmp_png_path):
            if not os.path.isdir(www_chunkymapdata_world_path):
                os.makedirs(www_chunkymapdata_world_path)
            if minetestinfo.contains("www_minetest_path"):
                dest_png_path = os.path.join(www_chunkymapdata_world_path, png_name)
                if os.path.isfile(dest_png_path):
                    os.remove(dest_png_path)
                os.rename(tmp_png_path, dest_png_path)
                final_png_path = dest_png_path
            print("Png image saved to:")
            print("  "+final_png_path)
            print("Converting to jpg...")
            pngim = Image.open(final_png_path)
            #jpgim = Image.new('RGB', pngim.size, (0, 0, 0))
            #jpgim.paste(pngim.convert("RGB"), (0,0,pngim.size[0],pngim.size[0]))
            jpg_name = "singleimage.jpg"
            dest_jpg_path = os.path.join(www_chunkymapdata_world_path, jpg_name)
            if os.path.isfile(dest_jpg_path):
                os.remove(dest_jpg_path)
                if not os.path.isfile(dest_jpg_path):
                    print("  removed old '"+dest_jpg_path+"'")
                else:
                    print("  failed to remove'"+dest_jpg_path+"'")
            #jpgim.save(dest_jpg_path)
            pngim.save(dest_jpg_path, 'JPEG')
            if os.path.isfile(dest_jpg_path):
                print("jpg image saved to:")
                print("  "+dest_jpg_path)
            else:
                print("Could not write '"+dest_jpg_path+"'")
            if os.path.isfile(genresult_path):
                print("Results:")
                print("  "+genresult_path)
                mtchunk = MTChunk()
                mtchunk.set_from_genresult(genresult_path)
                mtchunk.metadata["is_traversed"] = True
                dest_yaml_name = "singleimage.yml"
                dest_yaml_path = os.path.join(www_chunkymapdata_world_path, dest_yaml_name)
                mtchunk.save_yaml(dest_yaml_path)
        else:

            print("No image could be generated from '"+self.world_path+"'")
            if is_locked:
                print("(database is locked--shutdown server first or try generator.py to render chunks individually).")

cmor = ChunkymapOfflineRenderer()
cmor.RenderSingleImage()
