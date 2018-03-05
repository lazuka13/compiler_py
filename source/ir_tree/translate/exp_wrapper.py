from .i_subtree_wrapper import ISubtreeWrapper
from ir_tree.expressions.i_exp import IExp
from ir_tree.statements.exp import Exp
from ir_tree.label import Label
from ir_tree.statements.jumpc import JumpC, JumpTypeEnum
from ir_tree.expressions.temp import Temp


class ExpWrapper(ISubtreeWrapper):
    def __init__(self, expression: IExp):
        self.expression = expression

    def to_exp(self):
        return self.expression

    def to_stm(self):
        return Exp(self.expression)

    def to_conditional(self, jump_type: JumpTypeEnum, true_label: Label):
        name = 'true'
        return JumpC(jump_type, self.expression, Temp(name, None, None), true_label)
