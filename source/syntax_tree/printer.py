from .base import *
from .declarations import *
from .expressions import *
from .grammar import *
from .statements import *


class Printer(Visitor):
    def __init__(self, path):
        Visitor.__init__(self)
        self.path = path
        self.out = "digraph g {\n\n"

    def print_to_file(self):
        self.out = self.out + "}"
        with open(self.path, 'w+') as file:
            file.write(self.out)
        print(f'Абстрактное синтаксическое дерево сохранено в файл {self.path}')

    def print_edge(self, obj_from, obj_to, label=None):
        if label is None:
            self.out = self.out + "\tnode" + str(id(obj_from)) + "->" + "node" + str(id(obj_to)) + "\n"
        else:
            self.out = self.out + "\tnode" + str(id(obj_from)) + "->" + "node" + str(
                id(obj_to)) + "[label=\"" + label + "\"]\n"

    def print_vertex(self, node, label):
        self.out = self.out + "\tnode" + str(id(node)) + "[label=\"" + str(label) + "\"]\n"

    def visit(self, obj):
        if isinstance(obj, BinaryExpr):
            self.visit_binary_expr(obj)
        elif isinstance(obj, Id):
            self.visit_id(obj)
        elif isinstance(obj, TrueExpr):
            self.visit_true_expr(obj)
        elif isinstance(obj, FalseExpr):
            self.visit_false_expr(obj)
        elif isinstance(obj, ClassDecl):
            self.visit_class_decl(obj)
        elif isinstance(obj, MainClass):
            self.visit_main_class(obj)
        elif isinstance(obj, MethodDecl):
            self.visit_method_decl(obj)
        elif isinstance(obj, Program):
            self.visit_program(obj)
        elif isinstance(obj, IntegerExpr):
            self.visit_integer_expr(obj)
        elif isinstance(obj, AssignStatement):
            self.visit_assign_statement(obj)
        elif isinstance(obj, IfStatement):
            self.visit_if_statement(obj)
        elif isinstance(obj, NotExpr):
            self.visit_not_expr(obj)
        elif isinstance(obj, CallMethodExpr):
            self.visit_call_method_expr(obj)
        elif isinstance(obj, NewIntArrExpr):
            self.visit_new_int_array_expr(obj)
        elif isinstance(obj, NewObjectExpr):
            self.visit_new_object_expr(obj)
        elif isinstance(obj, RandomAccessAssignStatement):
            self.visit_random_access_assign_statement(obj)
        elif isinstance(obj, LengthExpr):
            self.visit_length_expr(obj)
        elif isinstance(obj, PrintLineStatement):
            self.visit_print_line_statement(obj)
        elif isinstance(obj, WhileStatement):
            self.visit_while_statement(obj)
        elif isinstance(obj, Statements):
            self.visit_statements(obj)
        elif isinstance(obj, RandomAccessExpr):
            self.visit_random_access_expr(obj)
        elif isinstance(obj, ArgDecl):
            self.visit_arg_decl(obj)
        elif isinstance(obj, VarDecl):
            self.visit_var_decl(obj)
        elif isinstance(obj, ThisExpr):
            self.visit_this_expr(obj)

    def visit_binary_expr(self, obj: BinaryExpr):
        self.print_vertex(obj, obj.label)
        obj.left.accept(self)
        obj.right.accept(self)
        self.print_edge(obj, obj.right, 'right')
        self.print_edge(obj, obj.left, 'left')

    def visit_id(self, obj):
        self.print_vertex(obj, f'id: {obj.name}')

    def visit_true_expr(self, obj):
        self.print_vertex(obj, 'True')

    def visit_false_expr(self, obj):
        self.print_vertex(obj, 'False')

    def visit_class_decl(self, obj: ClassDecl):
        self.print_vertex(obj, 'Class')
        obj.id.accept(self)
        self.print_edge(obj, obj.id)
        if obj.method_decl_list is not None:
            for method in obj.method_decl_list:
                method.accept(self)
                self.print_edge(obj, method)

    def visit_main_class(self, obj: MainClass):
        self.print_vertex(obj, "Main")
        obj.id.accept(self)
        self.print_edge(obj, obj.id)
        obj.param_id.accept(self)
        self.print_edge(obj, obj.param_id, 'param_id')
        if obj.statement_list is not None:
            for statement in obj.statement_list:
                statement.accept(self)
                self.print_edge(obj, statement, 'statement')

    def visit_method_decl(self, obj: MethodDecl):
        self.print_vertex(obj, 'method ' + obj.type_of.label + ' ' + obj.access_modifier)
        obj.id.accept(self)
        self.print_edge(obj, obj.id)
        if obj.var_decl_list is not None:
            for var in obj.var_decl_list:
                var.accept(self)
                self.print_edge(obj, var, 'var')
        if obj.statement_list is not None:
            for statement in obj.statement_list:
                statement.accept(self)
                self.print_edge(obj, statement)
        if obj.arg_decl_list is not None:
            for arg in obj.arg_decl_list:
                arg.accept(self)
                self.print_edge(obj, arg, 'arg')
        obj.result.accept(self)
        self.print_edge(obj, obj.result, 'result')

    def visit_program(self, obj: Program):
        self.print_vertex(obj, "Program")
        obj.main.accept(self)
        self.print_edge(obj, obj.main, label='PROGRAM TO MAIN')
        if obj.class_decl_list is not None:
            for class_decl in obj.class_decl_list:
                class_decl.accept(self)
                self.print_edge(obj, class_decl)

    def visit_integer_expr(self, obj: IntegerExpr):
        self.print_vertex(obj, f'int: {obj.value}')

    def visit_assign_statement(self, obj: AssignStatement):
        self.print_vertex(obj, '=')
        obj.left.accept(self)
        obj.right.accept(self)
        self.print_edge(obj, obj.left, 'left')
        self.print_edge(obj, obj.right, 'right')

    def visit_if_statement(self, obj: IfStatement):
        self.print_vertex(obj, 'if')
        obj.condition.accept(self)
        self.print_edge(obj, obj.condition, 'condition')
        obj.if_false.accept(self)
        self.print_edge(obj, obj.if_false, 'if_false')
        obj.if_true.accept(self)
        self.print_edge(obj, obj.if_true, 'if_true')

    def visit_not_expr(self, obj: NotExpr):
        self.print_vertex(obj, 'not_expression')
        obj.right.accept(self)
        self.print_edge(obj, obj.right)

    def visit_call_method_expr(self, obj: CallMethodExpr):
        self.print_vertex(obj, 'call_method')
        obj.id.accept(self)
        self.print_edge(obj, obj.id)
        obj.expr.accept(self)
        self.print_edge(obj, obj.expr)
        if obj.expr_list is not None:
            for param in obj.expr_list:
                param.accept(self)
                self.print_edge(obj, param, 'parameter')

    def visit_new_int_array_expr(self, obj: NewIntArrExpr):
        self.print_vertex(obj, 'new int []')
        obj.size.accept(self)
        self.print_edge(obj, obj.size, 'size')

    def visit_new_object_expr(self, obj: NewObjectExpr):
        self.print_vertex(obj, 'new')
        obj.id.accept(self)
        self.print_edge(obj, obj.id)

    def visit_random_access_assign_statement(self, obj: RandomAccessAssignStatement):
        self.print_vertex(obj, '=')
        obj.id.accept(self)
        self.print_edge(obj, obj.id, 'array')
        obj.position_in_arr.accept(self)
        self.print_edge(obj, obj.position_in_arr, 'position')
        obj.expr.accept(self)
        self.print_edge(obj, obj.expr)

    def visit_length_expr(self, obj):
        self.print_vertex(obj, 'length')
        obj.obj.accept(self)
        self.print_edge(obj, obj.obj, 'object')

    def visit_print_line_statement(self, obj: PrintLineStatement):
        self.print_vertex(obj, 'print_line_statement')
        obj.obj.accept(self)
        self.print_edge(obj, obj.obj)

    def visit_while_statement(self, obj: WhileStatement):
        self.print_vertex(obj, 'while')
        obj.condition.accept(self)
        self.print_edge(obj, obj.condition, 'condition')
        obj.action.accept(self)
        self.print_edge(obj, obj.action, 'action')

    def visit_statements(self, obj: Statements):
        self.print_vertex(obj, 'statements')
        if obj.statement_list is not None:
            for statement in obj.statement_list:
                statement.accept(self)
                self.print_edge(obj, statement)

    def visit_random_access_expr(self, obj: RandomAccessExpr):
        self.print_vertex(obj, 'access_to_position')
        obj.object.accept(self)
        self.print_edge(obj, obj.object, 'object')
        obj.position_in_arr.accept(self)
        self.print_edge(obj, obj.position, 'position')

    def visit_arg_decl(self, obj: ArgDecl):
        self.print_vertex(obj, obj.type_of.label)
        obj.id.accept(self)
        self.print_edge(obj, obj.id)

    def visit_var_decl(self, obj: VarDecl):
        self.print_vertex(obj, obj.type_of.label + " " + obj.id.name)

    def visit_this_expr(self, obj: ThisExpr):
        self.print_vertex(obj, 'this')
