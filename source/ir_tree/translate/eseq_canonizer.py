from ir_tree.expressions.all import *
from ir_tree.expressions.i_exp import IExp
from ir_tree.ir_visitor import IRVisitor
from ir_tree.list import ExpList
from ir_tree.statements.all import *
from ir_tree.statements.i_stm import IStm
from ir_tree.translate.exp_wrapper import ExpWrapper
from ir_tree.translate.i_subtree_wrapper import ISubtreeWrapper
from ir_tree.translate.stm_wrapper import StmWrapper
from syntax_tree import Visitable


class EseqCanonizer(IRVisitor):
    def __init__(self):
        IRVisitor.__init__(self)
        self.last_eseq = Eseq(None, None)

    def canonize(self, wrapper: ISubtreeWrapper):
        self.last_eseq = Eseq(None, None)
        wrapper.accept(self)
        stm_wrapper = StmWrapper(self.last_eseq.statement)
        self.last_eseq.statement = None
        return stm_wrapper

    def reorder(self, exp: IExp):
        exp.accept(self)
        exp = None
        self.decompose_eseq()
        exp = self.last_eseq.expression
        self.last_eseq.expression = None
        statement = self.last_eseq.statement
        self.last_eseq.statement = None
        return statement, exp

    def add_seq_if_required(self, stm: IStm):
        assert stm is not None
        if self.last_eseq.statement is None:
            return stm
        else:
            statement = self.last_eseq.statement
            self.last_eseq.statement = None
            return Seq(statement, stm)

    def decompose_eseq(self):
        if self.last_eseq.statement is None or self.last_eseq.expression is None:
            return
        if self.last_eseq.expression.is_commutative():
            return
        else:
            holder: Temp = Temp(None, Temp.temp_holder_local_id, None)
            statement, expression = self.last_eseq.statement, self.last_eseq.expression
            self.last_eseq.statement = None, None
            self.last_eseq.statement = Seq(statement, Move(holder, expression))
            self.last_eseq.expression = Mem(Temp(None, None, holder))

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

    def visit_unary_op(self, obj: UnaryOp):
        self.last_eseq.statement, obj.expression = self.reorder(obj.expression)
        self.last_eseq.expression = obj

    def visit_binop(self, obj: Binop):
        left_statements, obj.left_expression = self.reorder(obj.left_expression)
        right_statements, obj.right_expression = self.reorder(obj.right_expression)
        self.last_eseq.statement = Seq(left_statements, right_statements)
        self.last_eseq.expression = obj

    def visit_call(self, obj: Call):
        obj.args.accept(self)
        obj.args = None
        obj.args = self.last_eseq.expression
        self.last_eseq.expression = None
        self.last_eseq.statement, obj.func_expr = self.reorder(obj.func_expr)
        self.last_eseq.expression = obj

    def visit_const(self, obj: Const):
        self.last_eseq.expression = obj

    def visit_eseq(self, obj: Eseq):
        obj.statement.accept(self)
        obj.statement = None
        self.last_eseq.statement, obj.expression = self.reorder(obj.expression)
        self.last_eseq.expression = obj.expression
        obj.expression = None
        del obj

    def visit_mem(self, obj: Mem):
        obj.expression.accept(self)
        obj.expression = None
        obj.expression = self.last_eseq.expression
        self.last_eseq.expression = None
        self.last_eseq.expression = obj

    def visit_name(self, obj: Name):
        self.last_eseq.expression = obj

    def visit_temp(self, obj: Temp):
        self.last_eseq.expression = obj

    def visit_exp(self, obj: Exp):
        stm, obj.expression = self.reorder(obj.expression)
        if stm is not None:
            self.last_eseq.statement = self.add_seq_if_required(stm)
        self.last_eseq.statement = self.add_seq_if_required(obj)

    def visit_jump(self, obj: Jump):
        self.last_eseq.statement = self.add_seq_if_required(obj)

    def visit_jumpc(self, obj: JumpC):
        left_statements, obj.condition_left_expression = self.reorder(obj.condition_left_expression)
        right_statements, obj.condition_right_expression = self.reorder(obj.condition_right_expression)
        if left_statements is not None:
            self.last_eseq.statement = self.add_seq_if_required(left_statements)
        if right_statements is not None:
            self.last_eseq.statement = self.add_seq_if_required(right_statements)
        self.last_eseq.statement = self.add_seq_if_required(obj)

    def visit_label_stm(self, obj: LabelStm):
        self.last_eseq.statement = self.add_seq_if_required(obj)

    def visit_move(self, obj: Move):
        src, obj.source = self.reorder(obj.source)
        dst, obj.destination = self.reorder(obj.destination)
        if src is not None:
            self.last_eseq.statement = self.add_seq_if_required(src)
        if dst is not None:
            self.last_eseq.statement = self.add_seq_if_required(dst)
        self.last_eseq.statement = self.add_seq_if_required(obj)

    def visit_seq(self, obj: Seq):
        obj.head.accept(self)
        obj.head = None
        if obj.tail is not None:
            obj.tail.accept(self)
        obj.tail = None
        del obj

    def visit_exp_list(self, obj: ExpList):
        if obj.head is not None:
            stm, obj.head = self.reorder(obj.head)
            if stm is not None:
                self.last_eseq.statement = self.add_seq_if_required(stm)

        if obj.tail is not None:
            obj.tail.accept(self)
            obj.tail = None
            obj.tail = self.last_eseq.expression
            self.last_eseq.expression = None

        self.last_eseq.expression = obj

    def visit_stm_wrapper(self, obj: StmWrapper):
        obj.to_stm().accept(self)

    def visit_exp_wrapper(self, obj: ExpWrapper):
        obj.to_stm().accept(self)
