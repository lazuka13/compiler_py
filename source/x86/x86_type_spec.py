from activation_records.i_type_spec import ITypeSpec, TypeEnum

WORD_SIZE = 4
INT_SIZE = WORD_SIZE * 1
BOOLEAN_SIZE = WORD_SIZE * 1
REFERENCE_SIZE = WORD_SIZE * 1


class X86MiniJavaTypeSpec(ITypeSpec):
    def __init__(self):
        ITypeSpec.__init__(self)

    def type_size(self, type_enum: TypeEnum):
        if type_enum == TypeEnum.UserClass:
            return REFERENCE_SIZE
        elif type_enum == TypeEnum.Int:
            return INT_SIZE
        elif type_enum == TypeEnum.IntArray:
            return REFERENCE_SIZE
        elif type_enum == TypeEnum.Boolean:
            return BOOLEAN_SIZE

    def reference_size(self):
        return REFERENCE_SIZE

    def word_size(self):
        return WORD_SIZE
