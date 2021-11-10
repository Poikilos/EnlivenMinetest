
'''
Create actual bones from temporary bones that the
B3D importer creates.

Requires: Blender (>=2.8)

Assumes:
- x y and z scale, if not 1.0, must be all the same on the empties for this to work.

Usage:
- Paste this script into a new text file in a text editor panel
  (If you don't know how to get there, see the HowTo file in
  the utilities/blender directory at
  github.com/poikilos/EnlivenMinetest).
- Select an empty that has a mesh for a parent like a model imported from a B3D, or an empty that has no parent.
- "Text", "Run Script".
'''
import bpy
from mathutils import Vector, Quaternion
import mathutils
import math
context = bpy.context
print("")
print("[ EnlivenMinetest/utilities/blender/hierarchy_of_empties_to_bones.py ] started")

# armature_display_type = 'STICK'
armature_display_type = 'OCTAHEDRAL'
# ^ Can be: ('OCTAHEDRAL', 'STICK', 'BBONE', 'ENVELOPE', 'WIRE')
#   default: 'OCTAHEDRAL'


def mat3_to_vec_roll(mat):
    '''
    Convert a mat3 to a tuple containing a vec and roll.
    
    Hendrix says that he re-ported the C code of blender to do this
    after Emd4600 ported it 
    but for this function, he says, "this hasn't changed."
    -[HENDRIX](https://blender.stackexchange.com/users/45904/hendrix).
     <https://blender.stackexchange.com/a/90240>. Sep 14, 2017.

    Blender is [GPLv2](https://developer.blender.org/diffusion/B/browse/master/doc/license/GPL-license.txt)
    --does that matter here?    
    '''
    vec = mat.col[1]
    vecmat = vec_roll_to_mat3(mat.col[1], 0)
    vecmatinv = vecmat.inverted()
    rollmat = vecmatinv * mat
    roll = math.atan2(rollmat[0][2], rollmat[2][2])
    return vec, roll


def vec_roll_to_mat3(vec, roll):
    '''
    #port of the updated C function from armature.c
    #https://developer.blender.org/T39470
    #note that C accesses columns first, so all matrix indices are swapped compared to the C version
    -HENDRIX1
    
    HENDRIX1 says that he re-ported the C code of blender to do this
    after Emd4600 ported it 
    -[HENDRIX](https://blender.stackexchange.com/users/45904/hendrix).
     <https://blender.stackexchange.com/a/90240>. Sep 14, 2017.

    Blender is [GPLv2](https://developer.blender.org/diffusion/B/browse/master/doc/license/GPL-license.txt)
    --does that matter here?    
    '''

    nor = vec.normalized()
    THETA_THRESHOLD_NEGY = 1.0e-9
    THETA_THRESHOLD_NEGY_CLOSE = 1.0e-5

    #create a 3x3 matrix
    bMatrix = mathutils.Matrix().to_3x3()

    theta = 1.0 + nor[1];

    if (theta > THETA_THRESHOLD_NEGY_CLOSE) or ((nor[0] or nor[2]) and theta > THETA_THRESHOLD_NEGY):

        bMatrix[1][0] = -nor[0];
        bMatrix[0][1] = nor[0];
        bMatrix[1][1] = nor[1];
        bMatrix[2][1] = nor[2];
        bMatrix[1][2] = -nor[2];
        if theta > THETA_THRESHOLD_NEGY_CLOSE:
            #If nor is far enough from -Y, apply the general case.
            bMatrix[0][0] = 1 - nor[0] * nor[0] / theta;
            bMatrix[2][2] = 1 - nor[2] * nor[2] / theta;
            bMatrix[0][2] = bMatrix[2][0] = -nor[0] * nor[2] / theta;

        else:
            #If nor is too close to -Y, apply the special case.
            theta = nor[0] * nor[0] + nor[2] * nor[2];
            bMatrix[0][0] = (nor[0] + nor[2]) * (nor[0] - nor[2]) / -theta;
            bMatrix[2][2] = -bMatrix[0][0];
            bMatrix[0][2] = bMatrix[2][0] = 2.0 * nor[0] * nor[2] / theta;

    else:
        #If nor is -Y, simple symmetry by Z axis.
        bMatrix = mathutils.Matrix().to_3x3()
        bMatrix[0][0] = bMatrix[1][1] = -1.0;

    #Make Roll matrix
    rMatrix = mathutils.Matrix.Rotation(roll, 3, nor)

    #Combine and output result
    mat = rMatrix * bMatrix
    return mat


