import syntax_tree as ast
import symbol_table as st

# создадим несколько сокращений для проверки типов #
IntType = st.TypeInfo(st.TypeEnum.Int, None)
BooleanType = st.TypeInfo(st.TypeEnum.Boolean, None)
IntArrayType = st.TypeInfo(st.TypeEnum.IntArray, None)


class TypeChecker(ast.Visitor):
    """
    Проверка типов (конечно, далеко не все проверки, только необходимый минимум)
    Передаем таблицу и само дерево снаружи, тайпчекер не занимается построением,
    только обработкой (чтобы в случае вывода всего-всего не делать лишней работы)
    """

    def __init__(self):
        """

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
        if isinstance(visitable, ast.StatementList):
            self.visit_statement_list(visitable)
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
        pass

    def visit_main_class(self, main_class: ast.MainClass):
        pass

    def visit_class_decl(self, class_decl: ast.ClassDecl):
        pass

    def visit_var_decl(self, var_decl: ast.VarDecl):
        pass

    def visit_arg_decl(self, arg_decl: ast.ArgDecl):
        pass

    def visit_method_decl(self, method_decl: ast.MethodDecl):
        pass

    def visit_random_access_assign_statement(self, raa_statement: ast.RandomAccessAssignStatement):
        pass

    def visit_assign_statement(self, assign_statement: ast.AssignStatement):
        pass

    def visit_print_line_statement(self, print_line_statement: ast.PrintLineStatement):
        pass

    def visit_while_statement(self, while_statement: ast.WhileStatement):
        pass

    def visit_statements(self, statements: ast.Statements):
        pass

    def visit_statement_list(self, statement_list: ast.StatementList):
        pass

    def visit_if_statement(self, if_statement: ast.IfStatement):
        pass

    def visit_binary_expr(self, binary_expr: ast.BinaryExpr):
        pass

    def visit_random_access_expr(self, ra_expr: ast.RandomAccessExpr):
        pass

    def visit_length_expr(self, length_expr: ast.LengthExpr):
        pass

    def visit_call_method_expr(self, call_method_expr: ast.CallMethodExpr):
        call_method_expr.expr.accept(self)
        returned_base: st.TypeInfo = self.pop_types_stack()
        if returned_base.type_enum != st.TypeEnum.UserClass:
            raise SyntaxError(f'Trying to use type {returned_base.get_type_string()} as user type! '
                              f'Position {call_method_expr.place}')

        class_info: st.ClassInfo = self.table.get_class(returned_base.user_class_name, call_method_expr.place)
        method_info = class_info.methods_block.get(call_method_expr.id.name)
        if method_info is None:
            raise SyntaxError(f'Requested method {call_method_expr.id.name} is not presented in '
                              f'class {class_info.name}! Position {call_method_expr.place}')



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
        variable: st.VariableInfo = self.table.get_variable(id.name, id.place)
        self.types_stack.append(variable.type_of)

    def visit_this_expr(self, this_expr: ast.ThisExpr):
        _ = this_expr
        scoped_class = self.table.get_scoped_class()
        self.types_stack.append(scoped_class.type_info)

    def visit_new_object_expr(self, new_obj_expr: ast.NewObjectExpr):
        object_type: st.ClassInfo = self.table.get_class(new_obj_expr.id.name, new_obj_expr.place)
        self.types_stack.append(object_type.type_info)

    def visit_new_int_arr_expr(self, new_int_arr_expr: ast.NewIntArrExpr):
        new_int_arr_expr.size.accept(self)
        returned: st.TypeInfo = self.pop_types_stack()
        if returned != IntType:
            raise SyntaxError(f'Trying to use type {returned.get_type_string()} as size of array! '
                              f'Position {new_int_arr_expr.place}')

    def visit_not_expr(self, not_expr: ast.NotExpr):
        not_expr.right.accept(self)
        returned: st.TypeInfo = self.pop_types_stack()
        if returned != BooleanType:
            raise SyntaxError(f'Trying to use type {returned.get_type_string} as boolean expression! '
                              f'Position {not_expr.place}')
        self.types_stack.append(BooleanType)

    def pop_types_stack(self):
        result = self.types_stack[-1]
        self.types_stack.pop(len(self.types_stack) - 1)
        return result
