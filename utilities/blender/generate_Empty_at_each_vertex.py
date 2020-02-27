#!/usr/bin/env python
import bpy
# from mathutils import Matrix
from mathutils import Vector
# from mathutils import Euler

print("How to use: paste into a Blender Text Editor panel, select"
      " object, Run Script")

y_up = True
enable_minetest = True


class MessageBox(bpy.types.Operator):
    bl_idname = "message.messagebox"
    bl_label = ""
    message = bpy.props.StringProperty(
        name="message",
        description="message",
        default=''
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


ob1 = bpy.context.active_object  # works with 2.7 or 2.8
# try:
#     # See <https://blender.stackexchange.com/questions/141330/
#     #   problem-with-bpy-context-selected-objects>
#     # for o in context.scene.objects:
#     #     o.select_get() returns bool!
#     # To select it automatically: o.select_set(bool)
# except:
#     # Blender version <= 2.79
#     ob1 = bpy.context.scene.objects.active

bpy.utils.register_class(MessageBox)

if ob1 is None:
    msg = "Nothing is selected."
    # WRONG: <https://stackoverflow.com/questions/7697532/how-to-show-a-
    #   message-from-a-blender-script>
    # self.report({'ERROR'}, msg)
    bpy.ops.message.messagebox('INVOKE_DEFAULT', message=msg)
else:

    loc1 = ob1.location
    # loc1 = ob1.matrix_world.translation

    # See <https://blender.stackexchange.com/questions/6139/how-to-
    #   iterate-through-all-vertices-of-an-object-that-contains-
    #   multiple-meshes>
    mesh = ob1.data
    # print("mesh:" + str(mesh))
    # print("hasattr(mesh, 'vertices'):" + str(hasattr(mesh,
    #                                                  'vertices')))
    xMin = None  # Define so None check is possible later.
    if (mesh is not None) and (not hasattr(mesh, 'vertices')):
        print("--can't calculate collisionbox for skeleton")
    elif mesh is not None:
        xMin = None
        yMin = None
        zMin = None
        xMax = None
        yMax = None
        zMax = None
        # See <https://blender.stackexchange.com/questions/6155/how-to-
        #   convert-coordinates-from-vertex-to-world-space>
        wm = ob1.matrix_world
        newNamePrefix = "Empty.from." + ob1.name
        i = 0
        for vert in mesh.vertices:
            name = newNamePrefix + "." + str(i)
            # This matrix multiplication is NOT transitive.
            try:
                loc = wm @ vert.co
            except TypeError:
                loc = wm * vert.co  # Blender <2.8
            # See also vert.co.x (and y and z)
            bpy.ops.object.add(type='EMPTY', radius=.25, location=loc)
            bpy.context.active_object.name = name

            # Also consider sambler's answer at
            # <https://blender.stackexchange.com/a/45102/12998>:
            # new_obj = bpy.data.objects.new(name, None)  # , 'EMPTY')??
            # new_obj.location = (x,y,z)
            # bpy.context.scene.objects.link(new_obj)  # add to scene

            # The add_named code below doesn't work:
            # bpy.ops.object.add_named(name="Empty" + ob1.name,
            #                          type='EMPTY', radius=.25,
            #                          location=loc)
            i += 1

# bpy.ops.message.messagebox('INVOKE_DEFAULT', message = msg)

# Unregistering before user clicks the MessageBox will crash Blender!
# bpy.utils.unregister_class(MessageBox)
