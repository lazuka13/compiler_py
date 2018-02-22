from typing import List

from activation_records.i_type_spec import ITypeSpec
from ir_tree.expressions.i_exp import IExp
from ir_tree.list import ExpList, StmList
from ir_tree.name_conventions import *
from ir_tree.statements.all import *
from symbol_table.i_class_struct import IClassStruct
from symbol_table.method_info import MethodInfo
from symbol_table.variable_info import VariableInfo
from syntax_tree import Position
from .x86_type_spec import X86MiniJavaTypeSpec


class X86MiniJavaClassStruct(IClassStruct):
    def __init__(self):
        IClassStruct.__init__(self)
        self.vtable_entries: List[MethodInfo] = []
        self.vtable_indices: dict = dict()
        self.fields_offsets: dict = dict()
        self.type_spec: ITypeSpec = X86MiniJavaTypeSpec()
        self.total_fields_size: int = 0
        self.class_name: str = None

    def add_class_name(self, class_name: str):
        self.class_name = class_name

    def add_to_vtable(self, method_info: MethodInfo):
        self.vtable_indices[method_info.name] = len(self.vtable_entries)
        self.vtable_entries.append(method_info)

    def add_field(self, variable_info: VariableInfo):
        self.fields_offsets[variable_info.name] = self.total_fields_size
        self.total_fields_size = len(self.fields_offsets)

    def get_vtable(self):
        return self.vtable_entries

    def get_table_name(self):
        return VTABLE_PREFIX + self.class_name

    def get_field_from(self, field_name: str, base: IExp, position: Position):
        assert self.fields_offsets.get(field_name) is not None
        word_size = self.type_spec.word_size()
        return Mem(
            Binop(
                BinopEnum.PLUS, base, Const(word_size * 1 + self.fields_offsets[field_name], position),
                position),
            position)

    def get_virtual_method_address(self, method_name, base, position):
        assert self.vtable_indices.get(method_name) is not None
        word_size = self.type_spec.word_size()
        return Mem(
            Binop(
                BinopEnum.PLUS,
                Mem(base, position),
                Const(word_size * (1 + self.vtable_indices[method_name]), position),
                position
            ),
            position
        )

    def allocate_new(self, position: Position):
        word_size = self.type_spec.word_size()
        alloc_arg = ExpList(Const(self.total_fields_size + word_size * (len(self.vtable_entries) + 1), position),
                            None, position)
        base_address_id = 0
        base_address: Temp = Temp(None, base_address_id, None, position)
        prepare_actions: StmList = StmList(
            Move(
                base_address,
                Call(
                    Name(MALLOC_NAME, position),
                    alloc_arg,
                    position),
                position
            ),
            None,
            position
        )
        prepare_actions = StmList(
            Move(
                Mem(
                    Temp(None, None, base_address), position
                ),
                Name(self.get_table_name(), position),
                position
            ),
            prepare_actions,
            position
        )
        for offset in self.fields_offsets.items():
            prepare_actions = StmList(
                Move(
                    Binop(
                        BinopEnum.PLUS,
                        Mem(
                            Temp(None, None, base_address),
                            position
                        ),
                        Const(offset[1] + word_size * (1), position),
                        position
                    ),
                    Const(0, position),
                    position
                ),
                prepare_actions,
                position
            )
        return Eseq(prepare_actions, Temp(None, None, base_address), position)
