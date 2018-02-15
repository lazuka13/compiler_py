from ir_tree.i_node import INode
from syntax_tree import Position


class IExp(INode):
    def __init__(self, position: Position = Position(0, 0)):
        INode.__init__(self, position)
