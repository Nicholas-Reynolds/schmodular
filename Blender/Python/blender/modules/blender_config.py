from enum import Enum

class BlenderType(Enum):
    ARMATURE = 0
    BONE = 1

class BlenderMode(Enum):
    OBJECT = 0,
    EDIT = 1

TYPE_TO_SUFFIX = {
    BlenderType.ARMATURE : '_ARM',
    BlenderType.BONE : '_BN'
}