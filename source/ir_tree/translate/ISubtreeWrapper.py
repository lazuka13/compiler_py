from ir_tree.expressions.IExp import IExp
from ir_tree.statements.IStm import IStm
from ir_tree.Label import Label
from typing import Dict


class ISubtreeWrapper:
    def to_exp(self):
        pass

    def to_stm(self):
        pass

    def to_conditional(self, true_label, false_label):
        pass

    def accept(self, visitor):
        visitor.visit(self)


IRForest: Dict[str, ISubtreeWrapper] = dict
