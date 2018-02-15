from syntax_tree import Position, Visitor


class INode:
    def __init__(self, position: Position):
        self.position = position

    def accept(self, visitor: Visitor):
        visitor.visit(self)
