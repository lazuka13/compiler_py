from symbol_table.method_info import MethodInfo
from symbol_table.variable_info import VariableInfo

from syntax_tree import Position


class IClassStruct:
    """
    Отвечает за то, как хранится класс в памяти - его виртуальная таблица методов,
    расположение переменных, также отвечает за то, как выделяется место
    Реализуется для конкретной архитектуры (см. x86)

    # TODO type-hints
    """

    def __init__(self):
        pass

    def add_class_name(self, class_name: str):
        pass

    def add_to_vtable(self, method_info: MethodInfo):
        pass

    def add_field(self, variable_info: VariableInfo):
        pass

    def get_vtable(self):
        pass

    def get_table_name(self):
        pass

    def get_field_from(self, field_name, base, position):
        pass

    def get_virtual_method_address(self, method_name, base, position):
        pass

    def allocate_new(self, position: Position):
        pass
