from .IStm import IStm
from ir_tree.Label import Label
from syntax_tree import Position


class Jump(IStm):
    def __init__(self, label: Label, position: Position = Position(0, 0)):
        IStm.__init__(self, position)
        self.label_to_jump = label
