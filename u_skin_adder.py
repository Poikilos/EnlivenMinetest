import os
#from PIL import Image, ImageDraw, ImageFont, ImageColor
from expertmm import *
from minetestinfo import *  #paths and FLAG_EMPTY_HEXCOLOR = "#010000"
from PIL import Image, ImageDraw, ImageFont, ImageColor

u_skins_mod_path = "C:\\Users\\jgustafson\\Desktop\\Backup\\fcalocal\\usr\\local\\share\\minetest\\games\\fca_game_a\\mods\\u_skins\\u_skins"
if not os.path.isdir(u_skins_mod_path):
    print("Looking for u_skins mod in u_skins modpack...")
    u_skins_mod_path = os.path.join(  os.path.join( os.path.join(game_path, "mods"), "u_skins" ),  "u_skins"  )  # get the u_skins mod in the u_skins modpack
    print("  trying '"+u_skins_mod_path+"'")
meta_path = os.path.join(u_skins_mod_path,"meta")
textures_path = os.path.join(u_skins_mod_path,"textures")
in_path = "C:\\Users\\jgustafson\\Downloads\\skins-to-add"
image_prefix = "character_"
preview_suffix = "_preview"

default_license = "CC BY-SA 3.0"

if not os.path.isdir(in_path):
    in_path = "."
    print("Looking for new textures in current directory")

png_count = 0

class RectTransferInfo:
    source_rect_tuple = None
    dest_rect_tuple = None
    flip_h = None
    
    def __init__(self, source_rect_tuple, dest_rect_tuple, flip_h):
        self.flip_h = flip_h
        self.source_rect_tuple = source_rect_tuple
        self.dest_rect_tuple = dest_rect_tuple
    
rect_trans_list = list()
rect_trans_list.append(RectTransferInfo((8,8,8,8),(4,0,8,8),False))  # face
rect_trans_list.append(RectTransferInfo((20,20,8,12),(4,8,8,12),False))  # shirt
#rect_trans_list.append(RectTransferInfo((44,28,4,4),(0,16,4,4),False))  # hand.r
#rect_trans_list.append(RectTransferInfo((44,28,4,4),(12,16,4,4),True))  # hand.l (True since must be flipped manually)
rect_trans_list.append(RectTransferInfo((44,20,4,12),(0,8,4,12),False))  # arm.r
rect_trans_list.append(RectTransferInfo((44,20,4,12),(12,8,4,12),True))  # arm.l (True since on hands, left one must be flipped manually)
rect_trans_list.append(RectTransferInfo((4,20,4,12),(8,20,4,12),False))  # leg.l
rect_trans_list.append(RectTransferInfo((4,20,4,12),(4,20,4,12),True))  # leg.r (True since on legs, right one must be flipped manually)
#yes, the flipping is different for leg vs arm

image_size = (64,32)
preview_size = (16,32)

