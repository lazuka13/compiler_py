from symbol_table.class_info import ClassInfo
from symbol_table.method_info import MethodInfo, AccessModifierEnum
from symbol_table.table import Table
from symbol_table.type_info import TypeInfo, TypeEnum
from symbol_table.variable_info import VariableInfo
from symbol_table.type_stack_visitor import TypeScopeSwitcher, TypeStackVisitor, MethodScopeSwitcher
from syntax_tree import *

# создадим несколько сокращений для проверки типов #
IntType = TypeInfo(TypeEnum.INT, None)
BooleanType = TypeInfo(TypeEnum.BOOLEAN, None)
IntArrayType = TypeInfo(TypeEnum.INT_ARRAY, None)


class TypeChecker(Visitor):
    """
    Проверка типов
    Передаем таблицу и само дерево снаружи, тайпчекер
    не занимается построением, только обрабатывает построенное

    Идея проста - есть стек типов, закидываем в него при обходе полученные типы, при проверке
    достаем тип и сверяем. Например, разберем случай:

    if (3 < 5) { ... }
    1) в обходе if (3 < 5) как IfStatement вызывается обход 3 < 5 как BinaryExpr
    2) в обходе 3 < 5 в стек кладется BooleanType, обход завершается
    3) в продолжении обхода if (3 < 5) из стека извлекается тип - проверяем, Boolean ли он

    Тут используется TypeStackVisitor, именно в нем хранится стек типов, он нужен для сокращения
    кода (потом используется в IR_Tree)
    """

    def __init__(self, table, verbose=False):
        """
        Конструктор
        """
        Visitor.__init__(self)
        self.table = table
        self.verbose = verbose
        self.type_stack_visitor = TypeStackVisitor(self.table)

    def check_ast_st(self, program: Program):
        """
        Отвечает за проверку дерева на соответствие типов
        :param program: корень абстрактного синтаксического дерева
        :param symbol_table: символьная таблица для дерева
        :return:
        """
        try:
            program.accept(self)
        except SyntaxError as error:
            print(error)
        else:
            if self.verbose:
                print('Проверка типов пройдена успешно!')

    def visit(self, visitable: Visitable):
        """
        Отвечает за посещение узлов дерева
        :param visitable: посещаемый узел AST
        :return:
        """
        if isinstance(visitable, Program):
            self.visit_program(visitable)
        elif isinstance(visitable, MainClass):
            self.visit_main_class(visitable)
        elif isinstance(visitable, ClassDecl):
            self.visit_class_decl(visitable)
        elif isinstance(visitable, VarDecl):
            self.visit_var_decl(visitable)
        elif isinstance(visitable, ArgDecl):
            self.visit_arg_decl(visitable)
        elif isinstance(visitable, MethodDecl):
            self.visit_method_decl(visitable)
        elif isinstance(visitable, RandomAccessAssignStatement):
            self.visit_random_access_assign_statement(visitable)
        elif isinstance(visitable, AssignStatement):
            self.visit_assign_statement(visitable)
        elif isinstance(visitable, PrintLineStatement):
            self.visit_print_line_statement(visitable)
        elif isinstance(visitable, WhileStatement):
            self.visit_while_statement(visitable)
        elif isinstance(visitable, Statements):
            self.visit_statements(visitable)
        elif isinstance(visitable, IfStatement):
            self.visit_if_statement(visitable)
        elif isinstance(visitable, BinaryExpr):
            self.visit_binary_expr(visitable)
        elif isinstance(visitable, RandomAccessExpr):
            self.visit_random_access_expr(visitable)
        elif isinstance(visitable, LengthExpr):
            self.visit_length_expr(visitable)
        elif isinstance(visitable, CallMethodExpr):
            self.visit_call_method_expr(visitable)
        elif isinstance(visitable, ValueExpr):
            self.visit_value_expr(visitable)
        elif isinstance(visitable, Id):
            self.visit_id(visitable)
        elif isinstance(visitable, ThisExpr):
            self.visit_this_expr(visitable)
        elif isinstance(visitable, NewObjectExpr):
            self.visit_new_object_expr(visitable)
        elif isinstance(visitable, NewIntArrExpr):
            self.visit_new_int_arr_expr(visitable)
        elif isinstance(visitable, NotExpr):
            self.visit_not_expr(visitable)
        elif isinstance(visitable, ReturnStatement):
            self.visit_return_statement(visitable)

    def visit_program(self, program: Program):
        program.main.accept(self)
        for cls in program.class_decl_list:
            cls.accept(self)

    def visit_main_class(self, main_class: MainClass):
        for statement in main_class.statement_list:
            statement.accept(self)

    def visit_class_decl(self, class_decl: ClassDecl):
        switcher = TypeScopeSwitcher(None, class_decl.id.name, self.table, class_decl.position)
        for method in class_decl.method_decl_list:
            method.accept(self)
        switcher.destroy()

    def visit_var_decl(self, var_decl: VarDecl):
        if TypeInfo.from_type(var_decl.type_of).type_enum == TypeEnum.USER_CLASS:
            self.table.get_class(var_decl.type_of.label, var_decl.position)

    def visit_arg_decl(self, arg_decl: ArgDecl):
        if TypeInfo.from_type(arg_decl.type_of).type_enum == TypeEnum.USER_CLASS:
            self.table.get_class(arg_decl.type_of.label, arg_decl.position)

    def visit_method_decl(self, method_decl: MethodDecl):
        switcher = MethodScopeSwitcher(None, method_decl.id.name, self.table, method_decl.position)
        for arg_decl in method_decl.arg_decl_list:
            arg_decl.accept(self)
        for var_decl in method_decl.var_decl_list:
            var_decl.accept(self)
        for statement in method_decl.statement_list:
            statement.accept(self)
        method_decl.return_statement.accept(self)
        returned = self.type_stack_visitor.pop_type_from_stack()
        if returned != TypeInfo.from_type(method_decl.type_of):
            raise SyntaxError(f'Trying to return type {returned.get_type_string()} from method '
                              f'{method_decl.id.name} of type {method_decl.type_of}! Position {method_decl.position}')
        switcher.destroy()

    def visit_random_access_assign_statement(self, raa_statement: RandomAccessAssignStatement):
        var_info: VariableInfo = self.table.get_variable(raa_statement.id.name, raa_statement.position)
        if var_info.type_of.type_enum != TypeEnum.INT_ARRAY:
            raise SyntaxError(f'Trying to subscript {var_info.type_of.get_type_string()} as array! '
                              f'Position {raa_statement.position}')  # TODO Переписать на другой ошибке!
        raa_statement.position_in_arr.accept(self)
        returned: TypeInfo = self.type_stack_visitor.pop_type_from_stack()
        if returned.type_enum != TypeEnum.INT:
            raise SyntaxError(f'Trying to use type {returned.get_type_string()} as index of array! '
                              f'Position {raa_statement.position}')
        raa_statement.expr.accept(self)
        returned: TypeInfo = self.type_stack_visitor.pop_type_from_stack()
        if returned.type_enum != TypeEnum.INT:
            raise SyntaxError(f'Trying to assign type {returned.get_type_string()} to element of int array! '
                              f'Position {raa_statement.position}')

    def visit_assign_statement(self, assign_statement: AssignStatement):
        var_info: VariableInfo = self.table.get_variable(assign_statement.left.name, assign_statement.position)
        assign_statement.right.accept(self)
        returned = self.type_stack_visitor.pop_type_from_stack()
        if var_info.type_of != returned:
            raise SyntaxError(f'Trying to assign value of type {returned.get_type_string()} to variable '
                              f'of type {var_info.type_of.get_type_string()}! Position {assign_statement.position}')

    def visit_print_line_statement(self, print_line_statement: PrintLineStatement):
        print_line_statement.obj.accept(self)
        returned: TypeInfo = self.type_stack_visitor.pop_type_from_stack()
        if returned.type_enum == TypeEnum.USER_CLASS:
            raise SyntaxError(f'Trying to return user type {returned.get_type_string()}! '
                              f'Position {print_line_statement.position}')

    def visit_while_statement(self, while_statement: WhileStatement):
        while_statement.condition.accept(self)
        returned = self.type_stack_visitor.pop_type_from_stack()
        if returned.type_enum != TypeEnum.BOOLEAN:
            raise SyntaxError(f'Trying to use type {returned.get_type_string()} as condition! '
                              f'Position {while_statement.position}')

    def visit_statements(self, statements: Statements):
        for statement in statements.statement_list:
            statement.accept(self)

    def visit_if_statement(self, if_statement: IfStatement):
        if_statement.condition.accept(self)
        returned = self.type_stack_visitor.pop_type_from_stack()
        if returned.type_enum != TypeEnum.BOOLEAN:
            raise SyntaxError(f'Trying to use type {returned.get_type_string()} as condition! '
                              f'Position {if_statement.position}')
        if_statement.if_false.accept(self)
        if_statement.if_true.accept(self)

    def visit_binary_expr(self, binary_expr: BinaryExpr):
        binary_expr.left.accept(self)
        returned = self.type_stack_visitor.pop_type_from_stack()
        if binary_expr.binary_enum in [BinaryEnum.PLUS, BinaryEnum.MULT, BinaryEnum.MINUS, BinaryEnum.MOD,
                                       BinaryEnum.LESS]:
            if returned.type_enum != TypeEnum.INT:
                raise SyntaxError(f'Trying to apply math operation to type {returned.get_type_string()}! '
                                  f'Position {binary_expr.position}')
            binary_expr.right.accept(self)
            returned = self.type_stack_visitor.pop_type_from_stack()
            if returned.type_enum != TypeEnum.INT:
                raise SyntaxError(f'Trying to apply math operation to type {returned.get_type_string()}! '
                                  f'Position {binary_expr.position}')
        elif binary_expr.binary_enum in [BinaryEnum.OR, BinaryEnum.AND]:
            if returned.type_enum != TypeEnum.BOOLEAN:
                raise SyntaxError(f'Trying to apply logical operation to type {returned.get_type_string()}! '
                                  f'Position {binary_expr.position}')
            binary_expr.right.accept(self)
            returned = self.type_stack_visitor.pop_type_from_stack()
            if returned.type_enum != TypeEnum.BOOLEAN:
                raise SyntaxError(f'Trying to apply logical operation to type {returned.get_type_string()}! '
                                  f'Position {binary_expr.position}')
        self.type_stack_visitor.visit(binary_expr)

    def visit_random_access_expr(self, ra_expr: RandomAccessExpr):
        ra_expr.object.accept(self)
        returned = self.type_stack_visitor.pop_type_from_stack()
        if returned.type_enum != TypeEnum.INT_ARRAY:
            raise SyntaxError(f'Trying to use type {returned.get_type_string()} as int array! '
                              f'Position {ra_expr.position}')
        ra_expr.position_in_arr.accept(self)
        returned = self.type_stack_visitor.pop_type_from_stack()
        if returned.type_enum != TypeEnum.INT:
            raise SyntaxError(f'Trying to use type {returned.get_type_string()} as index of int array! '
                              f'Position {ra_expr.position}')
        self.type_stack_visitor.visit(ra_expr)

    def visit_length_expr(self, length_expr: LengthExpr):
        length_expr.obj.accept(self)
        returned = self.type_stack_visitor.pop_type_from_stack()
        if returned.type_enum != TypeEnum.INT_ARRAY:
            raise SyntaxError(f'Trying to use type {returned.get_type_string()} as int array! '
                              f'Position {length_expr.position}')
        self.type_stack_visitor.visit(length_expr)

    def visit_call_method_expr(self, call_method_expr: CallMethodExpr):
        call_method_expr.expr.accept(self)
        returned_base: TypeInfo = self.type_stack_visitor.get_type_from_stack()
        if returned_base.type_enum != TypeEnum.USER_CLASS:
            raise SyntaxError(f'Trying to use type {returned_base.get_type_string()} as user type! '
                              f'Position {call_method_expr.position}')

        class_info: ClassInfo = self.table.get_class(returned_base.user_class_name, call_method_expr.position)
        method_info: MethodInfo = class_info.methods_block.get(call_method_expr.id.name)
        if method_info is None:
            raise SyntaxError(f'Requested method {call_method_expr.id.name} is not presented in '
                              f'class {class_info.name}! Position {call_method_expr.position}')

        scoped_class: ClassInfo = self.table.get_scoped_class()
        if method_info.access_modifier == AccessModifierEnum.Private and \
                (scoped_class is None or scoped_class.name != class_info.name):
            raise SyntaxError(f'Requested method {class_info.name}::{call_method_expr.id.name} has private access '
                              f'modifier! Position {call_method_expr.position}')
        for arg in call_method_expr.expr_list:
            arg.accept(self)
        if len(call_method_expr.expr_list) != method_info.get_args_count():
            raise SyntaxError(f'Requested method {class_info.name}::{call_method_expr.id.name} was called with '
                              f'invalid arguments number - expected {method_info.get_args_count()} arguments, got '
                              f'{len(call_method_expr.expr_list)} arguments! Position {call_method_expr.position}')
        for arg in reversed(method_info.args_block):
            passed: TypeInfo = self.type_stack_visitor.pop_type_from_stack()
            if passed != arg.type_of:
                if passed.type_enum == TypeEnum.USER_CLASS and \
                        self.table.does_type_have_super(
                            self.table.get_class(passed.user_class_name, call_method_expr.position),
                            arg.type_of.user_class_name, call_method_expr.position):
                    continue
                raise SyntaxError(f'Requested method {class_info.name}::{call_method_expr.id.name} was called with '
                                  f'invalid argument - expected {arg.type_of.get_type_string()}, but got '
                                  f'{passed.get_type_string()}! Position {call_method_expr.position}')
        self.type_stack_visitor.visit(call_method_expr)

    def visit_value_expr(self, value_expr: ValueExpr):
        self.type_stack_visitor.visit(value_expr)

    def visit_id(self, id: Id):
        self.type_stack_visitor.visit(id)

    def visit_this_expr(self, this_expr: ThisExpr):
        self.type_stack_visitor.visit(this_expr)

    def visit_new_object_expr(self, new_obj_expr: NewObjectExpr):
        self.type_stack_visitor.visit(new_obj_expr)

    def visit_new_int_arr_expr(self, new_int_arr_expr: NewIntArrExpr):
        new_int_arr_expr.size.accept(self)
        returned: TypeInfo = self.type_stack_visitor.pop_type_from_stack()
        if returned != IntType:
            raise SyntaxError(f'Trying to use type {returned.get_type_string()} as size of array! '
                              f'Position {new_int_arr_expr.position}')
        self.type_stack_visitor.visit(new_int_arr_expr)

    def visit_not_expr(self, not_expr: NotExpr):
        not_expr.right.accept(self)
        returned: TypeInfo = self.type_stack_visitor.pop_type_from_stack()
        if returned != BooleanType:
            raise SyntaxError(f'Trying to use type {returned.get_type_string} as boolean expression! '
                              f'Position {not_expr.position}')
        self.type_stack_visitor.visit(not_expr)

    def visit_return_statement(self, obj: ReturnStatement):
        obj.expression.accept(self)
