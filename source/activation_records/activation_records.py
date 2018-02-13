from enum import Enum

import symbol_table as st
import syntax_tree as ast


class TempAddress:
    def __init__(self, offset=0, address=0):
        self.offset = offset
        self.address = address

    def get_address(self) -> int:
        return self.address + self.offset

    def at_address(self, address: int):
        return TempAddress(offset=self.offset, address=self.address + address)

    def get_address_string(self) -> str:
        if self.address == 0:
            return f'offset {self.offset}'
        else:
            return f'address {self.address}, offset {self.offset}'

    def __eq__(self, other):
        return self.__dict__ == other.__dict__


class RecordsType(Enum):
    RT_Formal = 1
    RT_Local = 2
    RT_FramePointer = 3
    RT_StackPointer = 4
    RT_AddressExit = 5
    RT_AddressReturnValue = 6


class Access:
    def __init__(self):
        pass

    def print(self, frame_pointer: TempAddress):
        pass


class IFrame:
    def __init__(self):
        pass

    def add_formal(self, *args):
        pass

    def add_local(self, *args):
        pass

    def add_address_exit(self):
        pass

    def add_address_return_value(self, *args):
        pass

    def formals_count(self):
        pass

    def formal(self, index: int):
        pass

    def find_local_or_formal(self, name: str):
        pass

    def exit_address(self):
        pass

    def return_address(self):
        pass

    def word_type(self):
        pass


class FramePointer:
    def __init__(self, pointer):
        self.pointer = pointer


class InFrameAccess(Access):
    def __init__(self, record_type: RecordsType, size: int, offset: int):
        Access.__init__(self)
        self.record_type = record_type
        self.size = size
        self.address = TempAddress(offset)

    def offset(self):
        return self.address

    def print(self, frame_pointer: TempAddress):
        return f'In frame position {self.address.at_address(frame_pointer.get_address()).get_address()}'


class InRegAccess(Access):
    def __init__(self, record_type, size, reg_number):
        Access.__init__(self)
        self.record_type = record_type
        self.size = size
        self.reg_number = reg_number

    def print(self, frame_pointer: TempAddress):
        return f'Register {self.reg_number}'


WORD_SIZE = 4
int_size = WORD_SIZE
bool_size = WORD_SIZE
reference_size = WORD_SIZE

MAX_IN_REG = 4
EXIT_ADDRESS_NAME = "@EXIT_ADDRESS@"
RETURN_ADDRESS_NAME = "@RETURN_ADDRESS@"


def type_size(type_enum: st.TypeEnum):
    if type_enum == st.TypeEnum.UserClass:
        return reference_size
    elif type_enum == st.TypeEnum.Int:
        return int_size
    elif type_enum == st.TypeEnum.IntArray:
        return reference_size
    elif type_enum == st.TypeEnum.Boolean:
        return bool_size


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

    def add_formal(self, var_info: st.VariableInfo):
        var: Access = self._create_formal(RecordsType.RT_Formal, type_size(var_info.type_of.type_enum))
        self.formal_access[var_info.name] = var
        self.formal_list.append(var)

    def add_local(self, var_info: st.VariableInfo):
        var: Access = InFrameAccess(RecordsType.RT_Formal, type_size(var_info.type_of.type_enum),
                                    self.local_top_pointer)
        self.local_access[var_info.name] = var
        self.local_top_pointer += type_size(var_info.type_of.type_enum)

    def add_address_exit(self):
        var: Access = self._create_formal(RecordsType.RT_AddressExit, reference_size)
        self.formal_access[EXIT_ADDRESS_NAME] = var
        self.address_exit_index = len(self.formal_list)
        self.formal_list.append(var)

    def add_address_return_value(self, type_of: st.TypeInfo):
        var: Access = self._create_formal(RecordsType.RT_AddressReturnValue, reference_size)
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
        return st.TypeInfo(st.TypeEnum.Int, None)

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


class FrameFiller:
    def __init__(self, table: st.Table):
        self.table = table
        self.filled: bool = False

    def fill(self):
        assert self.filled is not True
        class_names = self.table.classes_names
        for class_name in class_names:
            position = ast.Position(0, 0)
            self.table.add_class_to_scope(class_name, position)
            class_info = self.table.get_class(class_name, position)
            methods_names = class_info.methods_names
            for method in methods_names:
                method_info = self.table.get_method(method, position)
                frame = X86MiniJavaFrame()
                this_variable = st.VariableInfo('this', position, class_info.type_info)
                frame.add_formal(this_variable)
                for arg_info in method_info.args_block:
                    frame.add_formal(arg_info)
                for var_info in method_info.vars_block:
                    frame.add_local(var_info)
                frame.add_address_exit()
                frame.add_address_return_value(method_info.return_type)
                print(f'Method name: {method_info.name}')
                activation = frame.find_local_or_formal('this')
                print(f'this: {activation.print(frame.FP())}')
                for arg_name in method_info.args_names:
                    activation = frame.find_local_or_formal(arg_name)
                    print(f'{arg_name}: {activation.print(TempAddress(0))}')
                print(f'FP: {frame.FP().get_address()}')
                for var_name in method_info.vars_names:
                    activation = frame.find_local_or_formal(var_name)
                    print(f'{var_name}: {activation.print(frame.FP())}')
                print(f'SP: {frame.SP().get_address()}')
                print(f'Return address: {frame.return_address().print(TempAddress(0))}')
                print(f'Exit address: {frame.exit_address().print(TempAddress(0))}')
                print('- - - - - - - - - - - - -')
                print()
            self.table.free_last_scope()
        self.filled = True
