class TempAddress:
    def __init__(self, offset=0, address=0):
        self.offset = offset
        self.address = address

    def get_address(self) -> int:
        return self.address + self.offset

    def at_address(self, address: int):
        return TempAddress(offset=self.offset, address=self.address + address)

    def get_address_string(self) -> str:
        if self.address == 0:
            return f'offset {self.offset}'
        else:
            return f'address {self.address}, offset {self.offset}'

    def __eq__(self, other):
        return self.__dict__ == other.__dict__
