from syntax_tree import Position
from .Identifier import Identifier
from .TypeInfo import TypeInfo


class VariableInfo(Identifier):
    """
    Информация о переменной - ее название, положение и тип
    """

    def __init__(self, name: str, position: Position, type_of: TypeInfo):
        """
        Конструктор
        :param name: Название переменной
        :param position: Положение переменной
        :param type_of: Тип переменной
        """
        Identifier.__init__(self, name, position)
        self.type_of = type_of
