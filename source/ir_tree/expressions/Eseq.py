from syntax_tree import Position

from .IExp import IExp
from ir_tree.statements.IStm import IStm


class Const(IExp):
    def __init__(self, statement: IStm, expression: IExp, position: Position = Position(0, 0)):
        IExp.__init__(self, position)
        self.statement = statement
        self.expression = expression
