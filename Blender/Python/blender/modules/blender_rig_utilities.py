import bpy
from blender.modules.blender_config import *

def does_armature_exist(namespace):
    try:
        return bpy.data.armatures[namespace + '_ARM'] is not None
    except:
        return False

def create_base_armature(namespace, location=(0.0,0.0,0.0), show_name=False):
    if not does_armature_exist(namespace):
        # Create the Object
        bpy.ops.object.add(
            type=BlenderType.ARMATURE.name,
            enter_editmode=True,
            location=location)
        
        # Set Object Name
        ob = bpy.context.object
        ob.name = namespace
        ob.show_name = show_name

        # Set Armature Name
        arm = ob.data
        arm.name = namespace + TYPE_TO_SUFFIX[BlenderType.ARMATURE]

        # Return to Object Mode
        bpy.ops.object.mode_set(mode='OBJECT')

        return bpy.data.armatures[namespace + TYPE_TO_SUFFIX[BlenderType.ARMATURE]]
    else:
        print ('Armature already exists! Choose a different namespace')

    return bpy.data.armatures[namespace + TYPE_TO_SUFFIX[BlenderType.ARMATURE]]

def add_bone_to_armature(armature, boneName='Bone', wsOrigin=(0.0,0.0,0.0), wsDestination=(0.0,0.0,1.0), parent=None):
    out_bone = None

    if armature is not None:
        # Set to Edit for bone add
        bpy.ops.object.mode_set(mode='EDIT')

        # Create single bone
        out_bone = armature.edit_bones.new(boneName)
        out_bone.head = wsOrigin
        out_bone.tail = wsDestination

        # Return to Object Mode
        bpy.ops.object.mode_set(mode='OBJECT')
    else:
        print ('Armature is null')
    
    return out_bone