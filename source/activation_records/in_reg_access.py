from ir_tree.expressions.i_exp import IExp
from ir_tree.expressions.mem import Mem
from ir_tree.expressions.temp import Temp
from syntax_tree import Position
from .i_access import IAccess
from .temp_address import TempAddress


class InRegAccess(IAccess):
    AR_Prefix = 'AR::'

    def __init__(self, record_type, size, name: str = None, id: int = None):
        IAccess.__init__(self)
        self.record_type = record_type
        self.size = size
        if id is not None:
            self.id = id
            self.name = str(id)
        else:
            self.id = -1
            self.name = name

        self.temp = Temp(self.AR_Prefix + self.name)

    @classmethod
    def from_other(cls, other: 'InRegAccess'):
        obj = cls(other.record_type, other.size, other.name, other.id)
        obj.temp = Temp(None, None, other.temp)

    def print(self, frame_pointer: TempAddress):
        return f'Register {self.name}'

    def get_exp(self, fp: Temp, position: Position) -> IExp:
        del fp
        return Mem(Temp(None, None, self.temp, position), position)
