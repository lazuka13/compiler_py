from syntax_tree import Visitor, Program, Visitable, \
    MainClass, ClassDecl, Position
from .ClassInfo import ClassInfo
from .MethodInfo import MethodInfo, AccessModifierEnum
from .Table import Table
from .TypeInfo import TypeEnum, TypeInfo
from .VariableInfo import VariableInfo


class TableFiller(Visitor):
    """
    Visitor, отвечающий за заполнение символьной таблицы
    при обходе абстрактного синтаксического дерева
    """

    def __init__(self, table: Table):
        """
        Конструктор (передаем заполняемую таблицу)
        :param table: символьная таблица для заполнения
        """
        Visitor.__init__(self)
        self.table = table

    def parse_program(self, program: Program, print_table: bool = True):
        """
        Отвечает за обход AST и заполнение таблицы
        :param program: корень AST (class Program)
        :param print_table: отвечает за вывод таблицы на экран
        :return:
        """
        program.accept(self)
        if print_table:
            for class_name in self.table.classes_names:
                try:
                    class_info = self.table.get_class(class_name, Position(0, 0))
                    self.table.add_class_to_scope(class_name, Position(0, 0))
                    if print_table:
                        self._print_class_info(class_info)
                    self.table.free_last_scope()
                    print()
                except SyntaxError as error:
                    print(error)

    def visit(self, visitable: Visitable):
        """
        Отвечает за посещение произвольного узла дерева (начальный пункт)
        :param visitable: посещаемый узел
        :return:
        TODO переписать на декораторах?
        """
        if isinstance(visitable, Program):
            self._visit_program(visitable)
        elif isinstance(visitable, MainClass):
            self._visit_main_class(visitable)
        elif isinstance(visitable, ClassDecl):
            self._visit_class_decl(visitable)

    def _visit_program(self, program: Program):
        """
        Отвечает за посещение узла класса Program
        :param program: узел дерева класса Program
        :return:
        """
        program.main.accept(self)
        for class_decl in program.class_decl_list:
            class_decl.accept(self)

    def _visit_main_class(self, main_class: MainClass):
        """
        Отвечает за посещение главного класса программы
        :param main_class: узел дерева класса MainClass
        :return:
        """
        class_info = ClassInfo(main_class.id.name, main_class.position)
        method_info = MethodInfo('main',
                                 main_class.id.name,
                                 main_class.position,
                                 TypeInfo(TypeEnum.UserClass, 'void'),
                                 AccessModifierEnum.Public)
        method_info.add_arg_info(VariableInfo(
            main_class.param_id.name,
            main_class.position,
            TypeInfo(TypeEnum.UserClass, 'String []')
        ))
        class_info.add_method_info(method_info)
        self.table.add_class(class_info)

    def _visit_class_decl(self, class_decl: ClassDecl):
        """
        Отвечает за посещение не главного класса программы
        :param class_decl: узел AST класса ClassDecl
        :return:
        """
        class_info = ClassInfo(class_decl.id.name, class_decl.position)
        if class_decl.extends is not None:
            class_info.add_super_class(class_decl.extends.name)

        for var_decl in class_decl.var_decl_list:
            class_info.add_variable_info(
                VariableInfo(
                    var_decl.id.name,
                    var_decl.position,
                    TypeInfo.from_type(var_decl.type_of)
                )
            )

        for method_decl in class_decl.method_decl_list:
            method_info = MethodInfo(
                method_decl.id.name,
                class_decl.id.name,
                method_decl.position,
                TypeInfo.from_type(method_decl.type_of),
                AccessModifierEnum.Public if method_decl.access_modifier == 'public' else AccessModifierEnum.Private
            )
            for arg_decl in method_decl.arg_decl_list:
                method_info.add_arg_info(VariableInfo(
                    arg_decl.id.name,
                    arg_decl.position,
                    TypeInfo.from_type(arg_decl.type_of)
                ))
            for var_decl in method_decl.var_decl_list:
                method_info.add_variable_info(VariableInfo(
                    var_decl.id.name,
                    var_decl.position,
                    TypeInfo.from_type(var_decl.type_of)
                ))
            class_info.add_method_info(method_info)
        self.table.add_class(class_info)

    def _print_class_info(self, class_info: ClassInfo):
        """
        Отвечает за вывод информации о классе на экран
        :param class_info: информация о классе, который будет выведен
        :return:
        """
        print(f'class {class_info.name} {class_info.position}')

        if class_info.super_class_name is not None:
            print(f'extends {class_info.super_class_name}')
            self.table.get_class(class_info.super_class_name, Position(0, 0))

        for var_name in class_info.vars_names:
            variable_info = self.table.get_variable(var_name, Position(0, 0))
            print(self._format_variable_info(variable_info))

        for method_name in class_info.methods_names:
            method_info = self.table.get_method(method_name, Position(0, 0))
            self.table.add_method_to_scope(method_info.name, Position(0, 0))
            access_modifier = 'public' if method_info.access_modifier == AccessModifierEnum.Public else 'private'

            print(f'    func {access_modifier} {method_info.name} {method_info.position}')

            if method_info.get_args_count() > 0:
                print(f'        arguments:')
                for arg_name in method_info.args_names:
                    arg_info = self.table.get_variable(arg_name, Position(0, 0))
                    print(f'            {self._format_variable_info(arg_info)}')

            if method_info.get_vars_count() > 0:
                print(f'        local variables:')
                for var_name in method_info.vars_names:
                    variable_info = self.table.get_variable(var_name, Position(0, 0))
                    print(f'            {self._format_variable_info(variable_info)}')

            self.table.free_last_scope()

    @staticmethod
    def _format_variable_info(variable_info: VariableInfo):
        """
        Отвечает за формирование текста для отображения переменной
        :param variable_info: информация об отображаемой переменной
        :return:
        """
        if variable_info.type_of.type_enum == TypeEnum.Boolean:
            type_of = 'bool'
        if variable_info.type_of.type_enum == TypeEnum.Int:
            type_of = 'int'
        if variable_info.type_of.type_enum == TypeEnum.IntArray:
            type_of = 'int []'
        if variable_info.type_of.type_enum == TypeEnum.UserClass:
            type_of = variable_info.type_of.user_class_name
        return f'{type_of} {variable_info.name} {variable_info.position}'
