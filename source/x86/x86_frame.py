from activation_records.i_access import IAccess, RecordsType
from activation_records.i_frame import IFrame
from activation_records.in_frame_access import InFrameAccess
from activation_records.in_reg_access import InRegAccess
from activation_records.temp_address import TempAddress
from symbol_table.type_info import TypeInfo, TypeEnum
from symbol_table.variable_info import VariableInfo
from x86.x86_type_spec import X86MiniJavaTypeSpec
from ir_tree.name_conventions import *

MAX_IN_REG = 4
EXIT_ADDRESS_NAME = "@EXIT_ADDRESS@"
RETURN_ADDRESS_NAME = "@RETURN_ADDRESS@"


class X86MiniJavaFrame(IFrame):
    """
    Реализация фрейма под конкретную архитектуру x86
    """

    def __init__(self):
        IFrame.__init__(self)
        self.formal_list = []
        self.formal_access = dict()
        self.local_access = dict()
        self.frame_pointer = None
        self.stack_pointer = None
        self.address_exit_index = 0
        self.formal_top_pointer = 0
        self.local_top_pointer = 0
        self.type_spec = X86MiniJavaTypeSpec()
        self.return_address: IAccess = InRegAccess(RecordsType.RT_AddressReturnValue,
                                                   self.type_spec.word_size(),
                                                   None,
                                                   RETURN_ADDRESS)

    def type_size(self, type_enum: TypeEnum):
        return self.type_spec.type_size(type_enum)

    def add_formal(self, var_info: VariableInfo):
        var: IAccess = self._create_formal(RecordsType.RT_Formal, self.type_size(var_info.type_of.type_enum))
        self.formal_access[var_info.name] = var
        self.formal_list.append(var)

    def add_local(self, var_info: VariableInfo):
        var: IAccess = InFrameAccess(RecordsType.RT_Formal, self.type_size(var_info.type_of.type_enum),
                                     self.local_top_pointer)
        self.local_access[var_info.name] = var
        self.local_top_pointer += self.type_size(var_info.type_of.type_enum)

    def add_address_exit(self):
        var: IAccess = self._create_formal(RecordsType.RT_AddressExit, self.type_spec.reference_size())
        self.formal_access[EXIT_ADDRESS_NAME] = var
        self.address_exit_index = len(self.formal_list)
        self.formal_list.append(var)

    def add_address_return_value(self, type_of: TypeInfo):
        pass

    def formals_count(self):
        return len(self.formal_list)

    def formal(self, index: int):
        return self.formal_list[index]

    def find_local_or_formal(self, name: str):
        res = self.local_access.get(name)
        if res is None:
            res = self.formal_access.get(name)
        return res

    def exit_address(self):
        return self.formal_list[self.address_exit_index]

    def formal_size_int(self, index: int):
        return self.formal_list[index].size

    def formal_size_str(self, name: str):
        res = self.formal_access.get(name)
        assert res is not None
        return res

    def word_type(self):
        return TypeInfo(TypeEnum.INT, None)

    def FP(self):
        return TempAddress(self.formal_top_pointer)

    def SP(self):
        return TempAddress(self.FP().get_address() + self.local_top_pointer)

    def _create_formal(self, records_type: RecordsType, size: int):
        if len(self.formal_list) < MAX_IN_REG:
            return InRegAccess(records_type, size, None, len(self.formal_list))
        else:
            access: IAccess = InFrameAccess(records_type, size, self.formal_top_pointer)
            self.formal_top_pointer += size
            return access
