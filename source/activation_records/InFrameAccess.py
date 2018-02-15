from ir_tree.expressions.Binop import Binop, BinopEnum
from ir_tree.expressions.Const import Const
from ir_tree.expressions.IExp import IExp
from ir_tree.expressions.Mem import Mem
from ir_tree.expressions.Temp import Temp
from syntax_tree import Position
from .IAccess import Access, RecordsType
from .TempAddress import TempAddress


class InFrameAccess(Access):
    def __init__(self, record_type: RecordsType, size: int, offset: int):
        Access.__init__(self)
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
