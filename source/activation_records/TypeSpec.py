from symbol_table.TypeInfo import TypeEnum


class ITypeSpec:
    def type_size(self):
        pass

    def reference_size(self, type_enum : TypeEnum):
        pass

    def word_size(self):
        pass
