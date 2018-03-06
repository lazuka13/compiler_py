from enum import Enum

from syntax_tree import Position
from .i_exp import IExp


class UnaryOpEnum(Enum):
    NOT = 1


class UnaryOp(IExp):
    def __init__(self, operation, expression: IExp, position: Position = Position(0, 0)):
        IExp.__init__(self, position)
        self.operation = operation
        self.expression = expression

    def is_commutative(self):
        return False

    def is_absolutely_commutative(self):
        return False
