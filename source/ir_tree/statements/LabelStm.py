from ir_tree.Label import Label
from ir_tree.statements.IStm import IStm
from syntax_tree import Position


class LabelStm(IStm):
    def __init__(self, label: Label, position: Position = Position(0, 0)):
        IStm.__init__(self, position)
        self.label_name = label
