from enum import Enum
from .i_exp import IExp

from syntax_tree import Position


class BinopEnum(Enum):
    PLUS = 1
    MINUS = 2
    OR = 3
    AND = 4
    MUL = 5
    MOD = 6


class Binop(IExp):
    def __init__(self, operation: BinopEnum, left_expression: IExp, right_expression: IExp,
                 position: Position = Position(0, 0)):
        IExp.__init__(self, position)
        self.operation = operation
        self.left_expression = left_expression
        self.right_expression = right_expression

    def is_commutative(self):
        return False

    def is_absolutely_commutative(self):
        return False
