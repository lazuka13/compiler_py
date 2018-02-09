from typing import Optional

from .base import Visitable
from .declarations import MainClass, ClassDeclList


class Program(Visitable):
    """
    Корень дерева - включает в себя главный класс и список классов
    """

    def __init__(self, main: MainClass, classes: Optional[ClassDeclList], position):
        Visitable.__init__(self, position)
        self.main = main
        self.class_decl_list = classes.class_decl_list
