from enum import Enum
from typing import Dict, List

from syntax_tree import Position

from .i_exp import IExp


class InfoEnum(Enum):
    ID = 1
    NAME = 2


class Temp(IExp):
    counter: int = 0
    temp_holder_local_id = 9000

    def __init__(self, name: str = None, local_id: int = None, temp: 'Temp' = None,
                 position: Position = Position(0, 0), unique_id: int = -1):
        IExp.__init__(self, position)
        if local_id is None and temp is None:
            self.id = Temp.counter
            Temp.counter += 1
            self.local_id = 0
            self.name = name
            self.info_enum = InfoEnum.NAME
            self.unique = unique_id != -1
            if self.unique:
                self.id = unique_id
                self.local_id = unique_id
        elif name is None and temp is None:
            self.id = Temp.counter
            Temp.counter += 1
            self.local_id = local_id
            self.name = ''
            self.info_enum = InfoEnum.ID
            self.unique = False
        elif name is None and local_id is None:
            self.id = temp.id
            self.local_id = temp.local_id
            self.name = temp.name
            self.info_enum = temp.info_enum
            self.position = temp.position
            self.unique = temp.unique

    def is_commutative(self):
        return True

    def is_absolutely_commutative(self):
        return self.local_id == self.temp_holder_local_id


TempList: List[Temp] = list