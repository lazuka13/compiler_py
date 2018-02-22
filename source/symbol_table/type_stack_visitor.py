from typing import Optional

from symbol_table.method_info import MethodInfo
from symbol_table.table import Table
from symbol_table.type_info import TypeInfo, TypeEnum
from syntax_tree import *

IntType = TypeInfo(TypeEnum.Int, None)
BooleanType = TypeInfo(TypeEnum.Boolean, None)
IntArrayType = TypeInfo(TypeEnum.IntArray, None)


class TypeScopeSwitcher:
    def __init__(self, type_info: Optional[TypeInfo], class_name: Optional[str], table: Table, position: Position):
        self.table = table
        if type_info is not None:
            self.type_info = type_info
            if type_info.type_enum == TypeEnum.UserClass:
                self.table.add_class_to_scope(type_info.user_class_name, position)
        else:
            self.type_info = self.table.get_class(class_name).type_info
            self.table.add_class_to_scope(class_name, position)

    def destroy(self):
        if self.type_info.type_enum == TypeEnum.UserClass:
            self.table.free_last_scope()


class MethodScopeSwitcher:
    def __init__(self, method_info: Optional[MethodInfo], method_name: Optional[str], table: Table, position: Position):
        self.table = table
        if method_info is not None:
            self.table.add_method_to_scope(method_info.name, position)
        else:
            self.table.add_method_to_scope(method_name, position)

    def destroy(self):
        self.table.free_last_scope()


class TypeStackVisitor(Visitor):
    def __init__(self, table: Table):
        Visitor.__init__(self)
        self.table = table
        self.types_stack = []

    def _pop_types_stack(self) -> TypeInfo:
        result = self.types_stack[-1]
        self.types_stack.pop(len(self.types_stack) - 1)
        return result

    def visit(self, obj: Visitable):
        if isinstance(obj, BinaryExpr):
            self.visit_binary_expr(obj)
        elif isinstance(obj, ValueExpr):
            self.visit_value_expr(obj)
        elif isinstance(obj, Id):
            self.visit_id(obj)
        elif isinstance(obj, NotExpr):
            self.visit_not_expr(obj)
        elif isinstance(obj, CallMethodExpr):
            self.visit_call_method_expr(obj)
        elif isinstance(obj, NewIntArrExpr):
            self.visit_new_int_array_expr(obj)
        elif isinstance(obj, NewObjectExpr):
            self.visit_new_object_expr(obj)
        elif isinstance(obj, LengthExpr):
            self.visit_length_expr(obj)
        elif isinstance(obj, RandomAccessExpr):
            self.visit_random_access_expr(obj)
        elif isinstance(obj, ThisExpr):
            self.visit_this_expr(obj)

    def visit_binary_expr(self, obj: BinaryExpr):
        if obj.binary_enum in [BinaryEnum.PLUS, BinaryEnum.MULT, BinaryEnum.MINUS, BinaryEnum.MOD]:
            self.types_stack.append(IntType)
        elif obj.binary_enum in [BinaryEnum.AND, BinaryEnum.OR, BinaryEnum.LESS]:
            self.types_stack.append(BooleanType)

    def visit_id(self, obj: Id):
        var = self.table.get_variable(obj.name, obj.position)
        self.types_stack.append(var.type_of)

    def visit_value_expr(self, obj: ValueExpr):
        if obj.value_enum == ValueEnum.INTEGER:
            self.types_stack.append(IntType)
        else:
            self.types_stack.append(BooleanType)

    def visit_not_expr(self, obj: NotExpr):
        self.types_stack.append(BooleanType)

    def visit_call_method_expr(self, obj: CallMethodExpr):
        returned = self._pop_types_stack()
        switcher = TypeScopeSwitcher(returned, None, self.table, obj.position)
        method_info = self.table.get_method(obj.id.name)
        self.types_stack.append(method_info.return_type)
        switcher.destroy()

    def visit_new_int_array_expr(self, obj: NewIntArrExpr):
        self.types_stack.append(IntArrayType)

    def visit_new_object_expr(self, obj: NewObjectExpr):
        object_type = self.table.get_class(obj.id.name, obj.position).type_info
        self.types_stack.append(object_type)

    def visit_length_expr(self, obj: LengthExpr):
        self.types_stack.append(IntType)

    def visit_random_access_expr(self, obj: RandomAccessExpr):
        self.types_stack.append(IntType)

    def visit_this_expr(self, obj: ThisExpr):
        scoped_class = self.table.get_scoped_class()
        self.types_stack.append(scoped_class.type_info)

    def get_type_from_stack(self):
        if len(self.types_stack) > 0:
            return self.types_stack[-1]
        return None

    def pop_type_from_stack(self):
        if len(self.types_stack) > 0:
            return self._pop_types_stack()
        return None