def getFirstChild(parentName):
    for obj in bpy.data.objects:
        if obj.parent is None:
            continue
        if obj.parent.name == parentName:
            return obj
    return None


def getRealRotation_broken(cumulative_rotation, empty):
    if cumulative_rotation is None:
        cumulative_rotation = Quaternion((1, 0, 0, 0))
        # ^ default (no rotation) in Blender is (w, x, y, z) = (0, 0, 0, 1).
    if (empty.parent is None) or (empty.parent.type != 'EMPTY'):
        return cumulative_rotation
    return getRealRotation(cumulative_rotation, empty.rotation_quaternion) @ empty.parent.rotation_quaternion


def getRealRotation(empty):
    '''
    This function exists to test ensuring correct order of operation because
    HENDRIX1 replied to Cirno's cited post on blenderartists saying:
    mat_armature = mat_local * parent_mat_local_0 * parent_mat_local_1 * … * parent_mat_local_n
    The parent mats are the direct parent first, more removed parents in the end.
    current_bone.transform(transform_quat.to_matrix())
    - HENDRIX1 <https://blenderartists.org/t/needed-help-with-creating-bones-in-python-using-position-and-rotation-data/1209120/2>.
    '''
    ancestor = empty.parent
    if (ancestor is None):
        return empty.rotation_quaternion
    ancestor = empty.parent.parent
    if (ancestor is None):
        return empty.rotation_quaternion @ empty.parent.rotation_quaternion
    ancestor = empty.parent.parent.parent
    if (ancestor is None):
        return empty.rotation_quaternion @ empty.parent.rotation_quaternion @ empty.parent.parent.rotation_quaternion
    ancestor = empty.parent.parent.parent.parent
    if (ancestor is None):
        return empty.rotation_quaternion @ empty.parent.rotation_quaternion @ empty.parent.parent.rotation_quaternion @ empty.parent.parent.parent.rotation_quaternion
    ancestor = empty.parent.parent.parent.parent.parent
    if (ancestor is None):
        return empty.rotation_quaternion @ empty.parent.rotation_quaternion @ empty.parent.parent.rotation_quaternion @ empty.parent.parent.parent.rotation_quaternion @ empty.parent.parent.parent.parent.rotation_quaternion
    ancestor = empty.parent.parent.parent.parent.parent.parent
    if (ancestor is None):
        return empty.rotation_quaternion @ empty.parent.rotation_quaternion @ empty.parent.parent.rotation_quaternion @ empty.parent.parent.parent.rotation_quaternion @ empty.parent.parent.parent.parent.rotation_quaternion @ empty.parent.parent.parent.parent.parent.rotation_quaternion
    ancestor = empty.parent.parent.parent.parent.parent.parent.parent
    if (ancestor is None):
        return empty.rotation_quaternion @ empty.parent.rotation_quaternion @ empty.parent.parent.rotation_quaternion @ empty.parent.parent.parent.rotation_quaternion @ empty.parent.parent.parent.parent.rotation_quaternion @ empty.parent.parent.parent.parent.parent.rotation_quaternion @ empty.parent.parent.parent.parent.parent.parent.rotation_quaternion
    ancestor = empty.parent.parent.parent.parent.parent.parent.parent.parent
    if (ancestor is None):
        return empty.rotation_quaternion @ empty.parent.rotation_quaternion @ empty.parent.parent.rotation_quaternion @ empty.parent.parent.parent.rotation_quaternion @ empty.parent.parent.parent.parent.rotation_quaternion @ empty.parent.parent.parent.parent.parent.rotation_quaternion @ empty.parent.parent.parent.parent.parent.parent.rotation_quaternion @ empty.parent.parent.parent.parent.parent.parent.parent.rotation_quaternion
    ancestor = empty.parent.parent.parent.parent.parent.parent.parent.parent.parent
    if (ancestor is None):
        return empty.rotation_quaternion @ empty.parent.rotation_quaternion @ empty.parent.parent.rotation_quaternion @ empty.parent.parent.parent.rotation_quaternion @ empty.parent.parent.parent.parent.rotation_quaternion @ empty.parent.parent.parent.parent.parent.rotation_quaternion @ empty.parent.parent.parent.parent.parent.parent.rotation_quaternion @ empty.parent.parent.parent.parent.parent.parent.parent.rotation_quaternion @ empty.parent.parent.parent.parent.parent.parent.parent.parent.rotation_quaternion
    ancestor = empty.parent.parent.parent.parent.parent.parent.parent.parent.parent.parent
    if (ancestor is None):
        return empty.rotation_quaternion @ empty.parent.rotation_quaternion @ empty.parent.parent.rotation_quaternion @ empty.parent.parent.parent.rotation_quaternion @ empty.parent.parent.parent.parent.rotation_quaternion @ empty.parent.parent.parent.parent.parent.rotation_quaternion @ empty.parent.parent.parent.parent.parent.parent.rotation_quaternion @ empty.parent.parent.parent.parent.parent.parent.parent.rotation_quaternion @ empty.parent.parent.parent.parent.parent.parent.parent.parent.rotation_quaternion @ empty.parent.parent.parent.parent.parent.parent.parent.parent.parent.rotation_quaternion

    raise NotImplementedError("Fake recursion isn't implemented for hierarchies this deep.")


