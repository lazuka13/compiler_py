from ir_tree.expressions.i_exp import IExp
from ir_tree.expressions.temp import Temp
from syntax_tree import Position
from .i_access import Access
from .temp_address import TempAddress


class InRegAccess(Access):
    def __init__(self, record_type, size, name=None, id=None):
        Access.__init__(self)
        self.record_type = record_type
        self.size = size
        if id is not None:
            self.id = id
            self.name = str(id)
        else:
            self.id = -1
            self.name = name

    def print(self, frame_pointer: TempAddress):
        return f'Register {self.name}'

    def get_exp(self, fp: Temp, position: Position) -> IExp:
        return Temp(self.name, None, None, position)