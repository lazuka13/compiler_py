from syntax_tree import Position


class List:
    def __init__(self, head=None, tail=None, position=Position(0, 0)):
        self.head = head
        self.tail = tail
        self.position = position


class ExpList(List):
    def __init__(self, head: IExp = None, tail: IExp = None, position=Position(0, 0)):
        List.__init__(self)


class StmList(List):
    def __init__(self, head: IStm = None, tail: IStm = None, position=Position(0, 0)):
        List.__init__(self)
