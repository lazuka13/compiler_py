from enum import Enum


class RecordsType(Enum):
    RT_Formal = 1
    RT_Local = 2
    RT_FramePointer = 3
    RT_StackPointer = 4
    RT_AddressExit = 5
    RT_AddressReturnValue = 6


class Temp:
    def __init__(self, offset=None, address=None):
        self.offset = offset
        self.address = address

    def get_address(self):
        return self.address + self.offset

    def at_address(self, address):
        return Temp(offset=self.offset, address=self.address + address)

    def get_address_string(self):
        if self.address == 0:
            return f'offset {self.offset}'
        else:
            return f'address {self.address}, offset {self.offset}'

    def __eq__(self, other):
        return self.__dict__ == other.__dict__


class IAccess:
    def __init__(self):
        pass

    def get_record_type(self) -> RecordsType:
        pass

    def print(self):
        pass

    def get_size(self, fp: Temp) -> int:
        pass


class AddressExit(Temp):
    """

    """

    def __init__(self, address):
        Temp.__init__(self, address=address)


class AddressReturnValue(Temp):
    """

    """

    def __init__(self, address):
        Temp.__init__(self, address=address)


class FramePointer:
    """

    """

    def __init__(self, pointer):
        self.pointer = pointer
