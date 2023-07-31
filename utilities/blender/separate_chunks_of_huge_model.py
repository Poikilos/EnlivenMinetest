import bpy

# in Namaman, the chunk for Darkhorn is near 599000, 410000 to around 685000, 496000
# (chunk_col = 6, chunk_row = 4, chunk_size = 100000
chunk_size = 100000
epsilon = .1
for chunk_col in range(10):
    for chunk_row in range(10):
        chunk_left = chunk_col * chunk_size - epsilon
        chunk_right = (chunk_col+1) * chunk_size + epsilon
        # Lower number is bottom since cartesian:
        chunk_bottom = chunk_row * chunk_size - epsilon
        chunk_top = (chunk_row+1) * chunk_size + epsilon
        bpy.ops.wm.tool_set_by_id(name="builtin.scale")
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
        for i in range(len(obj.data.vertices)):
            # dir(obj.data.vertices[i])
            obj.data.vertices[i].select = False
            #obj.data.edges[7].select = True
            #obj.data.polygons[2].select = True
            v = obj.data.vertices[i]
            if v.co.x < chunk_left:
                continue
            if v.co.x > chunk_right:
                continue
            if v.co.y < chunk_bottom:
                continue
            if v.co.y > chunk_top:
                continue
            # v.select_set(False)
            obj.data.vertices[i].select = True

        bpy.ops.object.mode_set(mode = 'EDIT')
        bpy.ops.mesh.separate(type='SELECTED')

'''makes a dumb square every time for some reason
import bmesh  # for selecting in edit mode
# https://blender.stackexchange.com/a/188323
context = bpy.context

bpy.ops.mesh.primitive_plane_add(
        enter_editmode=True)
ob = context.object
me = ob.data
bm = bmesh.from_edit_mesh(me)

for i, v in enumerate(bm.verts):
    v.select_set(False)
    if v.co.x < chunk_left:
        continue
    if v.co.x > chunk_right:
        continue
    if v.co.y < chunk_bottom:
        continue
    if v.co.y > chunk_top:
        continue
    v.select_set(True)

bm.select_mode |= {'VERT'}
bm.select_flush_mode()

bmesh.update_edit_mesh(me)
'''
