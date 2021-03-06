import bpy
import blender.modules.blender_config as config
from schmod.schmod_rigging_framework.rig_definition import *

class BlenderRig(BaseRig):
    """Placeholder"""
    def __init__(self, name, position=(0.0,0.0,0.0), namespace=''):
        super().__init__(name)

        self.position = position

        # Blender specific armature concept
        self.armature = self._create_armature()
    
    # Abstract Methods
    @property
    def rig_dcc(self):
        return RigDCC.Blender
    
    def load_rig_from_definition(self):
        """TODO: Impliment once actually finished"""
        return None

    def resolve_armature_name(self):
        return self.resolve_rig_name() + config.TYPE_TO_SUFFIX[config.BlenderType.ARMATURE]

    def add_bone(self, boneName, primary_side, position, rotation, scale=None, parent='', parentSnap=False, secondary_side=None, secondary_position=(0.0,0.0,0.0)):
        new_bone = BlenderBone(self, boneName, primary_side, position, rotation, parent=parent, parentSnap=parentSnap, secondary_position=secondary_position)
        self.bones[new_bone] = new_bone.resolve_object_name()

        return new_bone

    def remove_bone(self, boneName):
        pass

    # Class Methods
    def does_armature_exist(self):
        try:
            return bpy.data.armatures[self.resolve_armature_name()] is not None
        except:
            return False

    def _create_armature(self):
        if not self.does_armature_exist():
            # Create the Object
            bpy.ops.object.add(
                type=config.BlenderType.ARMATURE.name,
                enter_editmode=True,
                location=self.position)
            
            # Set Object Name
            ob = bpy.context.object
            ob.name = self.resolve_rig_name()
            #ob.show_name = show_name

            # Set Armature Name
            arm = ob.data
            arm.name = self.resolve_armature_name()

            # Return to Object Mode
            bpy.ops.object.mode_set(mode='OBJECT')
        else:
            print ('Armature already exists! Choose a different namespace')

        return bpy.data.armatures[self.resolve_armature_name()]

class BlenderBone(RigObject):
    def __init__(self, rig, name, primary_side, position, rotation, scale=None, parent=None, parentSnap=False, secondary_side=None, secondary_position=(0.0,0.0,0.0)):
        super().__init__(rig, name, RigObjectType.Bone, primary_side, position, rotation, scale=scale, parent=parent, secondary_side=secondary_side, secondary_position=secondary_position)

        self.parent = None
        if parent:
            self._set_parent(parent, parentSnap=parentSnap)

    # Abstract Methods
    def _create_target(self):
        # Set to Edit for bone add
        bpy.ops.object.mode_set(mode='EDIT')

        # Create single bone
        bone = self.rig.armature.edit_bones.new(self.resolve_object_name())
        bone.head = self.position
        bone.tail = self.secondary_position
        
        # Return to Object Mode
        bpy.ops.object.mode_set(mode='OBJECT')

        return bone
    
    def _set_parent(self, parent, parentSnap=False):
        # set to Edit for bone add
        bpy.ops.object.mode_set(mode='EDIT')

        # set internal parent
        self.parent = parent

        # set parent
        parent_bone = self.rig.armature.edit_bones[parent.resolve_object_name()]
        bone = self.rig.armature.edit_bones[self.resolve_object_name()]
        bone.parent = parent_bone
        bone.use_connect = parentSnap

        # set to Edit for bone add
        bpy.ops.object.mode_set(mode='OBJECT')