def vectorDiff(v1, v2):
    if len(v1) != len(v2):
        raise ValueError("v1 length is {} but v2 length is {}".format(len(v1), len(v2)))
    if len(v1) == 4:
        return Vector((v1[0]-v2[0], v1[1]-v2[1], v1[2]-v2[2], v1[3]-v2[3]))
    elif len(v1) == 3:
        return Vector((v1[0]-v2[0], v1[1]-v2[1], v1[2]-v2[2]))
    else:
        raise ValueError("v1 and v1 are of length {} but that is not a known valid location vector length.".format(len(v1)))
    return None


def makeSameChildren(empty, armature, parent_bone, parent_empty, cumulative_rotation, cumulative_scale, depth=0):
    '''
    Make a new bone for the given empty, then do the same
    recursively for each of the empty's children.
    
    This is based on Cirno's hard-coded armature creation code at <https://blenderartists.org/t/needed-help-with-creating-bones-in-python-using-position-and-rotation-data/1209120>
    '''
    name = empty.name
    extI = empty.name.rfind(".")
    ext = None
    if extI > -1:
        name = empty.name[:extI]
        ext = empty.name[extI+1:]
    print(depth*" "+"- "+name)
    # ext != "Empty":
        # print("Error: the must end with .Empty so the bone naming scheme won't interfere with the object naming scheme.")
    #     return
    wm = empty.matrix_world
    current_bone = armature.edit_bones.new(name)

    length = empty.empty_display_size
    
    # Get rotation difference of 2 points (2 "vectors"):
    # 
    # - <https://docs.blender.org/api/current/mathutils.html?highlight=rotation_difference#mathutils.Vector.rotation_difference>
    # - <https://docs.blender.org/api/blender_python_api_2_63_5/mathutils.html>
    #   - several operations are used in succession in the first code block but some may be only for generating test data
    scale = None
    transform_quat = None
    if parent_bone is not None:
        '''
        It has a parent, so the **cumulative** transform of the empty is
        necessary here to set the length correctly according to scale,
        and to set rotation correctly.
        TODO: There is no answer at <https://devtalk.blender.org/t/how-to-retrieve-accumulated-transformation-matrix-from-bone-deformation/7729>
        - "EDIT: Posebone.matrix is in bonespace. Posebone.matrix rotation rotates armature up vector into bone vector." -Terry on https://blenderartists.org/t/how-to-global-pose-transforms-to-hierarchial-armature/548022/4
        '''
        # parent_bone.tail = empty.location  # Not always: there is often an offset
        
        # print("dir parent_bone: {}".format(dir(parent_bone)))
        # print("dir parent_bone: {}".format(dir(parent_bone)))
        parent_bone_tail = parent_bone.tail
        parent_bone_quat_armature_space = Quaternion(parent_empty.rotation_quaternion)
        print(depth*" "+"  - parent_empty.name:{}".format(parent_empty.name))
        print(depth*" "+"  - parent_bone.name:{}".format(parent_bone.name))
        
        # create bone at armature origin and set its length
        scale = cumulative_scale * empty.scale.z
        boneLength = length * scale
        current_bone.head = [0, 0, 0]
        current_bone.tail = [0, 0, boneLength]

        # rotate bone
        # print(depth*" "+"  - empty.rotation_quaternion:{}".format(Quaternion(empty.rotation_quaternion)))
        # print(depth*" "+"  - parent_empty.rotation_quaternion:{}".format(Quaternion(parent_empty.rotation_quaternion)))
        # ^ empty.rotation_quaternion is verified to be relative to parent
        # ^ parent and child rotation being the same is ok even if they look different because rotation_quaternion is relative.
        # parent_bone_quat_armature_space = Quaternion(parent_bone.rotation)
        # ^ bone only has: matrix, roll, transform and properties that are not transform-related.
        #   The head and tail locations determine the visual appearance of having direction.
        
        current_bone_quat_parent_space = Quaternion(empty.rotation_quaternion)
        # ^ rotation_quaternion is confirmed to be relative.
        # Like matrices, quaternions can be multiplied to accumulate rotational values.
        # Multiply parent rotation by the parent space rotation of the child:
        # transform_quat = parent_bone_quat_armature_space @ current_bone_quat_parent_space
        # transform_quat = current_bone_quat_parent_space @ cumulative_rotation
        # transform_quat = Quaternion(empty.rotation_quaternion) @ Quaternion(empty.parent.rotation_quaternion)
        # transform_quat = getRealRotation(empty)
        # ^ getRealRotation(emtpy) gives same result as current_bone_quat_parent_space @ cumulative_rotation
        # transform_quat = current_bone_quat_parent_space
        # transform_quat = getRealRotation(empty)
        transform_quat = empty.rotation_quaternion
        current_bone.transform(transform_quat.to_matrix())
        # current_bone.tail = transform_quat.to_matrix() @ current_bone.tail
        
        # matrix = transform_quat.to_matrix()
        # tail, roll = mat3_to_vec_roll(matrix)
        # current_bone.head = matrix.to_translation()
        # ^ ValueError: Matrix.to_translation(): inappropriate matrix size
        # tail, roll = mat3_to_vec_roll(matrix.to_3x3())
        # current_bone.head = matrix.to_translation()
        # ^ ValueError: Matrix.to_translation(): inappropriate matrix size
        #current_bone.tail = tail*boneLength + bone.head
        #current_bone.roll = roll
        
        # set position
        # new_relative_loc = Quaternion(empty.location)
        # ^ The empty.location is relative to the parent_empty's head
        # but must be made relative the parent_bone's tail.
        # old_to_new = Vector(parent_empty.location) - Vector(parent_bone.tail)
        old_to_new = vectorDiff(parent_empty.location, parent_bone.tail)
        # new_relative_loc = old_to_new - Vector(empty.location)
        new_relative_loc = vectorDiff(old_to_new, empty.location)
        # uhoh_if_nonzero = Vector(parent_bone.head) - Vector(parent_empty.location)
        # print(depth*" "+"  - uhoh_if_nonzero:{}".format(uhoh_if_nonzero))
        # ^ It is nonzero :(
        print(depth*" "+"  - empty.location:{}".format(empty.location))
        print(depth*" "+"  - parent_bone.tail:{}".format(parent_bone.tail))
        print(depth*" "+"  - old_to_new:{}".format(old_to_new))
        print(depth*" "+"  - new_relative_loc:{}".format(new_relative_loc))
        # print(depth*" "+"  - current_bone_offset:{}".format(current_bone_offset))
        current_bone.translate(new_relative_loc)

        # connect
        current_bone.parent = parent_bone
        # current_bone.use_connect = True
        '''
        ^ Bones are often not fully connected even though parented
          in block-style models.
          - current_bone.use_connect = True forces the base of the
            bone to the location of the tail of the parent,
            which will make often make the placement inaccurate.
        '''
    else:  # first bone in chain
        scale = cumulative_scale * empty.scale.z
        transform_quat = empty.rotation_quaternion
        current_bone.head = [0, 0, 0]
        current_bone.tail = [0, 0, length * scale]
        
        # rotate bone
        quat_armature_space = empty.rotation_quaternion
        # current_bone.rotation_quaternion = empty.rotation_quaternion
        # ^ AttributeError: 'EditBone' object has no attribute 'rotation_quaternion'
        current_bone.transform(quat_armature_space.to_matrix())
        
        # set position
        current_bone.translate(Vector(empty.location))
    '''
    try:
        current_bone.translate(Vector(wm @ empty.location))
    except TypeError:
        current_bone.translate(Vector(wm * empty.location))
        # ^ Blender < 2.8 matrix multiplication is *
    '''
    # parent_bone = current_bone
    # parent_bone_tail = current_bone.tail
    # parent_bone_quat_armature_space = quat_armature_space
    if empty.children is not None:
        for child in empty.children:
            if child.type != 'EMPTY':
                continue
            makeSameChildren(child, armature, current_bone, empty, transform_quat, scale, depth=depth+1)


