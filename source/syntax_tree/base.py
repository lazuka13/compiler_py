class Position:
    """
    Класс для хранение расположения (столбца и строки)
    """

    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y

    def __str__(self):
        """
        Отвечает за строковое представление расположения
        :return:
        """
        return f'(line: {self.y}, col: {self.x})'


class Visitor:
    """
    Базовый класс для всех классов, обходящих дерево
    """

    def __init__(self):
        pass

    def visit(self, visitable):
        pass


class Visitable:
    """
    Базовый класс для всех классов AST
    """

    def __init__(self, position: Position):
        self.position = position

    def accept(self, visitor: Visitor):
        visitor.visit(self)
