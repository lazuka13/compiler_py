from syntax_tree import Position

from ir_tree.List import List, ExpList
from .IExp import IExp


class Call(IExp):
    def __init__(self, func_expr: IExp, args: ExpList, position: Position = Position(0, 0)):
        IExp.__init__(self, position)
        self.func_expr = func_expr
        self.args = args