class USkinInfo:
    author_string = None
    name_string = None
    license_name_string = None
    
    #region temp
    source_image_path = None
    #endregion temp
    
    def __init__(self):
        pass
        
    def set_from_skindb_skin_file_path(self, file_path, license_name_string):
        self.source_image_path = file_path
        file_name = os.path.basename(self.source_image_path)
        self.license_name_string=license_name_string
        noext_name = file_name
        dot_index = file_name.rfind(".")
        if dot_index>=0:
            noext_name = file_name[:dot_index]
        by_string = "_by_"
        by_index = noext_name.rfind(by_string)
        print("noext_name:"+noext_name)
        if by_index>=0:
            self.author_string = noext_name[by_index+len(by_string):]
            self.name_string = noext_name[:by_index]
        else:
            self.author_string = "<unknown>"
            self.name_string = noext_name
            
    def print_dump(self, min_indent):
        print(min_indent+"author_string:"+self.author_string)
        print(min_indent+"name_string:"+self.name_string)
        print(min_indent+"author_string:"+self.license_name_string)
        
    def _save_metadata(self, metadata_file_path):
        outs = open(metadata_file_path, 'w')
        outs.write(self.author_string+"\n")
        outs.write(self.name_string+"\n")
        outs.write(self.license_name_string+"\n")
        outs.close()
        
    
    def push_next_skin_file(self):
        os.listdir(textures_path)
        this_index = 1
        while os.path.isfile( get_png_path_from_index(this_index) ):
            this_index += 1
        #image_name = get_png_name_from_index(this_index)
        image_path = get_png_path_from_index(this_index)
        metadata_name = get_metadata_name_from_index(this_index)
        metadata_path = os.path.join(meta_path, metadata_name)
        #preview_name = get_preview_name_from_index(this_index)
        preview_path = get_preview_path_from_index(this_index)
        print("saving to image_path:"+image_path)
        print("saving to preview_path:"+preview_path)
        print("saving to metadata_path:"+metadata_path)
        #actually save the skin and metadata files:
        print("Not yet implemented.")
        self.print_dump("  ")
        
        preview_im = Image.new("RGBA", preview_size, "#000000")
        fill_image_with_transparency(preview_im)
        skin_im = Image.open(open(self.source_image_path, 'rb'))  # double-open to make sure file is finished writing
        #NOTE: PIL automatically closes, otherwise you can do something like https://bytes.com/topic/python/answers/24308-pil-do-i-need-close
        #fp = open(file_name, "rb")
        #im = Image.open(fp) # open from file object
        #im.load() # make sure PIL has read the data
        #fp.close()
        for rect_trans in rect_trans_list:
            partial_im = skin_im.crop(rect_trans.source_rect_tuple)
            left, top, right, bottom = rect_trans.dest_rect_tuple
            preview_im.paste(partial_im, (left, top))
        
        preview_im.save(preview_path)
        print("Saved preview to '"+preview_path+"'")
        print("")

def fill_image_with_transparency(im):
    #modified version of: unutbu. "Python PIL: how to make area transparent in PNG? (answer 7 Dec 2010 at 19:08)" <http://stackoverflow.com/questions/4379978/python-pil-how-to-make-area-transparent-in-png>. 7 Dec 2010. 8 Apr 2016.
    #who cited http://stackoverflow.com/questions/890051/how-do-i-generate-circular-thumbnails-with-pil
    #import Image
    #import ImageDraw
    #im = Image.open("image.png")
    #transparent_area = (50,80,100,200)
    transparent_area = (0,0,im.size[0],im.size[1])

    mask=Image.new('L', im.size, color=255)
    draw=ImageDraw.Draw(mask)
    
    draw.rectangle(transparent_area, fill=0)
    im.putalpha(mask)
    #im.save('/tmp/output.png')

def get_png_path_from_index(this_index):
    return os.path.join(textures_path, get_png_name_from_index(this_index))

def get_png_name_from_index(this_index):
    return image_prefix+str(this_index)+".png"

def get_preview_path_from_index(this_index):
    return os.path.join(textures_path, get_preview_name_from_index(this_index))

def get_preview_name_from_index(this_index):
    return image_prefix+str(this_index)+preview_suffix+".png"

def get_metadata_name_from_index(this_index):
    return image_prefix+str(this_index)+".txt"

if os.path.isdir(meta_path):
    if os.path.isdir(textures_path):
        if os.path.isdir(in_path):
            folder_path = in_path
            for sub_name in os.listdir(folder_path):
                sub_path = os.path.join(folder_path,sub_name)
                if os.path.isfile(sub_path):
                    if (sub_name[:1]!="."):
                        if len(sub_name)>4 and sub_name[-4:]==".png":
                            this_usi = USkinInfo()
                            this_usi.set_from_skindb_skin_file_path(sub_path, default_license)
                            this_usi.push_next_skin_file()
        else:
            print("ERROR: Failed to get new texture files since in_path does not exist:'"+in_path+"'")
    else:
        print("ERROR: missing textures_path (tried '"+textures_path+"')")
else:
    print("ERROR: missing meta_path (tried '"+meta_path+"')")
    
input("Press return to exit.")
