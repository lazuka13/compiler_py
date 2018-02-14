from enum import Enum

from .TempAddress import TempAddress


class RecordsType(Enum):
    RT_Formal = 1
    RT_Local = 2
    RT_FramePointer = 3
    RT_StackPointer = 4
    RT_AddressExit = 5
    RT_AddressReturnValue = 6


class Access:
    def __init__(self):
        pass

    def print(self, frame_pointer: TempAddress):
        pass
