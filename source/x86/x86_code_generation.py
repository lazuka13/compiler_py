from code_generation.instruction import IInstruction, MoveInstruction, \
    LabelInstruction, InstructionList
from x86.x86_instruction_set import CISCOperation, RegMove, Regs
from ir_tree.expressions.temp import Temp, TempList
from ir_tree.expressions.mem import Mem
from ir_tree.expressions.i_exp import IExp
from ir_tree.expressions.binop import Binop, BinopEnum
from ir_tree.expressions.call import Call
from ir_tree.expressions.const import Const
from ir_tree.expressions.name import Name
from ir_tree.expressions.unary_op import UnaryOp, UnaryOpEnum
from ir_tree.label import Label
from ir_tree.list import ExpList
from ir_tree.statements.i_stm import IStm
from ir_tree.statements.jump import Jump
from ir_tree.statements.jumpc import JumpC, JumpTypeEnum
from ir_tree.statements.move import Move
from ir_tree.statements.exp import Exp
from ir_tree.statements.label_stm import LabelStm
from ir_tree.translate.i_subtree_wrapper import LinearTree


class Muncher:
    def __init__(self, tree: LinearTree):
        self.stm_list = tree
        self.instructions_list = InstructionList()

    def create_instructions_list(self):
        self.generation()
        return self.instructions_list

    def generation(self):
        for stm in self.stm_list:
            self.munch_stm(stm)

    def munch_stm(self, s: IStm):
        if isinstance(s, Move):
            self.munch_move(s.source, s.destination)
        elif isinstance(s, Jump):
            self.munch_jump(s.label_to_jump)
        elif isinstance(s, JumpC):
            self.munch_jumpc(s.condition_left_expression,
                             s.condition_right_expression,
                             s.true_label,
                             s.jump_type_enum)
        elif isinstance(s, LabelStm):
            self.munch_label_stm(s.label_name)
        elif isinstance(s, Exp):
            self.munch_exp(s.expression)
        else:
            raise NotImplementedError()

    def munch_exp(self, exp: IExp):
        if isinstance(exp, Mem):
            return self.munch_mem(exp)
        elif isinstance(exp, Binop):
            return self.munch_binop(exp)
        elif isinstance(exp, Const):
            return_reg = Temp("Const")
            self.instructions_list.registers.append(return_reg)
            self.emit(RegMove(
                "MOV %0 " + str(exp.value),
                exp,
                return_reg)
            )
            return return_reg
        elif isinstance(exp, Temp):
            return exp
        elif isinstance(exp, Call):
            return self.munch_call(exp)
        elif isinstance(exp, Name):
            result = Temp("Name")
            self.instructions_list.registers.append(result)
            self.emit(RegMove(
                "MOV %0" + exp.label_name.name,
                Const(0),
                result
            ))
            return result
        elif isinstance(exp, UnaryOp):
            if exp.operation == UnaryOpEnum.NOT:
                result = Temp("NOT")
                self.instructions_list.registers.append(result)
                self.emit(RegMove(
                    "MOV %0 %1",
                    self.munch_exp(exp.expression),
                    result
                ))
                self.emit(CISCOperation(
                    "NOT %0",
                    [result],
                    [result]
                ))
                return result
            else:
                raise NotImplementedError()
        else:
            raise NotImplementedError()

    def munch_move(self, source, destination):
        if isinstance(source, Mem):
            exp = source.expression
            if isinstance(exp, Binop) and \
                            exp.operation == BinopEnum.PLUS:
                if isinstance(exp.right_expression, Const):
                    self.emit(RegMove(
                        "MOV %0 [%1+" + str(exp.right_expression.value) + "]",
                        self.munch_exp(exp.left_expression),
                        self.munch_exp(destination)
                    ))
                elif isinstance(exp.left_expression, Const):
                    self.emit(RegMove(
                        "MOV %0 [%1+" + str(exp.left_expression.value) + "]",
                        self.munch_exp(exp.right_expression),
                        self.munch_exp(destination)
                    ))
                else:
                    self.emit(RegMove(
                        "MOV %0 [%1]",
                        self.munch_exp(exp),
                        self.munch_exp(destination)
                    ))
            elif isinstance(exp, Temp):
                self.emit(RegMove(
                    "MOV %0 %1",
                    exp,
                    self.munch_exp(destination)
                ))
            else:
                self.emit(RegMove(
                    "MOV %0 [%1]",
                    self.munch_exp(exp),
                    self.munch_exp(destination)
                ))
        ###
        elif isinstance(destination, Mem):
            exp = destination.expression
            if isinstance(exp, Binop) and \
                            exp.operation == BinopEnum.PLUS:
                if isinstance(exp.right_expression, Const):
                    self.emit(RegMove(
                        "MOV [%0 + " + str(exp.right_expression.value) + "] %1",
                        _fromlist=[
                            self.munch_exp(source),
                            self.munch_exp(exp.left_expression)
                        ]
                    ))
                elif isinstance(exp.left_expression, Const):
                    self.emit(RegMove(
                        "MOV [%0 + " + str(exp.left_expression.value) + "] %1",
                        _fromlist=[
                            self.munch_exp(source),
                            self.munch_exp(exp.right_expression)
                        ]
                    ))
                else:
                    self.emit(RegMove(
                        "MOV [%0] %1",
                        _fromlist=[
                            self.munch_exp(source),
                            self.munch_exp(exp)
                        ]
                    ))
            else:
                self.emit(RegMove(
                    "MOV [%0] %1",
                    _fromlist=[
                        self.munch_exp(source),
                        self.munch_exp(destination.expression)
                    ]
                ))
        ###
        elif isinstance(destination, Temp):
            self.emit(RegMove(
                "MOV %0 %1",
                self.munch_exp(source),
                destination
            ))
        ###
        else:
            self.emit(RegMove(
                "MOV %0 %1",
                self.munch_exp(source),
                self.munch_exp(destination)
            ))

    def munch_exp_list(self, exp_list: ExpList):
        head = exp_list.head
        tail = exp_list.tail
        temps = []
        if isinstance(head, ExpList):
            sub_temps = self.munch_exp_list(head)
            temps += sub_temps
        else:
            temps.append(self.munch_exp(head))
        if isinstance(tail, ExpList):
            sub_temps = self.munch_exp_list(tail)
            temps += sub_temps
        elif tail:
            temps.append(self.munch_exp(tail))
        return temps

    def munch_mem(self, mem: Mem):
        exp = mem.expression
        if isinstance(exp, Binop) and \
                        exp.operation == BinopEnum.PLUS:
            if isinstance(exp.right_expression, Const):
                left = self.munch_exp(exp.left_expression)
                returned_reg = Temp("MEM(BINOP(PLUS, e1, CONST(i)))")
                self.instructions_list.registers.append(returned_reg)
                self.emit(RegMove(
                    "MOV %0 [%1 + " + str(exp.right_expression.value) + "]",
                    left,
                    returned_reg
                ))
                return returned_reg
            elif isinstance(exp.left_expression, Const):
                right = self.munch_exp(exp.right_expression)
                returned_reg = Temp("MEM(BINOP(PLUS, CONST(i), e1))")
                self.instructions_list.registers.append(returned_reg)
                self.emit(RegMove(
                    "MOV %0 [%1 + " + str(exp.left_expression.value) + "]",
                    right,
                    returned_reg
                ))
                return returned_reg
            else:
                returned_reg = Temp("MEM(e1)")
                self.instructions_list.registers.append(returned_reg)
                self.emit(RegMove(
                    "MOV %0 [%1]",
                    self.munch_exp(exp),
                    returned_reg
                ))
                return returned_reg
        elif isinstance(exp, Const):
            returned_reg = Temp("MEM(Const(i))")
            self.instructions_list.registers.append(returned_reg)
            self.emit(RegMove(
                "MOV %0 [" + str(exp.value) + "]",
                exp,
                returned_reg
            ))
            return returned_reg
        else:
            e1 = self.munch_exp(mem.expression)
            returned_reg = Temp("MEM(e1)")
            self.instructions_list.registers.append(returned_reg)
            self.emit(RegMove(
                "MOV %0 [%1]",
                e1,
                returned_reg
            ))
            return returned_reg

    def munch_call(self, call: Call):
        eax = Temp("EAX", unique_id=Regs.EAX.value)
        self.instructions_list.registers.append(eax)
        list_args = self.munch_exp_list(call.args)
        fe = call.func_expr
        if isinstance(fe, Mem):
            func_address = fe.expression
            list_args.append(func_address)
            self.emit(CISCOperation(
                "CALL [%" + str(len(list_args)-1) + "]",
                list_args,
                TempList()
            ))
            return eax
        elif isinstance(fe, Name):
            self.emit(CISCOperation(
                "CALL " + fe.label_name.name,
                list_args,
                TempList()
            ))
            return eax
        else:
            raise NotImplementedError()

    def munch_binop(self, binop: Binop):
        if binop.operation == BinopEnum.PLUS:
            return self.munch_binop_regular(binop, "ADD ")
        elif binop.operation == BinopEnum.MINUS:
            return self.munch_binop_regular(binop, "SUB ")
        elif binop.operation == BinopEnum.OR:
            return self.munch_binop_regular(binop, "OR ")
        elif binop.operation == BinopEnum.AND:
            return self.munch_binop_regular(binop, "AND ")
        elif binop.operation == BinopEnum.MOD:
            return self.munch_binop_div(binop)
        elif binop.operation == BinopEnum.MUL:
            return self.munch_binop_mul(binop)
        else:
            raise NotImplementedError()

    def munch_binop_regular(self, binop: Binop, prefix: str):
        returned_reg = Temp("BINOP(Regular)")
        self.instructions_list.registers.append(returned_reg)
        if isinstance(binop.left_expression, Const):
            self.emit(RegMove(
                "MOV %0 %1",
                self.munch_exp(binop.right_expression),
                returned_reg
            ))
            self.emit(CISCOperation(
                prefix + "%0 " + str(binop.left_expression.value),
                [returned_reg],
                [returned_reg]
            ))
            return returned_reg
        elif isinstance(binop.right_expression, Const):
            self.emit(RegMove(
                "MOV %0 %1",
                self.munch_exp(binop.left_expression),
                returned_reg
            ))
            self.emit(CISCOperation(
                prefix + "%0 " + str(binop.right_expression.value),
                [returned_reg],
                [returned_reg]
            ))
            return returned_reg
        else:
            self.emit(RegMove(
                "MOV %0 %1",
                self.munch_exp(binop.left_expression),
                returned_reg
            ))
            self.emit(CISCOperation(
                prefix + "%0 %1",
                [self.munch_exp(binop.right_expression)],
                [returned_reg]
            ))
            return returned_reg


    def munch_binop_mul(self, binop: Binop):
        returned_reg = Temp("BINOP(Regular)")
        self.instructions_list.registers.append(returned_reg)
        if isinstance(binop.left_expression, Const):
            self.emit(CISCOperation(
                "IMUL %0 %1 " + str(binop.left_expression.value),
                [self.munch_exp(binop.right_expression)],
                [returned_reg]
            ))
            return returned_reg
        elif isinstance(binop.right_expression, Const):
            self.emit(CISCOperation(
                "IMUL %0 %1 " + str(binop.right_expression.value),
                [self.munch_exp(binop.left_expression)],
                [returned_reg]
            ))
            return returned_reg
        else:
            self.emit(RegMove(
                "MOV %0 %1",
                self.munch_exp(binop.left_expression),
                returned_reg
            ))
            self.emit(CISCOperation(
                "IMUL %0 %1",
                [self.munch_exp(binop.right_expression)],
                [returned_reg]
            ))
            return returned_reg

    def munch_binop_div(self, binop: Binop):
        eax = Temp("EAX", unique_id=Regs.EAX.value)
        self.instructions_list.registers.append(eax)
        edx = Temp("EDX", unique_id=Regs.EDX.value)
        self.instructions_list.registers.append(eax)
        self.emit(RegMove(
            "MOV %0 %1",
            self.munch_exp(binop.left_expression),
            eax
        ))
        self.emit(CISCOperation(
            "IDIV %1",
            [self.munch_exp(binop.right_expression), eax],
            [edx]
        ))
        return_reg = Temp("BINOP(Regular)")
        self.instructions_list.registers.append(return_reg)
        self.emit(RegMove(
            "MOV %0 %1",
            edx,
            return_reg
        ))
        return return_reg

    def munch_jump(self, label_to_jump: Label):
        self.emit(CISCOperation(
            "JMP %l",
            TempList(),
            TempList(),
            [label_to_jump]
        ))

    def munch_jumpc(
            self, condition_left_expression: IExp,
            condition_right_expression: IExp,
            true_label: Label, jump_type: JumpC):
        if isinstance(condition_left_expression, Const):
            e = self.munch_exp(condition_right_expression)
            self.emit(CISCOperation(
                "CMP %0 " + str(condition_left_expression.value),
                [e],
                TempList()
            ))
        elif isinstance(condition_right_expression, Const):
            e = self.munch_exp(condition_left_expression)
            self.emit(CISCOperation(
                "CMP %0 " + str(condition_right_expression.value),
                [e],
                TempList()
            ))
        else:
            e1 = self.munch_exp(condition_left_expression)
            e2 = self.munch_exp(condition_right_expression)
            self.emit(CISCOperation(
                "CMP %0 %1",
                [e1, e2],
                TempList()
            ))
        if jump_type == JumpTypeEnum.EQ:
            self.emit(CISCOperation(
                "JE %l",
                TempList(),
                TempList(),
                [true_label]
            ))
        elif jump_type == JumpTypeEnum.LT:
            self.emit(CISCOperation(
                "JL %l",
                TempList(),
                TempList(),
                [true_label]
            ))
        elif jump_type == JumpTypeEnum.NEQ:
            self.emit(CISCOperation(
                "JNE %l",
                TempList(),
                TempList(),
                [true_label]
            ))
        else:
            raise NotImplementedError()

    def munch_label_stm(self, label_name: Label):
        self.emit(LabelInstruction(label_name))

    def emit(self, next_instruction: IInstruction):
        self.instructions_list.instructions.append(next_instruction)
        return next_instruction
