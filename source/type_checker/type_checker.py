import symbol_table as st
import syntax_tree as ast

# создадим несколько сокращений для проверки типов #
IntType = st.TypeInfo(st.TypeEnum.Int, None)
BooleanType = st.TypeInfo(st.TypeEnum.Boolean, None)
IntArrayType = st.TypeInfo(st.TypeEnum.IntArray, None)


class TypeChecker(ast.Visitor):
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
    """

    def __init__(self):
        """
        Конструктор
        """
        ast.Visitor.__init__(self)
        self.table = None
        self.types_stack = []

    def check_ast_st(self, program: ast.Program, symbol_table: st.Table):
        """
        Отвечает за проверку дерева на соответствие типов
        :param program: корень абстрактного синтаксического дерева
        :param symbol_table: символьная таблица для дерева
        :return:
        """
        self.table = symbol_table
        try:
            program.accept(self)
        except SyntaxError as error:
            print(error)
        else:
            print('Проверка типов пройдена успешно!')

    def visit(self, visitable: ast.Visitable):
        """
        Отвечает за посещение узлов дерева
        :param visitable: посещаемый узел AST
        :return:
        """
        if isinstance(visitable, ast.Program):
            self.visit_program(visitable)
        if isinstance(visitable, ast.MainClass):
            self.visit_main_class(visitable)
        if isinstance(visitable, ast.ClassDecl):
            self.visit_class_decl(visitable)
        if isinstance(visitable, ast.VarDecl):
            self.visit_var_decl(visitable)
        if isinstance(visitable, ast.ArgDecl):
            self.visit_arg_decl(visitable)
        if isinstance(visitable, ast.MethodDecl):
            self.visit_method_decl(visitable)
        if isinstance(visitable, ast.RandomAccessAssignStatement):
            self.visit_random_access_assign_statement(visitable)
        if isinstance(visitable, ast.AssignStatement):
            self.visit_assign_statement(visitable)
        if isinstance(visitable, ast.PrintLineStatement):
            self.visit_print_line_statement(visitable)
        if isinstance(visitable, ast.WhileStatement):
            self.visit_while_statement(visitable)
        if isinstance(visitable, ast.Statements):
            self.visit_statements(visitable)
        if isinstance(visitable, ast.IfStatement):
            self.visit_if_statement(visitable)
        if isinstance(visitable, ast.BinaryExpr):
            self.visit_binary_expr(visitable)
        if isinstance(visitable, ast.RandomAccessExpr):
            self.visit_random_access_expr(visitable)
        if isinstance(visitable, ast.LengthExpr):
            self.visit_length_expr(visitable)
        if isinstance(visitable, ast.CallMethodExpr):
            self.visit_call_method_expr(visitable)
        if isinstance(visitable, ast.IntegerExpr):
            self.visit_integer_expr(visitable)
        if isinstance(visitable, ast.TrueExpr):
            self.visit_true_expr(visitable)
        if isinstance(visitable, ast.FalseExpr):
            self.visit_false_expr(visitable)
        if isinstance(visitable, ast.BooleanExpr):
            self.visit_boolean_expr(visitable)
        if isinstance(visitable, ast.Id):
            self.visit_id(visitable)
        if isinstance(visitable, ast.ThisExpr):
            self.visit_this_expr(visitable)
        if isinstance(visitable, ast.NewObjectExpr):
            self.visit_new_object_expr(visitable)
        if isinstance(visitable, ast.NewIntArrExpr):
            self.visit_new_int_arr_expr(visitable)
        if isinstance(visitable, ast.NotExpr):
            self.visit_not_expr(visitable)

    def visit_program(self, program: ast.Program):
        program.main.accept(self)
        for cls in program.class_decl_list:
            cls.accept(self)

    def visit_main_class(self, main_class: ast.MainClass):
        for statement in main_class.statement_list:
            statement.accept(self)

    def visit_class_decl(self, class_decl: ast.ClassDecl):
        self.table.add_class_to_scope(class_decl.id.name, class_decl.position)
        for method in class_decl.method_decl_list:
            method.accept(self)
        self.table.free_last_scope()

    def visit_var_decl(self, var_decl: ast.VarDecl):
        if var_decl.type_of.label != 'int' and \
                var_decl.type_of.label != 'int_array' and \
                var_decl.type_of.label != 'boolean':
            self.table.get_class(var_decl.type_of.label, var_decl.position)

    def visit_arg_decl(self, arg_decl: ast.ArgDecl):
        if arg_decl.type_of.label != 'int' and \
                arg_decl.type_of.label != 'int_array' and \
                arg_decl.type_of.label != 'boolean':
            self.table.get_class(arg_decl.type_of.label, arg_decl.position)

    def visit_method_decl(self, method_decl: ast.MethodDecl):
        self.table.add_method_to_scope(method_decl.id.name, method_decl.position)
        for arg_decl in method_decl.arg_decl_list:
            arg_decl.accept(self)
        for var_decl in method_decl.var_decl_list:
            var_decl.accept(self)
        for statement in method_decl.statement_list:
            statement.accept(self)
        if method_decl.type_of.label != 'int' and \
                method_decl.type_of.label != 'int_array' and \
                method_decl.type_of.label != 'boolean':  # TODO Переписать наконец эту хрень
            self.table.get_class(method_decl.type_of.label, method_decl.position)
        self.table.free_last_scope()

    def visit_random_access_assign_statement(self, raa_statement: ast.RandomAccessAssignStatement):
        var_info: st.VariableInfo = self.table.get_variable(raa_statement.id.name, raa_statement.position)
        if var_info.type_of.type_enum != st.TypeEnum.IntArray:
            raise SyntaxError(f'Trying to subscript {var_info.type_of.get_type_string()} as array! '
                              f'Position {raa_statement.position}')  # TODO Переписать на другой ошибке!
        raa_statement.position_in_arr.accept(self)
        returned: st.TypeInfo = self.pop_types_stack()
        if returned.type_enum != st.TypeEnum.Int:
            raise SyntaxError(f'Trying to use type {returned.get_type_string()} as index of array! '
                              f'Position {raa_statement.position}')
        raa_statement.expr.accept(self)
        returned: st.TypeInfo = self.pop_types_stack()
        if returned.type_enum != st.TypeEnum.Int:
            raise SyntaxError(f'Trying to assign type {returned.get_type_string()} to element of int array! '
                              f'Position {raa_statement.position}')

    def visit_assign_statement(self, assign_statement: ast.AssignStatement):
        var_info: st.VariableInfo = self.table.get_variable(assign_statement.left.name, assign_statement.position)
        assign_statement.right.accept(self)
        returned = self.pop_types_stack()
        if var_info.type_of != returned:
            raise SyntaxError(f'Trying to assign value of type {returned.get_type_string()} to variable '
                              f'of type {var_info.type_of.get_type_string()}! Position {assign_statement.position}')

    def visit_print_line_statement(self, print_line_statement: ast.PrintLineStatement):
        print_line_statement.obj.accept(self)
        returned: st.TypeInfo = self.pop_types_stack()
        if returned.type_enum == st.TypeEnum.UserClass:
            raise SyntaxError(f'Trying to return user type {returned.get_type_string()}! '
                              f'Position {print_line_statement.position}')

    def visit_while_statement(self, while_statement: ast.WhileStatement):
        while_statement.condition.accept(self)
        returned = self.pop_types_stack()
        if returned.type_enum != st.TypeEnum.Boolean:
            raise SyntaxError(f'Trying to use type {returned.get_type_string()} as condition! '
                              f'Position {while_statement.position}')

    def visit_statements(self, statements: ast.Statements):
        for statement in statements.statement_list:
            statement.accept(self)

    def visit_if_statement(self, if_statement: ast.IfStatement):
        if_statement.condition.accept(self)
        returned = self.pop_types_stack()
        if returned.type_enum != st.TypeEnum.Boolean:
            raise SyntaxError(f'Trying to use type {returned.get_type_string()} as condition! '
                              f'Position {if_statement.position}')
        if_statement.if_false.accept(self)
        if_statement.if_true.accept(self)

    def visit_binary_expr(self, binary_expr: ast.BinaryExpr):
        binary_expr.left.accept(self)
        returned = self.pop_types_stack()
        if binary_expr.label in ['+', '-', '*', '%', '<']:  # TODO переписать это (enum?)
            if returned.type_enum != st.TypeEnum.Int:
                raise SyntaxError(f'Trying to apply math operation to type {returned.get_type_string()}! '
                                  f'Position {binary_expr.position}')
            binary_expr.right.accept(self)
            returned = self.pop_types_stack()
            if returned.type_enum != st.TypeEnum.Int:
                raise SyntaxError(f'Trying to apply math operation to type {returned.get_type_string()}! '
                                  f'Position {binary_expr.position}')
            if binary_expr.label == '<':
                self.types_stack.append(BooleanType)
            else:
                self.types_stack.append(IntType)
        elif binary_expr.label in ['and', 'or']:
            if returned.type_enum != st.TypeEnum.Boolean:
                raise SyntaxError(f'Trying to apply logical operation to type {returned.get_type_string()}! '
                                  f'Position {binary_expr.position}')
            binary_expr.right.accept(self)
            returned = self.pop_types_stack()
            if returned.type_enum != st.TypeEnum.Boolean:
                raise SyntaxError(f'Trying to apply logical operation to type {returned.get_type_string()}! '
                                  f'Position {binary_expr.position}')
            self.types_stack.append(BooleanType)

    def visit_random_access_expr(self, ra_expr: ast.RandomAccessExpr):
        ra_expr.object.accept(self)
        returned = self.pop_types_stack()
        if returned.type_enum != st.TypeEnum.IntArray:
            raise SyntaxError(f'Trying to use type {returned.get_type_string()} as int array! '
                              f'Position {ra_expr.position}')
        ra_expr.position.accept(self)
        returned = self.pop_types_stack()
        if returned.type_enum != st.TypeEnum.Int:
            raise SyntaxError(f'Trying to use type {returned.get_type_string()} as index of int array! '
                              f'Position {ra_expr.position}')
        self.types_stack.append(IntType)

    def visit_length_expr(self, length_expr: ast.LengthExpr):
        length_expr.obj.accept(self)
        returned = self.pop_types_stack()
        if returned.type_enum != st.TypeEnum.IntArray:
            raise SyntaxError(f'Trying to use type {returned.get_type_string()} as int array! '
                              f'Position {length_expr.position}')

    def visit_call_method_expr(self, call_method_expr: ast.CallMethodExpr):
        call_method_expr.expr.accept(self)
        returned_base: st.TypeInfo = self.pop_types_stack()
        if returned_base.type_enum != st.TypeEnum.UserClass:
            raise SyntaxError(f'Trying to use type {returned_base.get_type_string()} as user type! '
                              f'Position {call_method_expr.position}')

        class_info: st.ClassInfo = self.table.get_class(returned_base.user_class_name, call_method_expr.position)
        method_info: st.MethodInfo = class_info.methods_block.get(call_method_expr.id.name)
        if method_info is None:
            raise SyntaxError(f'Requested method {call_method_expr.id.name} is not presented in '
                              f'class {class_info.name}! Position {call_method_expr.position}')

        scoped_class: st.ClassInfo = self.table.get_scoped_class()
        if method_info.access_modifier == st.AccessModifierEnum.Private and \
                (scoped_class is None or scoped_class.name != class_info.name):
            raise SyntaxError(f'Requested method {class_info.name}::{call_method_expr.id.name} has private access '
                              f'modifier! Position {call_method_expr.position}')
        for arg in call_method_expr.expr_list:
            arg.accept(self)
        if len(call_method_expr.expr_list) != method_info.get_args_count():
            raise SyntaxError(f'Requested method {class_info.name}::{call_method_expr.id.name} was called with '
                              f'invalid arguments number - expected {method_info.get_args_count()} arguments, got '
                              f'{len(call_method_expr.expr_list)} arguments! Position {call_method_expr.position}')
        for arg in method_info.args_block:
            passed: st.TypeInfo = self.pop_types_stack()
            if passed != arg.type_of:
                if passed.type_enum == st.TypeEnum.UserClass and \
                        self.table.does_type_have_super(
                            self.table.get_class(passed.user_class_name, call_method_expr.position),
                            arg.type_of.user_class_name):
                    continue
                raise SyntaxError(f'Requested method {class_info.name}::{call_method_expr.id.name} was called with '
                                  f'invalid argument - expected {arg.type_of.get_type_string()}, but got '
                                  f'{passed.get_type_string()}! Position {call_method_expr.position}')
        self.types_stack.append(method_info.return_type)

    def visit_integer_expr(self, integer_expr: ast.IntegerExpr):
        _ = integer_expr
        self.types_stack.append(IntType)

    def visit_true_expr(self, true_expr: ast.TrueExpr):
        _ = true_expr
        self.types_stack.append(BooleanType)

    def visit_false_expr(self, false_expr: ast.FalseExpr):
        _ = false_expr
        self.types_stack.append(BooleanType)

    def visit_boolean_expr(self, boolean_expr: ast.BooleanExpr):
        _ = boolean_expr
        self.types_stack.append(BooleanType)

    def visit_id(self, id: ast.Id):
        variable: st.VariableInfo = self.table.get_variable(id.name, id.position)
        self.types_stack.append(variable.type_of)

    def visit_this_expr(self, this_expr: ast.ThisExpr):
        _ = this_expr
        scoped_class = self.table.get_scoped_class()
        self.types_stack.append(scoped_class.type_info)

    def visit_new_object_expr(self, new_obj_expr: ast.NewObjectExpr):
        object_type: st.ClassInfo = self.table.get_class(new_obj_expr.id.name, new_obj_expr.position)
        self.types_stack.append(object_type.type_info)

    def visit_new_int_arr_expr(self, new_int_arr_expr: ast.NewIntArrExpr):
        new_int_arr_expr.size.accept(self)
        returned: st.TypeInfo = self.pop_types_stack()
        if returned != IntType:
            raise SyntaxError(f'Trying to use type {returned.get_type_string()} as size of array! '
                              f'Position {new_int_arr_expr.position}')

    def visit_not_expr(self, not_expr: ast.NotExpr):
        not_expr.right.accept(self)
        returned: st.TypeInfo = self.pop_types_stack()
        if returned != BooleanType:
            raise SyntaxError(f'Trying to use type {returned.get_type_string} as boolean expression! '
                              f'Position {not_expr.position}')
        self.types_stack.append(BooleanType)

    def pop_types_stack(self):
        result = self.types_stack[-1]
        self.types_stack.pop(len(self.types_stack) - 1)
        return result
