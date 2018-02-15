from .ISubtreeWrapper import ISubtreeWrapper
from ir_tree.expressions.IExp import IExp
from ir_tree.statements.Exp import Exp
from ir_tree.Label import Label
from ir_tree.statements.JumpC import JumpC, JumpTypeEnum
from ir_tree.expressions.Temp import Temp


class ExpWrapper(ISubtreeWrapper):
    def __init__(self, expression: IExp):
        self.expression = expression

    def to_exp(self):
        return self.expression

    def to_stm(self):
        return Exp(self.expression)

    def to_conditional(self, true_label: Label, false_label: Label):
        name = 'true'
        return JumpC(JumpTypeEnum.EQ, self.expression, Temp(name, None, None), true_label, false_label)
