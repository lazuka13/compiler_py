class Position:
    """
    Класс для хранение расположения (столбца и строки)
    """

    def __init__(self, x, y):
        """
        Конструктор
        :param p: объект из yacc - для того, чтобы получить значения строки и столбца
        """
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


class Visitable:
    """
    Базовый класс для всех классов AST
    """

    def __init__(self, place):
        self.place = place

    def accept(self, visitor):
        visitor.visit(self)
