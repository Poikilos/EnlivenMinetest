import bpy
from mathutils import Vector
from math import degrees
# bpy.ops.wm.tool_set_by_id(name="builtin.scale")
#clear scene, make mesh
#bpy.ops.object.mode_set(mode = 'OBJECT')
#bpy.ops.object.select_all(action='SELECT')
#bpy.ops.object.delete(use_global=False)
#bpy.ops.mesh.primitive_cube_add(size=2, enter_editmode=False, align='WORLD', location=(0, 0, 0), rotation=(1.5708, 1.5708, 0))
#obj = bpy.data.objects["Cube"]
obj = bpy.context.object

#select vertex
obj = bpy.context.active_object
bpy.ops.object.mode_set(mode = 'EDIT')
bpy.ops.mesh.select_mode(type="VERT")
#bpy.ops.mesh.select_mode(type="EDGE")
# bpy.ops.mesh.select_mode(type="FACE")
bpy.ops.mesh.select_all(action = 'DESELECT')
bpy.ops.object.mode_set(mode = 'OBJECT')
# for i in range(len(bpy.context.object.data.vertices)):
front_normal = Vector((0, 0, 1))
# ^ I'm not sure why this works, but it is probably
#   from using diff_quat oddly below.
for i in range(len(obj.data.vertices)):
    obj.data.vertices[i].select = False
    v = obj.data.vertices[i]  # MeshVertex
    vn = v.normal
    # v.select_set(False)  # deprecated
    diff_quat = front_normal.rotation_difference(vn)
    # ^ returns a quaternion (magnitude 1)
    axis, rad = diff_quat.to_axis_angle()
    deg = degrees(rad)
    if deg > 90.0:
        continue
    obj.data.vertices[i].select = True

bpy.ops.object.mode_set(mode = 'EDIT')
