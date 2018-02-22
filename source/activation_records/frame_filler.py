from ir_tree.name_conventions import *
from symbol_table.class_info import ClassInfo
from symbol_table.method_info import MethodInfo
from symbol_table.table import Table
from symbol_table.variable_info import VariableInfo
from syntax_tree import Position
from x86.x86_frame import X86MiniJavaFrame
from .temp_address import TempAddress


class FrameFiller:
    def __init__(self, table: Table):
        self.table = table
        self.filled: bool = False

    def fill(self):
        assert self.filled is not True
        class_names = self.table.classes_names
        for class_name in class_names:
            position = Position(0, 0)
            self.table.add_class_to_scope(class_name, position)
            class_info = self.table.get_class(class_name, position)
            methods_names = class_info.methods_names
            for method in methods_names:
                method_info = self.table.get_method(method, position)
                frame = X86MiniJavaFrame()
                this_variable = VariableInfo(THIS_NAME, position, class_info.type_info)
                frame.add_formal(this_variable)
                for arg_info in method_info.args_block:
                    frame.add_formal(arg_info)
                for var_info in method_info.vars_block:
                    frame.add_local(var_info)
                frame.add_address_exit()
                frame.add_address_return_value(method_info.return_type)
                print(f'Method name: {method_info.name}')
                activation = frame.find_local_or_formal(THIS_NAME)
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

    def create_frame(self, class_info: ClassInfo, method_info: MethodInfo):
        frame = X86MiniJavaFrame()
        this_variable = VariableInfo(THIS_NAME, Position(0, 0), class_info.type_info)
        frame.add_formal(this_variable)
        for arg_info in method_info.args_block:
            frame.add_formal(arg_info)
        for var_info in method_info.vars_block:
            frame.add_local(var_info)
        frame.add_address_exit()
        frame.add_address_return_value(method_info.return_type)
        return frame
