from typing import List

from ir_tree.expressions.all import *
from ir_tree.ir_visitor import IRVisitor
from ir_tree.list import ExpList
from ir_tree.statements.all import *
from ir_tree.statements.i_stm import IStm
from ir_tree.translate.exp_wrapper import ExpWrapper
from ir_tree.translate.i_subtree_wrapper import ISubtreeWrapper
from ir_tree.translate.stm_wrapper import StmWrapper
from syntax_tree import Visitable


class Linearizer(IRVisitor):
    def __init__(self):
        IRVisitor.__init__(self)
        self.statements = None
        self.is_previous_detached = False

    def linearize(self, wrapper: ISubtreeWrapper, stms: List[IStm]):
        assert self.statements is None
        self.is_previous_detached = False
        self.statements = stms
        wrapper.accept(self)
        self.statements = None

    def add_to_statements(self, stm: IStm):
        self.statements.append(stm)
        self.is_previous_detached = True

    def visit(self, visitable: Visitable):
        if isinstance(visitable, UnaryOp):
            self.visit_unary_op(visitable)
        elif isinstance(visitable, Binop):
            self.visit_binop(visitable)
        elif isinstance(visitable, Call):
            self.visit_call(visitable)
        elif isinstance(visitable, Const):
            self.visit_const(visitable)
        elif isinstance(visitable, Eseq):
            self.visit_eseq(visitable)
        elif isinstance(visitable, Mem):
            self.visit_mem(visitable)
        elif isinstance(visitable, Name):
            self.visit_name(visitable)
        elif isinstance(visitable, Temp):
            self.visit_temp(visitable)
        elif isinstance(visitable, Exp):
            self.visit_exp(visitable)
        elif isinstance(visitable, Jump):
            self.visit_jump(visitable)
        elif isinstance(visitable, JumpC):
            self.visit_jumpc(visitable)
        elif isinstance(visitable, LabelStm):
            self.visit_label_stm(visitable)
        elif isinstance(visitable, Move):
            self.visit_move(visitable)
        elif isinstance(visitable, Seq):
            self.visit_seq(visitable)
        elif isinstance(visitable, ExpList):
            self.visit_exp_list(visitable)
        elif isinstance(visitable, StmWrapper):
            self.visit_stm_wrapper(visitable)
        elif isinstance(visitable, ExpWrapper):
            self.visit_exp_wrapper(visitable)

    def visit_unary_op(self, _: UnaryOp):
        assert False

    def visit_binop(self, _: Binop):
        assert False

    def visit_call(self, _: Call):
        assert False

    def visit_const(self, _: Const):
        assert False

    def visit_eseq(self, _: Eseq):
        assert False

    def visit_mem(self, _: Mem):
        assert False

    def visit_name(self, _: Name):
        assert False

    def visit_temp(self, _: Temp):
        assert False

    def visit_exp_list(self, _: ExpList):
        assert False

    def visit_exp(self, obj: Exp):
        self.add_to_statements(obj)

    def visit_jump(self, obj: Jump):
        self.add_to_statements(obj)

    def visit_jumpc(self, obj: JumpC):
        self.add_to_statements(obj)

    def visit_label_stm(self, obj: LabelStm):
        self.add_to_statements(obj)

    def visit_move(self, obj: Move):
        self.add_to_statements(obj)

    def visit_seq(self, obj: Seq):
        if obj.head is not None:
            obj.head.accept(self)
            if self.is_previous_detached:
                self.is_previous_detached = False
        if obj.tail is not None:
            obj.tail.accept(self)
            if self.is_previous_detached:
                self.is_previous_detached = False

    def visit_stm_wrapper(self, obj: StmWrapper):
        stm = obj.to_stm()
        stm.accept(self)

    def visit_exp_wrapper(self, obj: ExpWrapper):
        stm = obj.to_stm()
        stm.accept(self)
