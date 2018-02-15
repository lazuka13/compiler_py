from ir_tree.i_node import INode
from syntax_tree import Position


class IStm(INode):
    def __init__(self, position: Position):
        INode.__init__(self, position)
