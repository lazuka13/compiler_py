from enum import Enum

from syntax_tree import Position

from .IExp import IExp


class InfoEnum(Enum):
    ID = 1
    NAME = 2


class Temp(IExp):
    counter: int = 0

    def __init__(self, name: str = None, local_id: int = None, temp: 'Temp' = None,
                 position: Position = Position(0, 0)):
        IExp.__init__(self, position)
        self.id = Temp.counter
        Temp.counter += 1
        if local_id is None and temp is None:
            self.local_id = 0
            self.name = name
            self.info_enum = InfoEnum.NAME
        elif name is None and temp is None:
            self.local_id = local_id
            self.name = ''
            self.info_enum = InfoEnum.ID
        elif name is None and local_id is None:
            self.id = temp.id
            self.local_id = temp.local_id
            self.name = temp.name
            self.info_enum = temp.info_enum
            self.position = temp.position
