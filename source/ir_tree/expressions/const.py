from syntax_tree import Position

from .i_exp import IExp


class Const(IExp):
    def __init__(self, value: int, position: Position = Position(0, 0)):
        IExp.__init__(self, position)
        self.value = value

    def is_commutative(self):
        return True

    def is_absolutely_commutative(self):
        return True
