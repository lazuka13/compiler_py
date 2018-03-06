from syntax_tree import Position

from ir_tree.expressions.i_exp import IExp
from ir_tree.expressions.all import *
from ir_tree.statements.all import *

ELEMENTS_OFFSET = 1


def get_element(base: IExp, element_number: IExp, position: Position):
    return Mem(
        Binop(
            BinopEnum.PLUS,
            Binop(
                BinopEnum.PLUS,
                base,
                Const(
                    ELEMENTS_OFFSET,
                    position
                ),
                position
            ),
            element_number,
            position
        ),
        position
    )


def get_length(base: IExp, position: Position):
    return Mem(base, position)
