from ir_tree.label import Label
from syntax_tree import Position
from .i_exp import IExp


class Name(IExp):
    def __init__(self, name: str = None, position: Position = Position(0, 0)):
        IExp.__init__(self, position)
        if str is None:
            self.label_name = Label.get_next_enumerated_label()
        else:
            self.label_name = Label.get_label(name)
