from activation_records.i_access import IAccess
from activation_records.i_frame import IFrame
from ir_tree import array_struct
from ir_tree.label import Label
from ir_tree.list import ExpList, StmList
from ir_tree.name_conventions import *
from ir_tree.statements.all import *
from ir_tree.expressions.all import *
from ir_tree.translate.exp_wrapper import ExpWrapper
from ir_tree.translate.stm_wrapper import StmWrapper
from symbol_table.table import Table
from symbol_table.type_info import *
from symbol_table.type_stack_visitor import TypeScopeSwitcher, MethodScopeSwitcher, TypeStackVisitor
from syntax_tree import *

println_name = 'println'
fp_name = 'fp'


class IRBuilder(Visitor):
    def __init__(self, table: Table):
        Visitor.__init__(self)
        self.table = table
        self.main_subtree = None
        self.trees = dict()
        self.current_frame: IFrame = None
        self.type_stack_visitor = TypeStackVisitor(table)

    def parse(self, program: Program):
        program.accept(self)

    def get_parse_result(self):
        return self.trees

    def visit(self, obj: Visitable):
        if isinstance(obj, BinaryExpr):
            self.visit_binary_expr(obj)
        elif isinstance(obj, Id):
            self.visit_id(obj)
        elif isinstance(obj, ClassDecl):
            self.visit_class_decl(obj)
        elif isinstance(obj, MainClass):
            self.visit_main_class(obj)
        elif isinstance(obj, MethodDecl):
            self.visit_method_decl(obj)
        elif isinstance(obj, Program):
            self.visit_program(obj)
        elif isinstance(obj, ValueExpr):
            self.visit_value_expr(obj)
        elif isinstance(obj, AssignStatement):
            self.visit_assign_statement(obj)
        elif isinstance(obj, IfStatement):
            self.visit_if_statement(obj)
        elif isinstance(obj, NotExpr):
            self.visit_not_expr(obj)
        elif isinstance(obj, CallMethodExpr):
            self.visit_call_method_expr(obj)
        elif isinstance(obj, NewIntArrExpr):
            self.visit_new_int_array_expr(obj)
        elif isinstance(obj, NewObjectExpr):
            self.visit_new_object_expr(obj)
        elif isinstance(obj, RandomAccessAssignStatement):
            self.visit_random_access_assign_statement(obj)
        elif isinstance(obj, LengthExpr):
            self.visit_length_expr(obj)
        elif isinstance(obj, PrintLineStatement):
            self.visit_print_line_statement(obj)
        elif isinstance(obj, WhileStatement):
            self.visit_while_statement(obj)
        elif isinstance(obj, Statements):
            self.visit_statements(obj)
        elif isinstance(obj, RandomAccessExpr):
            self.visit_random_access_expr(obj)
        elif isinstance(obj, ThisExpr):
            self.visit_this_expr(obj)

    def visit_program(self, obj: Program):
        obj.main.accept(self)
        for class_decl in obj.class_decl_list:
            class_decl.accept(self)

    def visit_main_class(self, obj: MainClass):
        for statement in obj.statement_list:
            statement.accept(self)
        assert self.main_subtree is not None
        self.trees[obj.id.name + '@MAIN'] = self.main_subtree

    def visit_class_decl(self, obj: ClassDecl):
        switcher = TypeScopeSwitcher(
            self.table.get_class(obj.id.name).type_info,
            None,
            self.table,
            obj.position
        )
        for method_decl in obj.method_decl_list:
            method_decl.accept(self)
        switcher.destroy()

    def visit_method_decl(self, obj: MethodDecl):
        method_info = self.table.get_method(obj.id.name, obj.position)
        switcher = MethodScopeSwitcher(
            method_info,
            None,
            self.table,
            obj.position
        )
        self.current_frame = method_info.get_frame()
        stm = None
        for statement in obj.statement_list:
            statement.accept(self)
            stm = StmList(self.main_subtree.to_stm(), None, obj.position)
        obj.result.accept(self)
        stm = StmList(self.main_subtree.to_stm(), stm, obj.position)
        name = method_info.get_full_name()
        self.trees[name] = StmWrapper(stm)
        switcher.destroy()

    def visit_binary_expr(self, obj: BinaryExpr):
        obj.left.accept(self)
        left = self.main_subtree.to_exp()
        self.type_stack_visitor.pop_type_from_stack()
        obj.right.accept(self)
        right = self.main_subtree.to_exp()
        self.type_stack_visitor.pop_type_from_stack()
        if obj.binary_enum == BinaryEnum.MINUS:
            result = Binop(BinopEnum.MINUS, left, right, obj.position)
        elif obj.binary_enum == BinaryEnum.MULT:
            result = Binop(BinopEnum.MUL, left, right, obj.position)
        elif obj.binary_enum == BinaryEnum.MINUS:
            result = Binop(BinopEnum.MINUS, left, right, obj.position)
        elif obj.binary_enum == BinaryEnum.MOD:
            result = Binop(BinopEnum.MOD, left, right, obj.position)
        elif obj.binary_enum == BinaryEnum.LESS:
            true_label = Label.get_next_enumerated_label()
            false_label = Label.get_next_enumerated_label()
            return_label = Label.get_next_enumerated_label()
            condition = JumpC(JumpTypeEnum.LT, left, right, true_label, false_label, obj.position)
            exp_value = Temp('exp_value', None, None, obj.position)
            true_branch = Seq(
                Seq(
                    LabelStm(
                        true_label,
                        obj.position
                    ),
                    Move(
                        exp_value,
                        Const(
                            1,
                            obj.position
                        ),
                        obj.position
                    ),
                    obj.position
                ),
                Jump(
                    return_label,
                    obj.position
                ),
                obj.position
            )
            false_branch = Seq(
                Seq(
                    LabelStm(
                        false_label,
                        obj.position
                    ),
                    Move(
                        Temp(None, None, exp_value),
                        Const(
                            1,
                            obj.position
                        ),
                        obj.position
                    ),
                    obj.position
                ),
                Jump(
                    return_label,
                    obj.position
                ),
                obj.position
            )
            result = Eseq(
                Seq(
                    Seq(
                        Seq(
                            condition,
                            true_branch,
                            obj.position
                        ),
                        false_branch,
                        obj.position
                    ),
                    LabelStm(
                        return_label,
                        obj.position
                    ),
                    obj.position
                ),
                Mem(
                    Temp(None, None, exp_value),
                    obj.position
                ),
                obj.position
            )
        elif obj.binary_enum == BinaryEnum.AND:
            true_label = Label.get_next_enumerated_label()
            false_label = Label.get_next_enumerated_label()
            continue_label = Label.get_next_enumerated_label()
            return_label = Label.get_next_enumerated_label()
            exp_value = Temp('exp_value', None, None, obj.position)
            condition = JumpC(JumpTypeEnum.EQ, left, Const(1, obj.position), continue_label, false_label, obj.position)
            true_branch = Seq(
                Seq(
                    LabelStm(continue_label, obj.position),
                    JumpC(JumpTypeEnum.EQ, right, Const(1, obj.position), true_label, false_label, obj.position),
                    obj.position
                ),
                Seq(
                    LabelStm(true_label, obj.position),
                    Seq(
                        Move(exp_value, Const(1, obj.position), obj.position),
                        Jump(return_label, obj.position),
                        obj.position
                    ),
                    obj.position
                ),
                obj.position
            )
            false_branch = Seq(
                LabelStm(false_label, obj.position),
                Seq(
                    Move(Temp(None, None, exp_value), Const(0, obj.position), obj.position),
                    Jump(return_label, obj.position),
                    obj.position
                ),
                obj.position
            )
            result = Eseq(
                Seq(
                    Seq(
                        condition,
                        true_branch,
                        obj.position
                    ),
                    false_branch,
                    obj.position
                ),
                Temp(None, None, exp_value),
                obj.position
            )
        elif obj.binary_enum == BinaryEnum.OR:
            true_label = Label.get_next_enumerated_label()
            false_label = Label.get_next_enumerated_label()
            continue_label = Label.get_next_enumerated_label()
            return_label = Label.get_next_enumerated_label()
            exp_value = Temp('exp_value', None, None, obj.position)
            condition = JumpC(JumpTypeEnum.EQ, left, Const(1, obj.position), true_label, continue_label, obj.position)
            true_branch = Seq(
                Seq(
                    LabelStm(continue_label, obj.position),
                    JumpC(JumpTypeEnum.EQ, right, Const(1, obj.position), true_label, false_label, obj.position),
                    obj.position
                ),
                Seq(
                    LabelStm(true_label, obj.position),
                    Seq(
                        Move(exp_value, Const(1, obj.position), obj.position),
                        Jump(return_label, obj.position),
                        obj.position
                    ),
                    obj.position
                ),
                obj.position
            )
            false_branch = Seq(
                LabelStm(false_label, obj.position),
                Seq(
                    Move(Temp(None, None, exp_value), Const(0, obj.position), obj.position),
                    Jump(return_label, obj.position),
                    obj.position
                ),
                obj.position
            )
            result = Eseq(
                Seq(
                    Seq(
                        condition,
                        true_branch,
                        obj.position
                    ),
                    false_branch,
                    obj.position
                ),
                Temp(None, None, exp_value),
                obj.position
            )
        else:
            raise Exception('NO RESULT')  # TODO
        self.main_subtree = ExpWrapper(result)
        self.type_stack_visitor.visit(obj)

    def visit_id(self, obj: Id):
        var_access: IAccess = self.current_frame.find_local_or_formal(obj.name)
        if var_access is not None:
            var_exp = var_access.get_exp(
                Temp(
                    fp_name,
                    None, None,
                    obj.position
                ),
                obj.position
            )
        else:
            assert self.table.get_scoped_class() is not None
            var_exp = self.table.get_scoped_class().class_struct.get_field_from(
                obj.name,
                self.current_frame.find_local_or_formal(THIS_NAME).get_exp(
                    Temp(
                        fp_name,
                        None, None,
                        obj.position
                    ),
                    obj.position
                ),
                obj.position
            )
        self.type_stack_visitor.visit(obj)
        self.main_subtree = ExpWrapper(var_exp)

    def visit_value_expr(self, obj: ValueExpr):
        self.main_subtree = ExpWrapper(Const(obj.value, obj.position))
        self.type_stack_visitor.visit(obj)

    def visit_assign_statement(self, obj: AssignStatement):
        obj.right.accept(self)
        access = self.current_frame.find_local_or_formal(obj.left.name)
        if access is not None:
            base_address = access.get_exp(
                Temp(fp_name, None, None, obj.position),
                obj.position
            )
        else:
            base_address = self.table.get_scoped_class().class_struct.get_field_from(
                obj.left.name,
                self.current_frame.find_local_or_formal(
                    THIS_NAME,
                ).get_exp(Temp(fp_name, None, None, obj.position), obj.position),
                obj.position
            )
        self.main_subtree = StmWrapper(Move(base_address, self.main_subtree.to_exp(), obj.position))

    def visit_not_expr(self, obj: NotExpr):
        obj.right.accept(self)
        self.type_stack_visitor.pop_type_from_stack()
        self.main_subtree = ExpWrapper(UnaryOp(UnaryOpEnum.NOT, self.main_subtree.to_exp(), obj.position))

    def visit_call_method_expr(self, obj: CallMethodExpr):
        obj.expr.accept(self)
        base_address = Temp(None, 0, None, obj.position)
        base_exp = Eseq(
            Move(
                base_address,
                self.main_subtree.to_exp(),
                obj.position
            ),
            Temp(
                None, None, base_address, obj.position
            )
        )
        info: TypeInfo = self.type_stack_visitor.get_type_from_stack()
        assert info is not None
        assert info.type_enum == TypeEnum.USER_CLASS
        type_switcher = TypeScopeSwitcher(info, None, self.table, obj.position)
        arguments = ExpList(base_exp, None, obj.position)
        for expr in obj.expr_list:
            expr.accept(self)
            arguments = ExpList(
                self.main_subtree.to_exp(),
                arguments,
                obj.position
            )
            self.type_stack_visitor.pop_type_from_stack()

        class_info = self.table.get_class(info.user_class_name)
        method_address = class_info.class_struct.get_virtual_method_address(
            obj.id.name,
            Temp(None, None, base_address),
            obj.position,
        )
        self.main_subtree = ExpWrapper(Call(method_address, arguments, obj.position))
        self.type_stack_visitor.visit(obj)
        type_switcher.destroy()

    def visit_new_int_array_expr(self, obj: NewIntArrExpr):
        obj.size.accept(self)
        self.type_stack_visitor.pop_type_from_stack()
        number_of_elements = self.main_subtree.to_exp()
        args = ExpList(
            Binop(
                BinopEnum.MUL,
                number_of_elements,
                Const(
                    self.current_frame.type_size(TypeEnum.INT),
                    obj.position
                ),
                obj.position
            ),
            obj.position
        )
        self.main_subtree = ExpWrapper(Call(Name(MALLOC_NAME, obj.position), args, obj.position))
        self.type_stack_visitor.visit(obj)

    def visit_new_object_expr(self, obj: NewObjectExpr):
        class_info = self.table.get_class(obj.id.name)
        alloc_actions = class_info.class_struct.allocate_new(obj.position)
        self.main_subtree = ExpWrapper(alloc_actions)
        self.type_stack_visitor.visit(obj)

    def visit_random_access_assign_statement(self, obj: RandomAccessAssignStatement):
        obj.position_in_arr.accept(self)
        self.type_stack_visitor.pop_type_from_stack()
        position_in_arr_expr = self.main_subtree
        obj.expr.accept(self)
        access = self.current_frame.find_local_or_formal(obj.id.name)
        if access is not None:
            base_address = access.get_exp(
                Temp(
                    fp_name, None, None,
                    obj.position
                ),
                obj.position
            )
        else:
            base_address = self.table.get_scoped_class().class_struct.get_field_from(
                obj.id.name,
                self.current_frame.find_local_or_formal(THIS_NAME).get_exp(
                    Temp(fp_name, None, None, obj.position),
                    obj.position
                ),
                obj.position
            )
        address = Mem(
            Binop(
                BinopEnum.PLUS,
                base_address,
                Binop(
                    BinopEnum.MUL,
                    Const(
                        self.current_frame.type_size(self.current_frame.word_type().type_enum),
                        obj.position
                    ),
                    position_in_arr_expr.to_exp(),
                    obj.position
                ),
                obj.position
            ),
            obj.position
        )
        self.main_subtree = StmWrapper(Move(address, self.main_subtree.to_exp(), obj.position))

    def visit_length_expr(self, obj: LengthExpr):
        obj.obj.accept(self)
        array_base = self.main_subtree.to_exp()
        self.main_subtree = ExpWrapper(array_struct.get_length(array_base, obj.position))
        self.type_stack_visitor.visit(obj)

    def visit_print_line_statement(self, obj: PrintLineStatement):
        obj.obj.accept(self)
        self.type_stack_visitor.pop_type_from_stack()
        self.main_subtree = ExpWrapper(
            Call(
                Name(
                    println_name,
                    obj.position
                ),
                ExpList(self.main_subtree.to_exp(), None, obj.position),
                obj.position
            )
        )

    def visit_if_statement(self, obj: IfStatement):
        obj.condition.accept(self)
        self.type_stack_visitor.pop_type_from_stack()
        if_branch_label = Label.get_next_enumerated_label()
        else_branch_label = Label.get_next_enumerated_label()
        exit_label = Label.get_next_enumerated_label()
        condition = self.main_subtree.to_conditional(if_branch_label, else_branch_label)
        obj.if_true.accept(self)
        if_part = Seq(
            Seq(
                LabelStm(if_branch_label, obj.position),
                self.main_subtree.to_stm(),
                obj.position
            ),
            Jump(exit_label, obj.position),
            obj.position
        )
        obj.if_false.accept(self)
        else_part = Seq(
            Seq(
                LabelStm(else_branch_label, obj.position),
                self.main_subtree.to_stm(),
                obj.position
            ),
            Jump(exit_label, obj.position),
            obj.position
        )
        self.main_subtree = StmWrapper(
            Seq(
                Seq(
                    condition,
                    Seq(
                        if_part,
                        else_part,
                        obj.position
                    ),
                    obj.position
                ),
                LabelStm(exit_label, obj.position),
                obj.position
            )
        )

    def visit_while_statement(self, obj: WhileStatement):
        obj.condition.accept(self)
        condition_label = Label.get_next_enumerated_label()
        body_label = Label.get_next_enumerated_label()
        exit_label = Label.get_next_enumerated_label()
        condition = self.main_subtree.to_conditional(body_label, exit_label)
        condition_part = Seq(LabelStm(condition_label, obj.position),
                             condition, obj.position)
        obj.action.accept(self)
        body_part = Seq(
            LabelStm(body_label, obj.position),
            Seq(
                self.main_subtree.to_stm(),
                Jump(condition_label, obj.position),
                obj.position),
            obj.position
        )
        self.main_subtree = StmWrapper(
            Seq(
                Seq(
                    condition_part,
                    body_part,
                    obj.position
                ),
                LabelStm(
                    exit_label,
                    obj.position
                ),
                obj.position
            )
        )

    def visit_statements(self, obj: Statements):
        for statement in obj.statement_list:
            statement.accept(self)

    def visit_random_access_expr(self, obj: RandomAccessExpr):
        obj.object.accept(self)
        array_base = self.main_subtree.to_exp()
        obj.position_in_arr.accept(self)
        element_number = self.main_subtree.to_exp()
        self.main_subtree = ExpWrapper(array_struct.get_element(array_base, element_number, obj.position))

    def visit_this_expr(self, obj: ThisExpr):
        self.main_subtree = ExpWrapper(
            Mem(
                self.current_frame.find_local_or_formal(THIS_NAME).get_exp(
                    Temp(fp_name, None, None, obj.position),
                    obj.position
                ),
                obj.position
            )
        )
        self.type_stack_visitor.visit(obj)
