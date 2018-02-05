from source.syntax_tree import *

from enum import Enum
from typing import Optional


class Position:
    """

    """

    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __str__(self):
        """

        :return:
        """
        return f'({self.y}, {self.x})'

    @classmethod
    def from_place(cls, place):
        """

        :param place:
        :return:
        """
        obj = cls(place[0], place[1])
        return obj


class Identifier:
    """
    Базовый класс для всех классов-идентификаторов (переменные, методы, классы)
    """

    def __init__(self, name, position):
        """
        Конструктор
        :param name: название идентификатора (имя класса / переменной / метода)
        :param position: положение идентификатора
        """
        self.name = name
        self.position = position

    def __str__(self) -> str:
        """
        Отвечает за строковое представление идентификатора
        :return: str
        """
        return self.name


class TypeEnum(Enum):
    """
    Перечисление существующих типов (UserClass для пользовательского класса)
    """
    Int = 1
    IntArray = 2
    Boolean = 3
    UserClass = 4


class TypeInfo:
    """
    Хранит информацию о типе, его название, в случае пользовательского класса
    """

    def __init__(self, type_enum: TypeEnum, user_class_name: Optional[str]):
        """
        Конструктор
        :param type_enum: Один из возможных вариантов типов
        :param user_class_name: Название пользовательского класса в случае (UserClass)
        """
        self.type_enum = type_enum
        if self.type_enum == TypeEnum.UserClass:
            self.user_class_name = user_class_name
        else:
            self.user_class_name = None

    def get_type_string(self):
        """
        Отвечает за получение "человеческого" представления типа
        :return:
        """
        if self.type_enum == TypeEnum.Int:
            return 'int'
        if self.type_enum == TypeEnum.IntArray:
            return 'int []'
        if self.type_enum == TypeEnum.Boolean:
            return 'boolean'
        if self.type_enum == TypeEnum.UserClass:
            return self.user_class_name
        raise KeyError()

    @classmethod
    def from_type(cls, type_of: Type):
        """
        Отвечает за конвертацию из AST Type в ST TypeInfo
        :param type_of:
        :return:
        """
        if isinstance(type_of, ClassType):
            obj = cls(TypeEnum.UserClass, type_of.label)
        elif type_of.label == 'int_array':
            obj = cls(TypeEnum.IntArray, 'int []')
        elif type_of.label == 'int':
            obj = cls(TypeEnum.Int, 'int')
        elif type_of.label == 'boolean':
            obj = cls(TypeEnum.Boolean, 'bool')
        else:
            raise Exception
        return obj

    def __eq__(self, other):
        """
        Отвечает за сравнение типов (не по ссылке, а по значению)
        :param other:
        :return:
        """
        if self.type_enum == other.type_enum and self.type_enum != TypeEnum.UserClass:
            return True
        if self.type_enum and other.type_enum and self.user_class_name == other.user_class_name:
            return True
        return False


class VariableInfo(Identifier):
    """
    Информация о переменной - ее название, положение и тип
    """

    def __init__(self, name: str, position: Position, type_of: TypeInfo):
        """
        Конструктор
        :param name: Название переменной
        :param position: Положение переменной
        :param type_of: Тип переменной
        """
        Identifier.__init__(self, name, position)
        self.type_of = type_of


class AccessModifierEnum(Enum):
    """
    Перечисление существующих модификаторов доступа (public и private)
    """
    Public = 1
    Private = 0


