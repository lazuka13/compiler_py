from syntax_tree import Position

from .i_exp import IExp


class Mem(IExp):
    def __init__(self, expression: IExp, position: Position = Position(0, 0)):
        IExp.__init__(self, position)
        self.expression = expression