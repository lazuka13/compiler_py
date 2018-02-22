from ir_tree.expressions.binop import Binop, BinopEnum
from ir_tree.expressions.const import Const
from ir_tree.expressions.i_exp import IExp
from ir_tree.expressions.mem import Mem
from ir_tree.expressions.temp import Temp
from syntax_tree import Position
from .i_access import IAccess, RecordsType
from .temp_address import TempAddress


class InFrameAccess(IAccess):
    def __init__(self, record_type: RecordsType, size: int, offset: int):
        IAccess.__init__(self)
        self.record_type = record_type
        self.size = size
        self.address = TempAddress(offset)

    def offset(self):
        return self.address

    def print(self, frame_pointer: TempAddress):
        return f'Frame Position {self.address.at_address(frame_pointer.get_address()).get_address()}'

    def get_exp(self, fp: Temp, position: Position) -> IExp:
        return Mem(
            Binop(
                BinopEnum.PLUS,
                fp,
                Const(self.address.address, position),
                position
            ),
            position
        )
