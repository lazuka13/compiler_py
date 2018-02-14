from .IAccess import Access
from .TempAddress import TempAddress


class InRegAccess(Access):
    def __init__(self, record_type, size, reg_number):
        Access.__init__(self)
        self.record_type = record_type
        self.size = size
        self.reg_number = reg_number

    def print(self, frame_pointer: TempAddress):
        return f'Register {self.reg_number}'
