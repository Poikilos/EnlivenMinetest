#!/usr/bin/env python

# collisionbox Lua generator
# 1. Select a mob mesh or an Empty
# 2. Press the "Run Script" button below
# - The script copies the collisionbox the the clipboard.
# - An 'Empty' with the object's name will appear,
#   which visually represents the collisionbox
#   (which MUST be symmetrical on horizontal axes and
#   centered at 0,0,0 for Minetest, since
#   collision boxes to not turn).
# 3. To adjust, scale the Empty.collisionbox.* object
#    in Blender then repeat steps 1-2. To keep the Empty
#    symmetrical for Minetest, scale ONLY with one
#    of the following hotkey sequences (with
#    the mouse pointer in the 3D View):
#    - 's'
#    - 's', 'z'
#    - 's', "shift z"

print("How to use: Paste this script into a Blender"
      " Text Editor panel, select an object,"
      " press the 'Run Script' button")

y_up = True
enable_minetest = True
enable_lowest_h = False
enable_center_h = False
if enable_minetest:
    enable_lowest_h = True
    enable_center_h = True

hs = (0, 1)  # horizontal axis indices
v = 2  # vertical axis index
# Do NOT swap until end.
#if y_up:
#    hs = (0, 2)
#    v = 1

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
        # print(self.message)
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
elif (mesh is not None) and (not hasattr(mesh, 'vertices')):
    msg = "Collision box for armatures cannot be calculated."
    bpy.ops.message.messagebox('INVOKE_DEFAULT', message = msg)