class MethodInfo(Identifier):
    """
    Информация о методе (название, название класса, положение, тип
    возвращаемого значения, модификатор доступа к методу)
    """

    def __init__(self, name: str, class_name: str, position, return_type: TypeInfo,
                 access_modifier: AccessModifierEnum):
        """
        Конструктор
        :param name: название метода
        :param class_name: название класса, содержащего метод
        :param position: расположение метода
        :param return_type: тип возвращаемого значения
        :param access_modifier: модификатор доступа к методу
        """
        Identifier.__init__(self, name, position)
        self.class_name = class_name
        self.return_type = return_type
        self.access_modifier = access_modifier

        self.vars_names = []  # список имен переменных
        self.args_names = []  # список имен аргументов

        self.variables_block = dict()  # храним переменные метода в словаре с доступом по названию

    def add_variable_info(self, variable_info: VariableInfo):
        """
        Отвечает за добавление переменной в метод
        :param variable_info: информация о добавляемой переменной
        :return:
        """
        declared = self.variables_block.get(variable_info.name)
        if declared is not None:
            raise SyntaxError(f'Variable redeclaration, {declared.type_of.get_type_string()} {declared.name} already '
                              f'declared at {declared.position}! Position: {variable_info.position}')
        self.vars_names.append(variable_info.name)
        self.variables_block[variable_info.name] = variable_info

    def get_variable_info(self, variable_name: str, position: Position):
        """
        Отвечает за получение информации о переменной по ее имени
        :param variable_name: Имя запрашиваемой переменной
        :param position: Расположение запроса информации о переменной
        :return:
        """
        variable = self.variables_block.get(variable_name)
        if variable is None:
            raise SyntaxError(f'Variable {variable_name} in class {self.class_name} undeclared! Position: {position}')

    def add_arg_info(self, arg):
        """

        :param arg:
        :return:
        """
        declared = self.variables_block.get(arg.name)
        if declared is not None:
            raise SyntaxError(f'Variable redeclaration, {declared.type_of.get_type_string()} {declared.name} already '
                              f'declared at {declared.position}! Position: {arg.position}')
        self.args_names.append(arg.name)
        self.variables_block[arg.name] = arg

    def get_args_count(self):
        return len(self.args_names)

    def get_vars_count(self):
        return len(self.vars_names)

    def get_full_name(self):
        """

        :return:
        """
        return self.class_name


class ClassInfo(Identifier):
    """

    """

    def __init__(self, name: str, position: Position):
        """
        Конструктор
        :param name:
        :param position:
        """
        Identifier.__init__(self, name, position)

        self.super_class: str = None
        self.methods_names: list = []
        self.vars_names: list = []

        self.variables_block = dict()
        self.methods_block = dict()

        self.info: TypeInfo = TypeInfo(TypeEnum.UserClass, name)

    def add_method_info(self, method: MethodInfo):
        """

        :param method:
        :return:
        """
        declared: MethodInfo = self.methods_block.get(method.name)
        if declared is not None:
            raise SyntaxError(f'Method redeclaration, {declared.return_type.get_type_string()} {declared.name} already '
                              f'declared at {declared.position}! Position: {method.position}')
        self.methods_names.append(method.name)
        self.methods_block[method.name] = method

    def add_variable_info(self, variable: VariableInfo):
        """

        :param variable:
        :return:
        """
        declared = self.variables_block.get(variable.name)
        if declared is not None:
            raise SyntaxError(f'Variable redeclaration, {declared.type_of.get_type_string()} {declared.name} already '
                              f'declared at {declared.position}! Position: {variable.position}')
        self.vars_names.append(variable.name)
        self.variables_block.update((variable.name, variable))

    def add_super_class(self, symbol: str):
        self.super_class = symbol

    def get_vars_count(self):
        return len(self.vars_names)

    def get_methods_count(self):
        return len(self.methods_names)


class ScopeBlock:
    """

    """

    def __init__(self,
                 variables_block: Optional[dict],
                 methods_block: Optional[dict],
                 class_info: ClassInfo):
        self.variables_block = variables_block
        self.methods_block = methods_block
        self.class_info = class_info


