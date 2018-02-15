from syntax_tree import Position

from .IExp import IExp


class Const(IExp):
    def __init__(self, value: int, position: Position = Position(0, 0)):
        IExp.__init__(self, position)
        self.value = value
