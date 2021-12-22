from enum import Enum
from abc import ABC, abstractmethod
import blender.modules.blender_config as config

class RigDCC(Enum):
    Blender = 0
    Houdini = 1
    Maya = 2,
    Unreal = 3,
    Custom = 99

class RigObjectType(Enum):
    Bone = 0,
    Control = 1,
    Constraint = 2

class RigSection(Enum):
    Generic = 0,
    Head = 1,
    Torso, = 2,
    Arm = 3,
    Hand = 4,
    Hips = 5,
    Leg = 7,
    Foot = 8,
    Tail = 9

class RigSide(Enum):
    Center = 0,
    Left = 1,
    Right = 2,
    Front = 3,
    Back = 4

OBJECT_TYPE_TO_SUFFIX = {
    RigObjectType.Bone : 'BN',
    RigObjectType.Control : 'CTRL',
    RigObjectType.Constraint : 'CSTRT'
}

SIDE_TO_SUFFIX = {
    RigSide.Center : '',
    RigSide.Left : 'L',
    RigSide.Right : 'R',
    RigSide.Front : 'F',
    RigSide.Back : 'B'
}

class RigObject(ABC):
    """Placeholder"""
    def __init__(self, rig, name, object_type, primary_side, position, rotation, scale=None, parent='', secondary_side=None):
        self.rig = rig
        self.name = name
        self.object_type = object_type
        self.primary_side = primary_side
        self.position = position
        self.rotation = rotation
        self.scale = scale
        self.parent = parent
        self.secondary_side = secondary_side

        # Generate target rig object for reference
        self.target = self._create_target()
    
    @abstractmethod
    def _create_target(self):
        raise NotImplementedError('Impliment dummy')

    @abstractmethod
    def _set_parent(self, parent):
        raise NotImplementedError('Impliment dummy')

    def resolve_object_name(self):
        object_name = ''
        if self.rig.namespace != '':
            object_name += self.rig.namespace + '_'
        
        object_name += self.name + '_'
        object_name += OBJECT_TYPE_TO_SUFFIX[self.object_type] + '_'
        if self.primary_side != RigSide.Center:
            object_name += SIDE_TO_SUFFIX[self.primary_side]
            if self.secondary_side:
                object_name += SIDE_TO_SUFFIX[self.secondary_side]
        
        return object_name

class BaseRig(ABC):
    def __init__(self, name, rig_version=0.0, namespace=''):
        self.name = name
        self.rig_version = rig_version
        self.namespace = namespace
        self.bones = {}
    
    @property
    @abstractmethod
    def rig_dcc(self):
        raise NotImplementedError()

    @abstractmethod
    def load_rig_from_definition(self):
        raise NotImplementedError()

    @abstractmethod
    def add_bone(self, bone):
        raise NotImplementedError()
    
    @abstractmethod
    def remove_bone(self):
        raise NotImplementedError()

    def resolve_rig_name(self, suffix=''):
        rig_name = ''

        # Add namespace if populated
        if self.namespace != '':
            rig_name += self.namespace + '_'
        
        # Set base name
        rig_name += self.name

        # Add any additive suffixes if provided
        if suffix != '':
            rig_name += suffix

        return rig_name

class BoneChainTemplate():
    def __init__(self):
        self.bones = None

    def get_chain_head(self):
        pass

    def get_chain_tail(self):
        pass

class HumanoidArmChainTemplate():
    pass

class HumanoidLegChainTemplate():
    pass

class HumanoidFootChainTemplate():
    pass

class HumanoidHeadChainTemplate():
    pass