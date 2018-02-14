from syntax_tree import Position


class List:
    def __init__(self, head=None, tail=None, position=Position(0, 0)):
        self.head = head
        self.tail = tail
        self.position = position
