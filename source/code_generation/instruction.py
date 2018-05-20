import re

from ir_tree.expressions.temp import Temp, TempList
from ir_tree.expressions.const import Const
from ir_tree.label import Label, LabelList


class IInstruction:
    def __init__(self):
        self.src = TempList()
        self.dst = TempList()
        self.label_list = LabelList()
        self.asm_code = None

    def format(self):
        instruction_string = ''
        prev_pivot = 0
        for match in re.finditer('%', self.asm_code):
            code = self.asm_code[match.start()+1]
            instruction_string += self.asm_code[prev_pivot:match.start()]
            if code == 'l':
                instruction_string += self.label_list[0].name
            elif int(code) < len(self.dst):
                assert len(self.dst) > 0
                instruction_string += "r" + self.dst[0].name + str(self.dst[0].id)
            else:
                src_pos = int(code) - len(self.dst)
                assert src_pos < len(self.src)
                instruction_string += "r" + self.src[src_pos].name + str(self.src[src_pos].id)
            prev_pivot = match.start() + 2
        instruction_string += self.asm_code[prev_pivot:]
        instruction_string += "\tUsed:"
        for tmp in self.src:
            instruction_string += " r" + tmp.name + str(tmp.id) + ";"
        instruction_string += "\tDefined:"
        for tmp in self.dst:
            instruction_string += " r" + tmp.name + str(tmp.id) + ";"
        return instruction_string

    def format_long(self):
        instructionString = self.format()
        instructionString += "\tUsed:"
        for tmp in self.src:
            instructionString += " r" + str(tmp.name) + str(tmp.id) + ";"
            instructionString += "\tDefined:"
        for tmp in self.dst:
            instructionString += " r" + str(tmp.name) + str(tmp.id) + ";"
        return instructionString;


class MoveInstruction(IInstruction):
    def __init__(self, _from=None, _to=None, _fromlist=None, pure_move=False):
        IInstruction.__init__(self)
        self._pure_move = pure_move
        if _from or _to:
            if isinstance(_to, Temp):
                self.dst.append(_to)
            else:
                raise NotImplementedError()

            if isinstance(_from, Temp):
                self.src.append(_from)
            elif isinstance(_from, Const):
                self.from_const = _from
            else:
                raise NotImplementedError()
        elif _fromlist and isinstance(_fromlist, TempList):
            self.src = _fromlist
        else:
            raise NotImplementedError()

    @property
    def pure_move(self):
        return self._pure_move


class LabelInstruction(IInstruction):
    def __init__(self, label: Label):
        IInstruction.__init__(self)
        self._label = label

    @property
    def label(self):
        return self._label

    def format(self):
        return self.label.name + ":"


class InstructionList:
    def __init__(self):
        self.instructions = []
        self.registers = []


