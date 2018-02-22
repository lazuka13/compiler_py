from ir_tree.name_conventions import *
from symbol_table.class_info import ClassInfo
from symbol_table.method_info import MethodInfo
from symbol_table.table import Table
from symbol_table.variable_info import VariableInfo
from syntax_tree import Position
from x86.x86_frame import X86MiniJavaFrame
from .temp_address import TempAddress


class FrameFiller:
    """
    Отвечает за создание Frame-ов (create_frame)
    и заполнение таблицы данными для примера (метод fill)

    # TODO Хорошо ли, что FrameFiller содержит метод create_frame?
    """

    def __init__(self, table: Table, verbose=False):
        self.table = table
        self.filled: bool = False
        self.verbose: bool = verbose

    def fill(self):
        """
        Отвечает за вывод задания по записям активации
        Заполняет фрейм, словно был вызов метода на пустом стеке
        :return:
        """
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
                self.print(f'Method name: {method_info.name}')
                activation = frame.find_local_or_formal(THIS_NAME)
                self.print(f'this: {activation.print(frame.FP())}')
                for arg_name in method_info.args_names:
                    activation = frame.find_local_or_formal(arg_name)
                    self.print(f'{arg_name}: {activation.print(TempAddress(0))}')
                    self.print(f'FP: {frame.FP().get_address()}')
                for var_name in method_info.vars_names:
                    activation = frame.find_local_or_formal(var_name)
                    self.print(f'{var_name}: {activation.print(frame.FP())}')
                self.print(f'SP: {frame.SP().get_address()}')
                self.print(f'Return address: {frame.return_address.print(TempAddress(0))}')
                self.print(f'Exit address: {frame.exit_address().print(TempAddress(0))}')
                self.print('- - - - - - - - - - - - -')
                self.print('')
            self.table.free_last_scope()
        self.filled = True

    def print(self, message):
        if self.verbose:
            print(message)

    @staticmethod
    def create_frame(class_info: ClassInfo, method_info: MethodInfo):
        """
        Отвечает за создание и заполнении фрейма на основании данных о классе и методе
        :param class_info:
        :param method_info:
        :return:
        """
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


