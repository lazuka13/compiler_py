from symbol_table.type_info import TypeEnum


class ITypeSpec:
    def type_size(self, type_enum: TypeEnum):
        pass

    def reference_size(self):
        pass

    def word_size(self):
        pass
