class Identifier:
    """
    Базовый класс для всех классов-идентификаторов (переменные, методы, классы)
    """

    def __init__(self, name, position):
        """
        Конструктор
        :param name: название идентификатора (имя класса / переменной / метода)
        :param position: положение идентификатора
        """
        self.name = name
        self.position = position

    def __str__(self) -> str:
        """
        Отвечает за строковое представление идентификатора
        :return: str
        """
        return self.name