from syntax_tree import Position
from x86.x86_class_struct import X86MiniJavaClassStruct
from .i_class_struct import IClassStruct
from .identifier import Identifier
from .method_info import MethodInfo
from .type_info import TypeEnum, TypeInfo
from .variable_info import VariableInfo


class ClassInfo(Identifier):
    """
    Информация о классе (название, положение, информация о методах и переменных)
    """

    def __init__(self, name: str, position: Position):
        """
        Конструктор
        :param name: название класса
        :param position: положение класса
        """
        Identifier.__init__(self, name, position)

        self.super_class_name: str = None
        self.methods_names: list = []
        self.vars_names: list = []

        self.variables_block = dict()
        self.methods_block = dict()

        self.class_struct: IClassStruct = X86MiniJavaClassStruct()
        self.type_info: TypeInfo = TypeInfo(TypeEnum.USER_CLASS, name)

    def add_method_info(self, method: MethodInfo):
        """
        Отвечает за добавление информации о методе в классе
        :param method: Информация о добавляемом методе
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
        Отвечает за добавление информации о переменной в классе
        :param variable: Информация о добавляемой переменной
        :return:
        """
        declared = self.variables_block.get(variable.name)
        if declared is not None:
            raise SyntaxError(f'Variable redeclaration, {declared.type_of.get_type_string()} {declared.name} already '
                              f'declared at {declared.position}! Position: {variable.position}')
        self.vars_names.append(variable.name)
        self.variables_block[variable.name] = variable

    def add_super_class(self, super_class_name: str):
        """
        Отвечает за добавление названия базового класса для текущего класса
        :param super_class_name: название базового класса
        :return:
        """
        self.super_class_name = super_class_name

    def get_vars_count(self):
        return len(self.vars_names)

    def get_methods_count(self):
        return len(self.methods_names)
