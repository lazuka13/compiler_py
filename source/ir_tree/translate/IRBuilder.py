from symbol_table.Table import Table
from syntax_tree import *


class IRBuilder(Visitor):
    def __init__(self, table: Table):
        Visitor.__init__(self)
        self.table = table
        self.main_subtree = None
        self.trees = []
        self.current_frame = 0

    def parse(self, program: Program):
        program.accept(self)

    def get_parse_result(self):
        return self.trees

    def visit(self, obj: Visitable):
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

    def visit_program(self, obj: Program):
        obj.main.accept(self)
        for class_decl in obj.class_decl_list:
            class_decl.accept(self)

    def visit_main_class(self, obj: MainClass):
        for statement in obj.statement_list:
            statement.accept(self)
        assert self.main_subtree is not None
        self.trees[obj.id.name] = self.main_subtree

    def visit_class_decl(self, obj: ClassDecl):
        

    def visit_var_decl(self, obj: VarDecl):
        pass

    def visit_arg_decl(self, obj: ArgDecl):
        pass

    def visit_method_decl(self, obj: MethodDecl):
        pass

    def visit_binary_expr(self, obj: BinaryExpr):
        pass

    def visit_id(self, obj: Id):
        pass

    def visit_true_expr(self, obj: TrueExpr):
        pass

    def visit_false_expr(self, obj: FalseExpr):
        pass

    def visit_integer_expr(self, obj: IntegerExpr):
        pass

    def visit_assign_statement(self, obj: AssignStatement):
        pass

    def visit_not_expr(self, obj: NotExpr):
        pass

    def visit_call_method_expr(self, obj: CallMethodExpr):
        pass

    def visit_new_int_array_expr(self, obj: NewIntArrExpr):
        pass

    def visit_new_object_expr(self, obj: NewObjectExpr):
        pass

    def visit_random_access_assign_statement(self, obj: RandomAccessAssignStatement):
        pass

    def visit_length_expr(self, obj: LengthExpr):
        pass

    def visit_print_line_statement(self, obj: PrintLineStatement):
        pass

    def visit_if_statement(self, obj : IfStatement):
        pass

    def visit_while_statement(self, obj: WhileStatement):
        pass

    def visit_statements(self, obj: Statements):
        pass

    def visit_random_access_expr(self, obj: RandomAccessExpr):
        pass

    def visit_this_expr(self, obj: ThisExpr):
        pass
