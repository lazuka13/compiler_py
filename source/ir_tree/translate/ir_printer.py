from ir_tree.ir_visitor import IRVisitor
from ir_tree.list import ExpList
from ir_tree.statements.all import *
from ir_tree.expressions.all import *
from ir_tree.translate.exp_wrapper import ExpWrapper
from ir_tree.translate.stm_wrapper import StmWrapper
from syntax_tree import Visitable


class IRPrinter(IRVisitor):
    def __init__(self, path):
        IRVisitor.__init__(self)
        self.path = path
        self.out = 'digraph g {graph [ rankdir = LR ]; ' \
                   'node [fontsize="18" shape="record"]; ' \
                   'edge [];' \
                   '\n'

    def print_to_file(self):
        self.out = self.out + "}"
        with open(self.path, 'w+') as file:
            file.write(self.out)
        print(f'IR Tree сохранено в файл {self.path}')

    def print_edge(self, obj_from, obj_to, label=None):
        if label is None:
            self.out = self.out + "\tnode" + str(id(obj_from)) + "->" + "node" + str(id(obj_to)) + "\n"
        else:
            self.out = self.out + "\tnode" + str(id(obj_from)) + "->" + "node" + str(
                id(obj_to)) + "[label=\"" + label + "\"]\n"

    def print_vertex(self, node, label):
        self.out = self.out + "\tnode" + str(id(node)) + "[label=\"" + str(label) + "\"]\n"

    def create_graph(self, forest: dict):
        for tree in forest.items():
            self.print_vertex(tree[0], f'Method | {tree[0]}')
            tree[1].accept(self)
            self.print_edge(tree[0], tree[1])

    def visit(self, obj: Visitable):
        if isinstance(obj, UnaryOp):
            self.visit_unary_op(obj)
        elif isinstance(obj, Binop):
            self.visit_binop(obj)
        elif isinstance(obj, Call):
            self.visit_call(obj)
        elif isinstance(obj, Const):
            self.visit_const(obj)
        elif isinstance(obj, Eseq):
            self.visit_eseq(obj)
        elif isinstance(obj, Mem):
            self.visit_mem(obj)
        elif isinstance(obj, Name):
            self.visit_name(obj)
        elif isinstance(obj, Temp):
            self.visit_temp(obj)
        elif isinstance(obj, Exp):
            self.visit_exp(obj)
        elif isinstance(obj, Jump):
            self.visit_jump(obj)
        elif isinstance(obj, JumpC):
            self.visit_jumpc(obj)
        elif isinstance(obj, LabelStm):
            self.visit_label_stm(obj)
        elif isinstance(obj, Move):
            self.visit_move(obj)
        elif isinstance(obj, Seq):
            self.visit_seq(obj)
        elif isinstance(obj, ExpList):
            self.visit_exp_list(obj)
        elif isinstance(obj, StmWrapper):
            self.visit_stm_wrapper(obj)
        elif isinstance(obj, ExpWrapper):
            self.visit_exp_wrapper(obj)

    def visit_unary_op(self, obj: UnaryOp):
        self.print_vertex(obj, f'Unary | {obj.operation} | {obj.position}')
        obj.expression.accept(self)
        self.print_edge(obj, obj.expression)

    def visit_binop(self, obj: Binop):
        self.print_vertex(obj, f'Binary | {obj.operation} | {obj.position}')
        obj.left_expression.accept(self)
        obj.right_expression.accept(self)
        self.print_edge(obj, obj.left_expression)
        self.print_edge(obj, obj.right_expression)

    def visit_call(self, obj: Call):
        self.print_vertex(obj, f'Call | {obj.position}')
        obj.args.accept(self)
        obj.func_expr.accept(self)
        self.print_edge(obj, obj.args)
        self.print_edge(obj, obj.func_expr)

    def visit_const(self, obj: Const):
        self.print_vertex(obj, f'Const | {str(obj.value)} | {obj.position}')

    def visit_eseq(self, obj: Eseq):
        self.print_vertex(obj, f'Eseq | {obj.position}')
        obj.statement.accept(self)
        obj.expression.accept(self)
        self.print_edge(obj, obj.statement)
        self.print_edge(obj, obj.expression)

    def visit_mem(self, obj: Mem):
        self.print_vertex(obj, f'Mem | {obj.position}')
        obj.expression.accept(self)
        self.print_edge(obj, obj.expression)

    def visit_name(self, obj: Name):
        self.print_vertex(obj, f'Name | {str(obj.label_name.name)} | {obj.position}')

    def visit_temp(self, obj: Temp):
        self.print_vertex(obj, f'Temp | {self.format_temp(obj)} | {obj.position}')

    def visit_exp(self, obj: Exp):
        self.print_vertex(obj, f'Exp | {obj.position}')
        obj.expression.accept(self)
        self.print_vertex(obj, obj.expression)

    def visit_jump(self, obj: Jump):
        self.print_vertex(obj, f'Jump | {obj.label_to_jump.name} | {obj.position}')

    def visit_jumpc(self, obj: JumpC):
        self.print_vertex(obj, f'JumpC | {self.format_jump_type(obj.jump_type_enum)} | '
                               f'True: {obj.true_label.name} | '
                               f'False: {obj.true_label.name} | '
                               f'{obj.position}')
        obj.condition_left_expression.accept(self)
        obj.condition_right_expression.accept(self)
        self.print_edge(obj, obj.condition_left_expression)
        self.print_edge(obj, obj.condition_right_expression)

    def visit_label_stm(self, obj: LabelStm):
        self.print_vertex(obj, f'LabrlStm | {obj.label_name.name} | {obj.position}')

    def visit_move(self, obj: Move):
        self.print_vertex(obj, f'Move | {obj.position}')
        obj.source.accept(self)
        obj.destination.accept(self)
        self.print_edge(obj, obj.source)
        self.print_edge(obj, obj.destination)

    def visit_seq(self, obj: Seq):
        self.print_vertex(obj, f'Seq | {obj.position}')
        if obj.head is not None:
            obj.head.accept(self)
            self.print_edge(obj, obj.head)
        if obj.tail is not None:
            obj.tail.accept(self)
            self.print_edge(obj, obj.tail)

    def visit_exp_list(self, obj: ExpList):
        self.print_vertex(obj, f'ExpList | {obj.position}')
        if obj.head is not None:
            obj.head.accept(self)
            self.print_edge(obj, obj.head)
        if obj.tail is not None:
            obj.tail.accept(self)
            self.print_edge(obj, obj.tail)

    def visit_stm_wrapper(self, obj: StmWrapper):
        obj.statement.accept(self)

    def visit_exp_wrapper(self, obj: ExpWrapper):
        obj.expression.accept(self)

    def format_binop(self, binop_enum: BinopEnum):
        if binop_enum == BinopEnum.MOD:
            return 'MOD'
        elif binop_enum == BinopEnum.MUL:
            return 'MUL'
        elif binop_enum == BinopEnum.PLUS:
            return 'PLUS'
        elif binop_enum == BinopEnum.MINUS:
            return 'MINUS'
        elif binop_enum == BinopEnum.OR:
            return 'OR'
        elif binop_enum == BinopEnum.AND:
            return 'AND'
        else:
            assert False

    def format_jump_type(self, jump_type_enum: JumpTypeEnum):
        if jump_type_enum == JumpTypeEnum.EQ:
            return '=='
        elif jump_type_enum == JumpTypeEnum.LT:
            return '\\<'
        elif jump_type_enum == JumpTypeEnum.NEQ:
            return '!='
        else:
            assert False

    def format_temp(self, temp: Temp):
        assert temp is not None
        if temp.info_enum == InfoEnum.ID:
            return f'ID: {str(temp.id)} | {str(temp.local_id)}'
        elif temp.info_enum == InfoEnum.NAME:
            return f'ID: {str(temp.id)} | {temp.name}'
        else:
            assert False
