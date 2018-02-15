from typing import Optional

from activation_records.i_frame import IFrame
from syntax_tree import Position
from .class_info import ClassInfo
from .method_info import MethodInfo
from .scope_block import ScopeBlock
from .variable_info import VariableInfo


class Table:
    """
    Таблица символов - отвечает за хранение информации о классах, переменных, методах
    Отвечает также за проверки классов, суперклассов, существования и переобъявления
    переменных. Отвечает за понятие Scope - доступных на данных момент переменных, методов
    """

    def __init__(self):
        """
        Конструктор (таблица заполняется снаружи при помощи методов)
        """
        self.classes_block = dict()
        self.classes_names = []

        self.verified_classes = set()
        self.blocks = []
        self.frames = dict()

    def add_class(self, class_info: ClassInfo):
        """
        Отвечает за добавление в таблицу информации о классе
        :param class_info: информация о классе
        :return:
        """
        already_found: ClassInfo = self.classes_block.get(class_info.name)
        if already_found is not None:
            raise SyntaxError(f'Class {class_info.name} already defined at {already_found.name}, '
                              f'{already_found.position}! Position {class_info.position}')
        self.classes_names.append(class_info.name)
        self.classes_block[class_info.name] = class_info

    def _add_class_to_scope(self, class_info: ClassInfo):
        """
        Отвечает за добавление класса в текущий Scope
        :param class_info: информация о классе
        :return:
        """
        self.blocks.append(ScopeBlock(class_info.variables_block, class_info.methods_block, class_info))

    def _add_method_to_scope(self, method_info: MethodInfo):
        """
        Отвечает за добавление метода в текущий Scope
        :param method_info:
        :return:
        """
        self.blocks.append(ScopeBlock(method_info.variables_block, None, self.blocks[-1].class_info))

    def add_class_to_scope(self, class_name: str, position: Position = Position(0, 0)):
        """
        Отвечает за добавление класса в текущий Scope по его названию
        :param class_name: название класса
        :param position: расположение класса
        :return:
        """
        class_to_add = self.get_class(class_name, position)
        if class_to_add.name not in self.verified_classes:
            self.verify_class(class_to_add, position)
        classes_stack = [class_to_add]
        while class_to_add.super_class_name is not None:
            class_to_add = self.get_class(class_to_add.super_class_name, position)
            classes_stack.append(class_to_add)
        for class_info in classes_stack:
            self._add_class_to_scope(class_info)

    def add_method_to_scope(self, method_name: str, position: Position = Position(0, 0)):
        """
        Отвечает за добавление метода в текущий Scope по его названию
        :param method_name: название метода
        :param position: расположение метода
        :return:
        """
        self._add_method_to_scope(self.get_method(method_name, position))

    def verify_class(self, class_info: ClassInfo, position: Position = Position(0, 0)):
        """
        Отвечает за проверку класса на циклическую зависимость
        :param class_info: информация о проверяемом классе
        :param position: расположение проверяемого класса
        :return:
        """
        classes_in_graph = set()
        class_to_check = class_info
        while class_to_check.super_class_name is not None:
            class_to_check = self.get_class(class_to_check.super_class_name, position)
            if class_to_check in classes_in_graph:
                raise SyntaxError(f'Cyclic dependency of class {class_to_check.name}! Position {class_info.position}')
            classes_in_graph.add(class_info)
        for class_info in classes_in_graph:
            self.verified_classes.add(class_info)

    def get_class(self, class_name: str, position: Position = Position(0, 0)) -> ClassInfo:
        """
        Отвечает за получение информации о классе по его названию и расположению
        :param class_name: название класса
        :param position: расположение класса
        :return:
        """
        class_info = self.classes_block.get(class_name)
        if class_info is not None:
            return class_info
        raise SyntaxError(f'Not declared class {class_name} requested! Position {position}')

    def get_method(self, method_name: str, position: Position = Position(0, 0)) -> MethodInfo:
        """
        Отвечает за получение информации о методе по его названию и расположению
        :param method_name: название метода
        :param position: расположение метода
        :return:
        """
        for block in reversed(self.blocks):
            methods_block = block.methods_block
            result = methods_block.get(method_name)
            if result is not None:
                return result
        raise SyntaxError(f'Not declared method {method_name} requested! Position {position}')

    def get_variable(self, variable_name: str, position: Position = Position(0, 0)) -> VariableInfo:
        """
        Отвечает за получение информации о переменной по ее названию и расположению
        :param variable_name: название переменной
        :param position: расположение переменной
        :return:
        """
        for block in reversed(self.blocks):
            variables_block = block.variables_block
            result = variables_block.get(variable_name)
            if result is not None:
                return result
        raise SyntaxError(f'Not declared variable {variable_name} requested! Position {position}')

    def get_scoped_class(self) -> Optional[ClassInfo]:
        """
        Возвращает информацию о классе из последнего Scope
        :return:
        """
        if len(self.blocks) > 0 and self.blocks[0].class_info is not None:
            return self.blocks[0].class_info
        return None

    def does_type_have_super(self, class_info: ClassInfo, super_class_name: str,
                             position: Position = Position(0, 0)) -> bool:
        """
        Проверяет, является ли класс наследником другого класса
        :param class_info: название класса
        :param super_class_name: название предполагаемого базового класса
        :param position: позиция, на которой произошел вызов
        :return:
        """
        while class_info.super_class_name is not None:
            if class_info.super_class_name == super_class_name:
                return True
            class_info = self.get_class(class_info.super_class_name, position)
        return False

    def free_last_scope(self):
        """
        Удаляет Scope таблицы
        :return:
        """
        self.blocks.pop(len(self.blocks) - 1)

    def add_frame(self, method_name: str, frame: IFrame):
        if self.frames.get(method_name) is not None:
            raise SyntaxError(f'Method {method_name} already has declared frame!')
        self.frames[method_name] = frame

    def get_frame(self, method_name: str):
        frame = self.frames.get(method_name)
        if frame is None:
            raise SyntaxError(f'Method {method_name} does not have a declared frame!')
        return frame
