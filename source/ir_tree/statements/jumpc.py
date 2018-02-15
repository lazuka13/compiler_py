from .i_stm import IStm
from ir_tree.expressions.i_exp import IExp
from ir_tree.label import Label
from enum import Enum
from syntax_tree import Position


class JumpTypeEnum(Enum):
    EQ = 1
    NEQ = 2
    LT = 3


class JumpC(IStm):
    def __init__(self, jump_type_enum: JumpTypeEnum, condition_left_expression: IExp,
                 condition_right_expression: IExp, true_label: Label, false_label: Label,
                 position: Position = Position(0, 0)):
        IStm.__init__(self, position)

        self.true_label = true_label
        self.false_label = false_label
        self.condition_left_expression = condition_left_expression
        self.condition_right_expression = condition_right_expression
        self.jump_type_enum = jump_type_enum
