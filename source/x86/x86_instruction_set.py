from enum import Enum

from code_generation.instruction import IInstruction, MoveInstruction
from ir_tree.expressions.temp import Temp, TempList
from ir_tree.expressions.const import Const
from ir_tree.label import Label, LabelList


class Regs(Enum):
    EAX = 1
    EBX = 2
    ECX = 3
    EDX = 4


class CISCOperation(IInstruction):
    def __init__(self, asm_code: str, src_list: TempList, dst_list: TempList,
                 label_list: LabelList=None):
        IInstruction.__init__(self)
        self.src = src_list
        self.dst = dst_list
        self.asm_code = asm_code
        if label_list:
            self.label_list = label_list


class RegMove(MoveInstruction):
    def __init__(self, _code, _from=None, _to=None, _fromlist=None, pure_move=False):
        super().__init__(_from, _to, _fromlist, pure_move)
        self.asm_code = _code
