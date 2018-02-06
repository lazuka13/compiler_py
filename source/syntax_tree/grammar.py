from .base import Visitable
from .declarations import MainClass, ClassDeclList

from typing import Optional


class Program(Visitable):
    """
    Корень дерева - включает в себя главный класс и список классов
    """

    def __init__(self, main: MainClass, classes: Optional[ClassDeclList], place):
        Visitable.__init__(self, place)
        self.main = main
        self.class_decl_list = classes.class_decl_list