class Table:
    def __init__(self):
        """

        """
        self.classes_block = dict()
        self.classes_names = []

        self.verified_classes = set()
        self.blocks = []
        self.frames = dict()

    def add_class(self, class_info: ClassInfo):
        """

        :param class_info:
        :param position:
        :return:
        """
        already_found = self.classes_block.get(class_info.name)
        if already_found is not None:
            raise SyntaxError('Class already defined')
        self.classes_names.append(class_info.name)
        self.classes_block[class_info.name] = class_info

    def _add_class_to_scope(self, class_info: ClassInfo):
        """

        :param class_info:
        :return:
        """
        self.blocks.append(ScopeBlock(class_info.variables_block, class_info.methods_block, class_info))

    def _add_method_to_scope(self, method_info: MethodInfo):
        """

        :param method_info:
        :return:
        """
        self.blocks.append(ScopeBlock(method_info.variables_block, None, self.blocks[-1].class_info))

    def add_class_to_scope(self, class_name: str, position: Position):
        """

        :param class_name:
        :param position:
        :return:
        """
        class_to_add = self.get_class(class_name, position)
        if class_to_add.name not in self.verified_classes:
            self.verify_class(class_to_add, position)
        classes_stack = [class_to_add]
        while class_to_add.super_class is not None:
            class_to_add = self.get_class(class_to_add.super_class, position)
            classes_stack.append(class_to_add)
        for class_info in classes_stack:
            self._add_class_to_scope(class_info)

    def add_method_to_scope(self, method_name: str, position: Position):
        """

        :param method_name:
        :param position:
        :return:
        """
        self._add_method_to_scope(self.get_method(method_name, position))

    def verify_class(self, class_info: ClassInfo, position: Position):
        """

        :param class_info:
        :param position:
        :return:
        """
        classes_in_graph = set()
        class_to_check = class_info
        while class_to_check.super_class is not None:
            class_to_check = self.get_class(class_to_check.super_class, position)
            if class_to_check in classes_in_graph:
                raise SyntaxError('Cyclic dependency!')
            classes_in_graph.add(class_info)
        for class_info in classes_in_graph:
            self.verified_classes.add(class_info)

    def get_class(self, class_name: str, position: Position) -> ClassInfo:
        """

        :param class_name:
        :param position:
        :return:
        """
        class_info = self.classes_block.get(class_name)
        if class_info is not None:
            return class_info
        raise SyntaxError(f'Not declared class {class_name} requested! Position {position}')

    def get_method(self, method_name: str, position: Position) -> MethodInfo:
        """

        :param method_name:
        :param position:
        :return:
        """
        for block in self.blocks:
            methods_block = block.methods_block
            result = methods_block.get(method_name)
            if result is not None:
                return result
        raise SyntaxError(f'Not declared method {method_name} requested! Position {position}')

    def get_variable(self, variable_name: str, position: Position) -> VariableInfo:
        """

        :param variable_name:
        :param position:
        :return:
        """
        for block in self.blocks:
            variables_block = block.variables_block
            result = variables_block.get(variable_name)
            if result is not None:
                return result
        raise SyntaxError(f'Not declared variable {variable_name} requested! Position {position}')

    def get_scoped_class(self) -> Optional[ClassInfo]:
        """

        :return:
        """
        if len(self.blocks) > 0 and self.blocks[0].class_info is not None:
            return self.blocks[0].class_info
        return None

    @staticmethod
    def does_type_have_super(class_info: ClassInfo, super_class_name: str) -> bool:
        """

        :param class_info:
        :param super_class_name:
        :param position:
        :return:
        """
        while class_info.super_class is not None:
            if class_info.super_class == super_class_name:
                return True
            class_info = class_info.super_class
        return False

    def free_last_scope(self):
        """

        :return:
        """
        self.blocks.clear()


