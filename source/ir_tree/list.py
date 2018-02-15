from ir_tree.expressions.i_exp import IExp
from ir_tree.statements.i_stm import IStm
from syntax_tree import Position


class ExpList(IExp):
    def __init__(self, head: IExp = None, tail: IExp = None, position=Position(0, 0)):
        IExp.__init__(self, position)
        self.head = head
        self.tail = tail


class StmList(IStm):
    def __init__(self, head: IStm = None, tail: IStm = None, position=Position(0, 0)):
        IStm.__init__(self, position)
        self.head = head
        self.tail = tail
