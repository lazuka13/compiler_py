from ir_tree.expressions.IExp import IExp
from syntax_tree import Position
from .IStm import IStm


class Exp(IStm):
    def __init__(self, expression: IExp, position: Position = Position(0, 0)):
        IStm.__init__(self, position)
        self.expression = expression
