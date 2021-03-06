from typing import Optional

from .class_info import ClassInfo


class ScopeBlock:
    """
    Отвечает за хранение информации о текущем Scope - нужен для
    разрешения имен переменных, методов и т.д.
    """

    def __init__(self,
                 variables_block: Optional[dict],
                 methods_block: Optional[dict],
                 class_info: ClassInfo):
        self.variables_block = variables_block
        self.methods_block = methods_block
        self.class_info = class_info
