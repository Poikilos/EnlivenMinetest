
'''
Count the number of objects (used meshes) in the scene.
For b3d files, instead use Poikilos' fork of b3view:
b3view Snail.b3d --count-meshes --exit

Requires: Blender (>=2.8)


Usage:
- Paste this script into a new text file in a text editor panel
  (If you don't know how to get there, see the HowTo file in
  the utilities/blender directory at
  github.com/poikilos/EnlivenMinetest).
- "Text", "Run Script".
'''
import bpy

def ShowMessageBox(message="", title="Count", icon='INFO'):
    def draw(self, context):
        self.layout.label(text=message)
    bpy.context.window_manager.popup_menu(draw, title=title, icon=icon)

context = bpy.context
count = 0
# If there ARE objects selected then act on all objects
if bpy.context.selected_objects != []:
    for obj in bpy.context.selected_objects:
        print(obj.name, obj, obj.type)
        if obj.type == 'MESH':
            print("&gt;&gt;&gt;&gt;", obj.name)
            count += 1


# If there are NO objects selected then act on all objects
if bpy.context.selected_objects == []:
    print('selected:')
    for obj in bpy.context.scene.objects:
        print(obj.name, obj, obj.type)
        if obj.type == 'MESH':
            print("&gt;&gt;&gt;&gt;", obj.name)
            count += 1

ShowMessageBox(str(count))
print("count:{}".format(count))