def makeSameChildrenFromRootEmpty(obj):
    if obj is None:
        print("Nothing is selected.")
        return
    if obj.type != 'EMPTY':
        print("non-Empty {} type: {} isn't compatible with this script".format(obj.name, obj.type))
        return
    if (obj.parent is not None) and (obj.parent.type != 'MESH'):
        print("WARNING: An object with a parent that isn't a mesh: {} type {} may not be compatible with this script".format(obj.name, obj.type))
        # return

    # Create a new armature if the empty has no parent.
    print("{} parent: {}".format(obj.name, obj.parent))
    # print("dir: {}".format(dir(obj)))
    print("location: {}".format(obj.location))
    
    print("rotation_quaternion: {}".format(obj.rotation_quaternion))
    print("scale: {}".format(obj.scale))
    # See <https://blenderartists.org/t/
    # needed-help-with-creating-bones-in-python-using-
    # position-and-rotation-data/1209120>:
    armature = bpy.data.armatures.new("Armature")
    armature.display_type = armature_display_type
    rig = bpy.data.objects.new("Armature", armature)
    context.scene.collection.objects.link(rig)
    context.view_layer.objects.active = rig
    bpy.ops.object.editmode_toggle()
    print("hierarchy:")
    makeSameChildren(obj, armature, None, None, None, 1.0)
    bpy.ops.object.editmode_toggle()
    # bpy.context.active_object = rig
    
    obj.select_set(state=False)
    rig.select_set(state=True)
    context.view_layer.objects.active = rig
    # else:
    #     print("{} parent: {}".format(obj.name, obj.parent))


makeSameChildrenFromRootEmpty(context.view_layer.objects.active)

