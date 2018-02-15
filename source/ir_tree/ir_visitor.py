from syntax_tree import Visitor


class IRVisitor(Visitor):
    def __init__(self):
        Visitor.__init__(self)

    def visit(self, visitable):
        pass
