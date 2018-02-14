from .IAccess import Access, RecordsType
from .TempAddress import TempAddress


class InFrameAccess(Access):
    def __init__(self, record_type: RecordsType, size: int, offset: int):
        Access.__init__(self)
        self.record_type = record_type
        self.size = size
        self.address = TempAddress(offset)

    def offset(self):
        return self.address

    def print(self, frame_pointer: TempAddress):
        return f'In frame position {self.address.at_address(frame_pointer.get_address()).get_address()}'
