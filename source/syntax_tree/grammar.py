from .base import Visitable


class Program(Visitable):
    def __init__(self, main, classes, place):
        Visitable.__init__(self, place)
        self.main = main
        self.class_decl_list = classes.class_decl_list
