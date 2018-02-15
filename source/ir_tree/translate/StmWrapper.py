from .ISubtreeWrapper import ISubtreeWrapper
from ir_tree.statements.IStm import IStm
from ir_tree.Label import Label


class StmWrapper(ISubtreeWrapper):
    def __init__(self, statement: IStm):
        self.statement = statement

    def to_exp(self):
        assert False

    def to_stm(self):
        return self.statement

    def to_conditional(self, true_label: Label, false_label: Label):
        assert False
