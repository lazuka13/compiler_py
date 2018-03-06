from ir_tree.statements.i_stm import IStm
from syntax_tree import Position
from .i_exp import IExp


class Eseq(IExp):
    def __init__(self, statement: IStm, expression: IExp, position: Position = Position(0, 0)):
        IExp.__init__(self, position)
        self.statement = statement
        self.expression = expression

    def is_commutative(self):
        return False

    def is_absolutely_commutative(self):
        return False