else:
    # extents1 = ob1.dimensions.copy()
    obj1Loc = ob1.location

    # See https://blender.stackexchange.com/questions/8459/get-blender-x-y-z-and-bounding-box-with-script
    # bbox_corners = [ob1.matrix_world * Vector(corner) for corner in ob1.bound_box]


    # See https://blender.stackexchange.com/questions/6139/how-to-iterate-through-all-vertices-of-an-object-that-contains-multiple-meshes
    # print("mesh:" + str(mesh))
    # print("hasattr(mesh, 'vertices'):"
          # + str(hasattr(mesh, 'vertices')))]
    mins = [None, None, None]  # minimums; in outer scope for checks.
    maxes = [None, None, None]  # minimums; in outer scope for checks.
    if mesh is not None:
        wm = ob1.matrix_world
        for vert in mesh.vertices:
            # This matrix multiplication is NOT transitive.
            try:
                loc = wm @ vert.co
            except TypeError:
                loc = wm * vert.co  # Blender <2.8
            # NOTE: swap y and z for Minetest (y-up) LATER
            coords = (loc.x, loc.y, loc.z)
            for i in range(3):
                if (mins[i] is None) or (coords[i] < mins[i]):
                    mins[i] = coords[i]
                if (maxes[i] is None) or (coords[i] > maxes[i]):
                    maxes[i] = coords[i]
        # print(str(extents1))
        # print("--by vertices (raw):")
        # print("    collisionbox = {{{:.2f}, {:.2f}, {:.2f}, {:.2f},"
              # " {:.2f}, {:.2f}}}".format(mins[0], mins[2], mins[1],
                                         # maxes[0], maxes[2], maxes[1]))

        # Use ob1.matrix_world (above) instead of incrementing
        # ob1.location.x, y, and z

        # newNamePrefix = "Empty.EDGE." + ob1.name
        # i = 0
        # wm = ob1.matrix_world
        # for vert in mesh.vertices:
            # newName = newNamePrefix + "." + str(i)
            # # This matrix multiplication is NOT transitive.
            # try:
                # loc = wm @ vert.co
            # except TypeError:
                # loc = wm * vert.co  # Blender <2.8
            # isFar = False
            # if loc.x == maxes[0] or loc.y == maxes[1] or loc.z == maxes[2]:
                # isFar = True
            # elif loc.x == mins[0] or loc.y == mins[1] or loc.z == mins[2]:
                # isFar = True
            # if isFar:
                # pass
                # # result = bpy.ops.object.add(type='EMPTY', radius=.25,
                                            # # location=loc)
                # # NOTE: result is merely {'FINISHED'}
                # # print("{:.2f}, {:.2f}, {:.2f}".format(loc.x, loc.y,
                                                      # # loc.z))

                # bpy.ops.object.add_named(name=newName, type='EMPTY',
                                         # radius=.25, location=loc)
            # i += 1
    else:
        extents1 = ob1.scale.copy()
        # Object is an empty, so scale up for Minetest
        extents1.x = extents1.x * (ob1.empty_draw_size * 2.0)
        extents1.y = extents1.y * (ob1.empty_draw_size * 2.0)
        extents1.z = extents1.z * (ob1.empty_draw_size * 2.0)
        mins[0] = obj1Loc.x - extents1.x / 2.0
        maxes[0] = obj1Loc.x + extents1.x / 2.0
        mins[1] = obj1Loc.y - extents1.y / 2.0
        maxes[1] = obj1Loc.y + extents1.y / 2.0
        mins[2] = obj1Loc.z - extents1.z / 2.0
        maxes[2] = obj1Loc.z + extents1.z / 2.0
        msgSuffix = " (using Empty object's scale)"
        # print("--using empty object:")

    # use ground as bottom (don't do this--it is not the Minetest way)
    # if mins[2] < 0.0:
    #     maxes[1] -= mins[1]
    #     mins[1] = 0.0

    # print("    collisionbox = {{{:.2f}, {:.2f}, {:.2f}, {:.2f}, {:.2f},"
          # " {:.2f}}}".format(mins[0], mins[1], mins[2], maxes[0], maxes[1], maxes[2]))
    sizes = [None, None, None]
    centers = [None, None, None]
    for i in range(3):
        sizes[i] = maxes[i] - mins[i]
        centers[i] = mins[i] + sizes[i] / 2.0

    if enable_lowest_h:
        # OK to use z as up, since will y&z will be swapped if y_up
        hSize = None
        for i in range(len(hs)):
            axis_i = hs[i]
            if (hSize is None) or (sizes[axis_i] < hSize):
                hSize = sizes[axis_i]
        for i in range(len(hs)):
            axis_i = hs[i]
            sizes[axis_i] = hSize
            mins[axis_i] = centers[axis_i] - hSize / 2
            maxes[axis_i] = mins[axis_i] + hSize

    if enable_center_h:
        for i in range(len(hs)):
            axis_i = hs[i]
            centers[i] = 0
            mins[axis_i] = centers[axis_i] - sizes[axis_i] / 2
            maxes[axis_i] = mins[axis_i] + sizes[axis_i]

    loc = (centers[0], centers[1], centers[2])
    bpy.ops.object.add(type='EMPTY', radius=.5, location=loc)
    collisionboxName = "Empty.collisionbox." + ob1.name
    newEmpty = bpy.context.scene.objects.active
    newEmpty.name = collisionboxName
    newEmpty.location = (centers[0], centers[1], centers[2])
    newEmpty.empty_draw_type = 'CUBE'
    # newEmpty.empty_draw_size = (sizes[0], sizes[1], sizes[2])
    # newEmpty.dimensions = (sizes[0], sizes[1], sizes[2])
    # newEmpty.scale = (sizes[0]/2.0, sizes[1]/2.0, sizes[2]/2.0)
    newEmpty.scale = (sizes[0], sizes[1], sizes[2])

    if enable_minetest:
        for i in range(3):
            mins[i] /= 10.0
            maxes[i] /= 10.0

    msg = ('Size is not available. Make sure you have a mesh object'
           ' selected.')

    if mins[0] is not None:
        # swap y and z for Minetest (y-up):
        if y_up:
            tmp = mins[1]
            mins[1] = mins[2]
            mins[2] = tmp
            tmp = maxes[1]
            maxes[1] = maxes[2]
            maxes[2] = tmp
        msg = ("    collisionbox = {{{:.2f}, {:.2f}, {:.2f}, {:.2f},"
               " {:.2f}, {:.2f}}}".format(mins[0], mins[1], mins[2],
                                          maxes[0], maxes[1], maxes[2]))
        if len(msgSuffix) > 0:
            msgSuffix = "  -- " + msgSuffix
        bpy.context.window_manager.clipboard = msg + msgSuffix
        msg += " --copied to clipboard"
        # if enable_minetest:
            # msg += "  -- *10"
    print(msg)

    bpy.ops.message.messagebox('INVOKE_DEFAULT', message=msg)

# Unregistering before user clicks the MessageBox will crash Blender!
# bpy.utils.unregister_class(MessageBox)
