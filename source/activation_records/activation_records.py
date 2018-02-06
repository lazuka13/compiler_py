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
