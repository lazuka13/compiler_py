from typing import Dict, List

from ir_tree.label import Label
from ir_tree.statements.i_stm import IStm
from ir_tree.statements.jumpc import JumpTypeEnum


class ISubtreeWrapper:
    def to_exp(self):
        pass

    def to_stm(self):
        pass

    def to_conditional(self, jump_type: JumpTypeEnum, true_label: Label):
        pass

    def accept(self, visitor):
        visitor.visit(self)


LinearTree: List[IStm] = list
IRForest: Dict[str, ISubtreeWrapper] = dict
IRLinearForest: Dict[str, LinearTree] = dict
