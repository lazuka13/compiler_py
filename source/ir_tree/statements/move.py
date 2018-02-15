from ir_tree.expressions.i_exp import IExp
from ir_tree.statements.i_stm import IStm
from syntax_tree import Position


class Move(IStm):
    def __init__(self, destination: IExp, source: IExp, position: Position = Position(0, 0)):
        IStm.__init__(self, position)
        self.source = source
        self.destination = destination
