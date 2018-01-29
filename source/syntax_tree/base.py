class Visitor:
    def __init__(self):
        pass


class Visitable:
    def __init__(self, place):
        self.place = place

    def accept(self, visitor):
        visitor.visit(self)
