bl_info = {
    "name": "Schmod Armature Tools",
    "description": "Tools for Rigging",
    "author": "Nicholas Reynolds",
    "version": (1, 0),
    "blender": (2, 80, 0),
    "category": "Schmod",
}

import pathlib
import json
import bpy
from blender.addons.schmod_blender_armature_tools.BlenderRig import BlenderRig
from schmod.schmod_rigging_framework.rig_definition import *

def save_bone_details_to_json(out_path, bone_list):
    desktop_dir = pathlib.Path.home() / 'Desktop'
    json_path = desktop_dir / 'bone_details.json'

    bone_dict = {}
    
    for bone in bone_list:
        bone_dict[bone.name] = []
        bone_dict[bone.name].append({
            'name':bone.name,
            'head':(bone.head[0], bone.head[1], bone.head[2]),
            'tail':(bone.tail[0], bone.tail[1], bone.tail[2]),
            #'rotation':bone.rotation_euler,
            'parent':bone.parent.name if bone.parent is not None else 'None'
        })
    
    to_json = json.dumps(bone_dict, indent=4)

    with open(str(json_path), 'w') as outfile:
        outfile.write(to_json)

class SCHMOD_OT_Test(bpy.types.Operator):
    bl_idname = 'wm.test_print_bones'
    bl_label = 'Test Print Bones'

    def execute(self, context):
        #armature = bpy.data.armatures['Armature']
        #bones = armature.bones
        #save_bone_details_to_json('', bones)
        #armature = bru.create_base_armature('Hello World',location=(0.0, 0.0, 0.0))
        #print(armature.name)
        
        #bone1 = add_bone_to_armature(armature, boneName='Test_Bone_A', wsOrigin=(0.0, 0.0, 12.0), wsDestination=(1.0,7.0,10.0))
        #bone2 = add_bone_to_armature(armature, boneName='Test_Bone_B', wsOrigin=(10.0, 0.0, 0.0), wsDestination=(5.0,1.0,10.0))
        
        #bpy.ops.object.mode_set(mode='EDIT')
        #bpy.context.active_bone.use_connect = False
        #armature.edit_bones['Test_Bone_B'].parent = armature.edit_bones['Test_Bone_A']
        #bpy.ops.object.mode_set(mode='OBJECT')

        # create rig
        rig = BlenderRig('Hello World')
        print ('Rig Name: {0}'.format(rig.resolve_rig_name()))
        print ('Armature Name: {0}'.format(rig.resolve_armature_name()))

        # add bone test
        bone_a = rig.add_bone('Test_Bone_A', RigSide.Left, (-10.0,0.0,0.0), None, secondary_position=(-10,0.0,5.0))
        bone_b = rig.add_bone('Test_Bone_B', RigSide.Right, (10.0,0.0,0.0), None, secondary_position=(10.0,0.0,5.0))

        # parent bone test
        bone_b._set_parent(bone_a, parentSnap=True)

        # print test
        print ('Bone Test A: {0}'.format(rig.bones[bone_a]))
        print ('Bone Test B: {0}'.format(rig.bones[bone_b]))
        
        return {'FINISHED'}

class SCHMOD_PT_ArmatureToolsPanel(bpy.types.Panel):
    """Armature Tools Panel"""
    bl_label = "Armature Tools"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'Armature Tools'

    def draw(self, context):
        self.layout.operator('wm.test_print_bones')

# Registration
classes = [
    SCHMOD_PT_ArmatureToolsPanel,
    SCHMOD_OT_Test
]

def register():
    for cls in classes:
        bpy.utils.register_class(cls)

def unregister():
    for cls in classes:
        bpy.utils.unregister_class(cls)