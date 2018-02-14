from symbol_table.MethodInfo import MethodInfo
from symbol_table.VariableInfo import VariableInfo

from syntax_tree import Position


class IClassStruct:
    def add_to_vtable(self, method_info: MethodInfo):
        pass

    def add_field(self, variable_info: VariableInfo):
        pass

    def get_field_from(self, field_name, base, position):
        pass

    def get_virtual_method_address(self, method_name, base, position):
        pass

    def allocate_new(self, position: Position):
        pass