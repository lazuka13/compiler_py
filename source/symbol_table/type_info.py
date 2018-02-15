from enum import Enum
from typing import Optional

from syntax_tree import Type, ClassType


class TypeEnum(Enum):
    """
    Перечисление существующих типов (UserClass для пользовательского класса)
    """
    Int = 1
    IntArray = 2
    Boolean = 3
    UserClass = 4


class TypeInfo:
    """
    Хранит информацию о типе, его название, в случае пользовательского класса
    """

    def __init__(self, type_enum: TypeEnum, user_class_name: Optional[str]):
        """
        Конструктор
        :param type_enum: Один из возможных вариантов типов
        :param user_class_name: Название пользовательского класса в случае (UserClass)
        """
        self.type_enum = type_enum
        if self.type_enum == TypeEnum.UserClass:
            self.user_class_name = user_class_name
        else:
            self.user_class_name = None

    def get_type_string(self):
        """
        Отвечает за получение "человеческого" представления типа
        :return:
        """
        if self.type_enum == TypeEnum.Int:
            return 'int'
        if self.type_enum == TypeEnum.IntArray:
            return 'int []'
        if self.type_enum == TypeEnum.Boolean:
            return 'boolean'
        if self.type_enum == TypeEnum.UserClass:
            return self.user_class_name
        raise KeyError()

    @classmethod
    def from_type(cls, type_of: Type):
        """
        Отвечает за конвертацию из AST Type в ST TypeInfo
        :param type_of:
        :return:
        """
        if isinstance(type_of, ClassType):
            obj = cls(TypeEnum.UserClass, type_of.label)
        elif type_of.label == 'int_array':
            obj = cls(TypeEnum.IntArray, 'int []')
        elif type_of.label == 'int':
            obj = cls(TypeEnum.Int, 'int')
        elif type_of.label == 'boolean':
            obj = cls(TypeEnum.Boolean, 'bool')
        else:
            raise Exception
        return obj

    def __eq__(self, other):
        """
        Отвечает за сравнение типов (не по ссылке, а по значению)
        :param other:
        :return:
        """
        if self.type_enum == other.type_enum and self.type_enum != TypeEnum.UserClass:
            return True
        if self.type_enum == TypeEnum.UserClass and \
                other.type_enum == TypeEnum.UserClass and \
                self.user_class_name == other.user_class_name:
            return True
        return False
