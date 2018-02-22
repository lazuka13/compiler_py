from enum import Enum

from activation_records.i_frame import IFrame
from syntax_tree import Position
from .identifier import Identifier
from .type_info import TypeInfo
from .variable_info import VariableInfo


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

        self.vars_block = []  # список имен переменных
        self.args_block = []  # список имен аргументов

        self.vars_names = []
        self.args_names = []

        self.frame : IFrame = None

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
        self.vars_block.append(variable_info)
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
        Отвечает за добавление аргумента в метод
        :param arg: информация о добавляемом аргументе
        :return:
        """
        declared = self.variables_block.get(arg.name)
        if declared is not None:
            raise SyntaxError(f'Variable redeclaration, {declared.type_of.get_type_string()} {declared.name} already '
                              f'declared at {declared.position}! Position: {arg.position}')
        self.args_names.append(arg.name)
        self.args_block.append(arg)
        self.variables_block[arg.name] = arg

    def get_args_count(self):
        return len(self.args_names)

    def get_vars_count(self):
        return len(self.vars_names)

    def get_full_name(self):
        return self.class_name + '@' + self.name

    def add_frame_info(self, frame: IFrame):
        self.frame = frame

    def get_frame(self):
        return self.frame
