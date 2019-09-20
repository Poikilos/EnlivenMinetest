print("How to use: paste into a Blender Text Editor panel, select"
      " object, Run Script")

y_up = True
enable_minetest = False


import bpy
# from mathutils import Matrix
from mathutils import Vector
# from mathutils import Euler

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
        return context.window_manager.invoke_props_dialog(self,
                                                          width=400)

    def draw(self, context):
        self.layout.label(self.message)
        self.layout.label("")
        # col = self.layout.column(align = True)
        # col.prop(context.scene, "my_string_prop")


bpy.utils.register_class(MessageBox)

msgSuffix = ""

mesh = None
if ob1 is not None:
    mesh = ob1.data

if ob1 is None:
    msg = "Nothing is selected."
    bpy.ops.message.messagebox('INVOKE_DEFAULT', message = msg)
if (mesh is not None) and (not hasattr(mesh, 'vertices')):
    msg = "Collision box for armatures cannot be calculated."
    bpy.ops.message.messagebox('INVOKE_DEFAULT', message = msg)
else:
    # extents1 = ob1.dimensions.copy()
    obj1Loc = ob1.location

    # See https://blender.stackexchange.com/questions/8459/get-blender-x-y-z-and-bounding-box-with-script
    # bbox_corners = [ob1.matrix_world * Vector(corner) for corner in ob1.bound_box]

    # use ground as bottom (don't do this--it is not the Minetest way)
    # if zMin < 0.0:
    #     yMax -= yMin
    #     yMin = 0.0

    print("    collisionbox = {{{:.2f}, {:.2f}, {:.2f}, {:.2f}, {:.2f},"
          " {:.2f}}}".format(xMin, yMin, zMin, xMax, yMax, zMax))

    # See https://blender.stackexchange.com/questions/6139/how-to-iterate-through-all-vertices-of-an-object-that-contains-multiple-meshes
    # print("mesh:" + str(mesh))
    # print("hasattr(mesh, 'vertices'):"
          # + str(hasattr(mesh, 'vertices')))]
    xMin = None
    if mesh is not None:
        xMin = None
        yMin = None
        zMin = None
        xMax = None
        yMax = None
        zMax = None
        wm = ob1.matrix_world
        for vert in mesh.vertices:
            # This matrix multiplication is NOT transitive.
            try:
                loc = wm @ vert.co
            except TypeError:
                loc = wm * vert.co  # Blender <2.8
            # switch y and z for Minetest (y-up)
            if (xMin is None) or (loc.x < xMin):
                xMin = loc.x
            if (xMax is None) or (loc.x > xMax):
                xMax = loc.x
            if (yMin is None) or (loc.y < yMin):
                yMin = loc.y
            if (yMax is None) or (loc.y > yMax):
                yMax = loc.y
            if (zMin is None) or (loc.z < zMin):
                zMin = loc.z
            if (zMax is None) or (loc.z > zMax):
                zMax = loc.z
        # print(str(extents1))
        # print("--by vertices (raw):")
        print("    collisionbox = {{{:.2f}, {:.2f}, {:.2f}, {:.2f},"
              " {:.2f}, {:.2f}}}".format(xMin, yMin, zMin, xMax, yMax,
                                         zMax))

        # Use ob1.matrix_world (above) instead of incrementing
        # ob1.location.x, y, and z

        newNamePrefix = "Empty.EDGE." + ob1.name
        i = 0
        wm = ob1.matrix_world
        for vert in mesh.vertices:
            newName = newNamePrefix + "." + str(i)
            try:
                loc = mat @ vert.co  # NOT transitive
            except TypeError:
                loc = mat * vert.co  # Blender <2.8
            isFar = False
            if loc.x == xMax or loc.y == yMax or loc.z == zMax:
                isFar = True
            elif loc.x == xMin or loc.y == yMin or loc.z == zMin:
                isFar = True
            if isFar:
                pass
                # result = bpy.ops.object.add(type='EMPTY', radius=.25,
                                            # location=loc);
                # NOTE: result is merely {'FINISHED'}
                # print("{:.2f}, {:.2f}, {:.2f}".format(loc.x, loc.y,
                                                      # loc.z))

                bpy.ops.object.add_named(name=newName, type='EMPTY',
                                         radius=.25, location=loc)
            i += 1
    else:
        extents1 = ob1.scale.copy()
        # Object is an empty, so scale up for Minetest
        extents1.x = extents1.x * 2.0
        extents1.y = extents1.y * 2.0
        extents1.z = extents1.z * 2.0
        xMin = obj1Loc.x - extents1.x / 2.0
        xMax = obj1Loc.x + extents1.x / 2.0
        yMin = obj1Loc.y - extents1.y / 2.0
        yMax = obj1Loc.y + extents1.y / 2.0
        zMin = obj1Loc.z - extents1.z / 2.0
        zMax = obj1Loc.z + extents1.z / 2.0
        msgSuffix = " (using Empty object's scale)"
        # print("--using empty object:")
    # switch y and z for Minetest (y-up):
    if enable_minetest:
        xMin /= 10.0
        xMax /= 10.0
        yMin /= 10.0
        yMax /= 10.0
        zMin /= 10.0
        zMax /= 10.0

    msg = ('Size is not available. Make sure you have a mesh object'
           ' selected.')

    if xMin is not None:
        if y_up:
            tmp = yMin
            yMin = zMin
            zMin = tmp
            tmp = yMax
            yMax = zMax
            zMax = tmp
        msg = ("    collisionbox = {{{:.2f}, {:.2f}, {:.2f}, {:.2f},"
               " {:.2f}, {:.2f}}}".format(xMin, yMin, zMin, xMax, yMax,
                                          zMax))
        msg += msgSuffix
        # if enable_minetest:
            # msg += "  -- *10"
    print(msg)

    bpy.ops.message.messagebox('INVOKE_DEFAULT', message=msg)

# Unregistering before user clicks the MessageBox will crash Blender!
# bpy.utils.unregister_class(MessageBox)
