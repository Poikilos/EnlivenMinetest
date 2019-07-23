print("How to use: paste into a Blender Text Editor panel, select object, Run Script")

y_up = True
enable_minetest = True

import bpy
#from mathutils import Matrix
from mathutils import Vector
#from mathutils import Euler

ob1 = None
try:
    ob1 = obj.select_get()
except:
    # < 2.8
    ob1 = bpy.context.scene.objects.active


class MessageBox(bpy.types.Operator):
    bl_idname = "message.messagebox"
    bl_label = ""
    message = bpy.props.StringProperty(
        name = "message",
        description = "message",
        default = ''
    )

    def execute(self, context):
        self.report({'INFO'}, self.message)
        print(self.message)
        return {'FINISHED'}

    def invoke(self, context, event):
        return context.window_manager.invoke_props_dialog(self, width = 400)

    def draw(self, context):
        self.layout.label(self.message)
        self.layout.label("")
        #col = self.layout.column(align = True)
        #col.prop(context.scene, "my_string_prop")


bpy.utils.register_class(MessageBox)

#print(str(thisO))
#extents1 = ob1.dimensions.copy()
#if (extents1.x == 0.0) and (extents1.y == 0.0) and (extents1.z == 0.0) and (ob1.scale.x > 0.0):
#extents1.x = extents1.x / 10.0
#extents1.y = extents1.y / 10.0
#extents1.z = extents1.z / 10.0
loc1 = ob1.location
#loc1 = ob1.matrix_world.translation
#print(str(extents1))

#see https://blender.stackexchange.com/questions/8459/get-blender-x-y-z-and-bounding-box-with-script
#bbox_corners = [ob1.matrix_world * Vector(corner) for corner in ob1.bound_box]


#use ground as bottom
#if zMin < 0.0:
#    yMax -= yMin
#    yMin = 0.0

#print(
#    "    collisionbox = {{{:.2f}, {:.2f}, {:.2f}, {:.2f}, {:.2f}, {:.2f}}}".format(xMin, yMin, zMin, xMax, yMax, zMax)
#)

#see https://blender.stackexchange.com/questions/6139/how-to-iterate-through-all-vertices-of-an-object-that-contains-multiple-meshes
mesh = ob1.data
#print("mesh:" + str(mesh))
#print("hasattr(mesh, 'vertices'):" + str(hasattr(mesh, 'vertices')))]
xMin = None
if (mesh is not None) and (not hasattr(mesh, 'vertices')):
    print("--can't calculate collisionbox for skeleton")
elif mesh is not None:
    xMin = None
    yMin = None
    zMin = None
    xMax = None
    yMax = None
    zMax = None
    for vert in mesh.vertices:
        # switch y and z for Minetest (y-up)
        if (xMin is None) or (vert.co.x < xMin):
            xMin = vert.co.x
        if (xMax is None) or (vert.co.x > xMax):
            xMax = vert.co.x
        if (yMin is None) or (vert.co.y < yMin):
            yMin = vert.co.y
        if (yMax is None) or (vert.co.y > yMax):
            yMax = vert.co.y
        if (zMin is None) or (vert.co.z < zMin):
            zMin = vert.co.z
        if (zMax is None) or (vert.co.z > zMax):
            zMax = vert.co.z
    #print(str(extents1))
    #print("--by vertices (raw):")
    #print(
    #    "    collisionbox = {{{:.2f}, {:.2f}, {:.2f}, {:.2f}, {:.2f}, {:.2f}}}".format(xMin, yMin, zMin, xMax, yMax, zMax)
    #)
    xMax += ob1.location.x
    xMin += ob1.location.x
    yMax += ob1.location.y
    yMin += ob1.location.y
    zMax += ob1.location.z
    zMin += ob1.location.z
    print("--by vertices:")
else:
    extents1 = ob1.scale.copy()
    # Object is an empty, so scale up for Minetest
    extents1.x = extents1.x * 2.0
    extents1.y = extents1.y * 2.0
    extents1.z = extents1.z * 2.0
    xMin = loc1.x - extents1.x / 2.0
    xMax = loc1.x + extents1.x / 2.0
    yMin = loc1.y - extents1.y / 2.0
    yMax = loc1.y + extents1.y / 2.0
    zMin = loc1.z - extents1.z / 2.0
    zMax = loc1.z + extents1.z / 2.0
    print("--using empty object:")
#switch y and z for Minetest (y-up):
if enable_minetest:
    xMin /= 10.0
    xMax /= 10.0
    yMin /= 10.0
    yMax /= 10.0
    zMin /= 10.0
    zMax /= 10.0

msg = 'Size is not available. Make sure you have a mesh object selected.'

if xMin is not None:
    if y_up:
        tmp = yMin
        yMin = zMin
        zMin = tmp
        tmp = yMax
        yMax = zMax
        zMax = tmp
    msg = "    collisionbox = {{{:.2f}, {:.2f}, {:.2f}, {:.2f}, {:.2f}, {:.2f}}}".format(xMin, yMin, zMin, xMax, yMax, zMax)
    # print(msg)

bpy.ops.message.messagebox('INVOKE_DEFAULT', message = msg)

bpy.utils.unregister_class(MessageBox)
