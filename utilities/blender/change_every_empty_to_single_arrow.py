import bpy
for obj in bpy.data.objects:
    if obj.type != 'EMPTY':
        continue
    obj.empty_display_type = 'SINGLE_ARROW'
    obj.empty_display_size = .33
