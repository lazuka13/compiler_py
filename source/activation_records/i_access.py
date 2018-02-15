from enum import Enum

from ir_tree.expressions.temp import Temp
from syntax_tree import Position
from .temp_address import TempAddress


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

    def get_exp(self, fp: Temp, position: Position):
        pass

    def print(self, frame_pointer: TempAddress):
        pass