class TableFiller(Visitor):
    """

    """

    def __init__(self, table):
        """

        :param table:
        """
        Visitor.__init__(self)
        self.table = table

    def parse_program(self, program: Program, print_table=True):
        """

        :param program:
        :param print_table:
        :return:
        """
        program.accept(self)
        if print_table:
            for class_name in self.table.classes_names:
                try:
                    class_info = self.table.get_class(class_name, Position(0, 0))
                    self.table.add_class_to_scope(class_name, Position(0, 0))
                    print(f'class {class_name}:')
                    self.print_class_info(class_info)
                    self.table.free_last_scope()
                    print()
                except SyntaxError as error:
                    print(error)

    def visit(self, visitable: Visitable):
        """

        :param visitable:
        :return:
        """
        if isinstance(visitable, Program):
            self.visit_program(visitable)
        elif isinstance(visitable, MainClass):
            self.visit_main_class(visitable)
        elif isinstance(visitable, ClassDecl):
            self.visit_class_decl(visitable)

    def visit_program(self, program: Program):
        """

        :param program:
        :return:
        """
        program.main.accept(self)
        for class_decl in program.class_decl_list:
            class_decl.accept(self)

    def visit_main_class(self, main_class: MainClass):
        """

        :param main_class:
        :return:
        """
        class_info = ClassInfo(main_class.id.name, Position.from_place(main_class.place))
        method_info = MethodInfo('main',
                                 main_class.id.name,
                                 Position.from_place(main_class.place),
                                 TypeInfo(TypeEnum.UserClass, 'void'),
                                 AccessModifierEnum.Public)
        method_info.add_arg_info(VariableInfo(
            main_class.param_id.name,
            Position.from_place(main_class.place),
            TypeInfo(TypeEnum.UserClass, 'String []')
        ))
        class_info.add_method_info(method_info)
        self.table.add_class(class_info)

    def visit_class_decl(self, class_decl: ClassDecl):
        """

        :param class_decl:
        :return:
        """
        class_info = ClassInfo(class_decl.id.name, Position.from_place(class_decl.place))
        if class_decl.extends is not None:
            class_info.add_super_class(class_decl.extends.name)

        for var_decl in class_decl.var_decl_list:
            class_info.add_variable_info(
                VariableInfo(
                    var_decl.id.name,
                    Position.from_place(var_decl.place),
                    TypeInfo.from_type(var_decl.type_of)
                )
            )

        for method_decl in class_decl.method_decl_list:
            method_info = MethodInfo(
                method_decl.id.name,
                class_decl.id.name,
                Position.from_place(method_decl.place),
                TypeInfo.from_type(method_decl.type_of),
                AccessModifierEnum.Public if method_decl.modifier == 'PUBLIC' else AccessModifierEnum.Private
            )
            for arg_decl in method_decl.arg_decl_list:
                method_info.add_arg_info(VariableInfo(
                    arg_decl.id.name,
                    Position.from_place(arg_decl.place),
                    TypeInfo.from_type(arg_decl.type_of)
                ))
            for var_decl in method_decl.var_decl_list:
                method_info.add_variable_info(VariableInfo(
                    var_decl.id.name,
                    Position.from_place(var_decl.place),
                    TypeInfo.from_type(var_decl.type_of)
                ))
            class_info.add_method_info(method_info)
        self.table.add_class(class_info)

    def print_class_info(self, class_info: ClassInfo):
        """

        :param class_info:
        :return:
        """
        if class_info.super_class is not None:
            print(f'    Super {class_info.super_class}')
            super_class_info = self.table.get_class(class_info.super_class, Position(0, 0))
            self.print_class_info(super_class_info)

        for var_name in class_info.vars_names:
            variable_info = self.table.get_variable(var_name, Position(0, 0))
            print(self.format_variable_info(variable_info))

        for method_name in class_info.methods_names:
            method_info = self.table.get_method(method_name, Position(0, 0))
            self.table.add_method_to_scope(method_info.name, Position(0, 0))
            access_modifier = 'public' if method_info.access_modifier == AccessModifierEnum.Public else 'private'

            print(f'    func {access_modifier} {method_info.name}')

            if method_info.get_args_count() > 0:
                print(f'        arguments:')
                for arg_name in method_info.args_names:
                    arg_info = self.table.get_variable(arg_name, Position(0, 0))
                    print(f'            {self.format_variable_info(arg_info)}')

            if method_info.get_vars_count() > 0:
                print(f'        local variables:')
                for var_name in method_info.vars_names:
                    variable_info = self.table.get_variable(var_name, Position(0, 0))
                    print(f'            {self.format_variable_info(variable_info)}')

            self.table.free_last_scope()

    @staticmethod
    def format_variable_info(variable_info: VariableInfo):
        """

        :param variable_info:
        :return:
        """
        if variable_info.type_of.type_enum == TypeEnum.Boolean:
            type_of = 'bool'
        if variable_info.type_of.type_enum == TypeEnum.Int:
            type_of = 'bool'
        if variable_info.type_of.type_enum == TypeEnum.IntArray:
            type_of = 'bool'
        if variable_info.type_of.type_enum == TypeEnum.UserClass:
            type_of = variable_info.type_of.user_class_name
        return f'{type_of} {variable_info.name}'
