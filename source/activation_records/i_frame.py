from symbol_table.type_info import TypeEnum


class IFrame:
    """
    # TODO
    """

    def __init__(self):
        pass

    def add_formal(self, *args):
        pass

    def add_local(self, *args):
        pass

    def add_address_exit(self):
        pass

    def add_address_return_value(self, *args):
        pass

    def formals_count(self):
        pass

    def formal(self, index: int):
        pass

    def find_local_or_formal(self, name: str):
        pass

    def exit_address(self):
        pass

    def return_address(self):
        pass

    def FP(self):
        pass

    def SP(self):
        pass

    def word_type(self):
        pass

    def type_size(self, type_enum: TypeEnum):
        pass
