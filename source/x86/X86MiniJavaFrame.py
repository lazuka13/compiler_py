from activation_records.IAccess import Access, RecordsType
from activation_records.IFrame import IFrame
from activation_records.InFrameAccess import InFrameAccess
from activation_records.InRegAccess import InRegAccess
from activation_records.TempAddress import TempAddress
from symbol_table.TypeInfo import TypeInfo, TypeEnum
from symbol_table.VariableInfo import VariableInfo

WORD_SIZE = 4
INT_SIZE = WORD_SIZE
BOOLEAN_SIZE = WORD_SIZE
REFERENCE_SIZE = WORD_SIZE

MAX_IN_REG = 4
EXIT_ADDRESS_NAME = "@EXIT_ADDRESS@"
RETURN_ADDRESS_NAME = "@RETURN_ADDRESS@"


def type_size(type_enum: TypeEnum):
    if type_enum == TypeEnum.UserClass:
        return REFERENCE_SIZE
    elif type_enum == TypeEnum.Int:
        return INT_SIZE
    elif type_enum == TypeEnum.IntArray:
        return REFERENCE_SIZE
    elif type_enum == TypeEnum.Boolean:
        return BOOLEAN_SIZE


class X86MiniJavaFrame(IFrame):
    """
    LocalAddress = access address + FP
    FormalAddress = access address or regIndex
    """

    def __init__(self):
        IFrame.__init__(self)
        self.formal_list = []
        self.formal_access = dict()
        self.local_access = dict()
        self.frame_pointer = None
        self.stack_pointer = None
        self.address_exit_index = 0
        self.address_return_value_index = 0
        self.formal_top_pointer = 0
        self.local_top_pointer = 0

    def add_formal(self, var_info: VariableInfo):
        var: Access = self._create_formal(RecordsType.RT_Formal, type_size(var_info.type_of.type_enum))
        self.formal_access[var_info.name] = var
        self.formal_list.append(var)

    def add_local(self, var_info: VariableInfo):
        var: Access = InFrameAccess(RecordsType.RT_Formal, type_size(var_info.type_of.type_enum),
                                    self.local_top_pointer)
        self.local_access[var_info.name] = var
        self.local_top_pointer += type_size(var_info.type_of.type_enum)

    def add_address_exit(self):
        var: Access = self._create_formal(RecordsType.RT_AddressExit, REFERENCE_SIZE)
        self.formal_access[EXIT_ADDRESS_NAME] = var
        self.address_exit_index = len(self.formal_list)
        self.formal_list.append(var)

    def add_address_return_value(self, type_of: TypeInfo):
        var: Access = self._create_formal(RecordsType.RT_AddressReturnValue, REFERENCE_SIZE)
        self.formal_access[RETURN_ADDRESS_NAME] = var
        self.address_return_value_index = len(self.formal_list)
        self.formal_list.append(var)

    def formals_count(self):
        return len(self.formal_list)

    def formal(self, index: int):
        return self.formal_list[index]

    def find_local_or_formal(self, name: str):
        res = self.local_access.get(name)
        if res is None:
            res = self.formal_access.get(name)
            assert res is not None
        return res

    def exit_address(self):
        return self.formal_list[self.address_exit_index]

    def return_address(self):
        return self.formal_list[self.address_return_value_index]

    def formal_size_int(self, index: int):
        return self.formal_list[index].size

    def formal_size_str(self, name: str):
        res = self.formal_access.get(name)
        assert res is not None
        return res

    def word_type(self):
        return TypeInfo(TypeEnum.Int, None)

    def FP(self):
        return TempAddress(self.formal_top_pointer)

    def SP(self):
        return TempAddress(self.FP().get_address() + self.local_top_pointer)

    def _create_formal(self, records_type: RecordsType, size: int):
        if len(self.formal_list) < MAX_IN_REG:
            return InRegAccess(records_type, size, len(self.formal_list))
        else:
            access: Access = InFrameAccess(records_type, size, self.formal_top_pointer)
            self.formal_top_pointer += size
            return access
