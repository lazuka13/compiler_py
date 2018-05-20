from typing import List, Dict, Set

from ir_tree.expressions.all import *
from ir_tree.i_node import INode
from ir_tree.ir_visitor import IRVisitor
from ir_tree.label import Label
from ir_tree.list import ExpList
from ir_tree.statements.all import *
from ir_tree.translate.exp_wrapper import ExpWrapper
from ir_tree.translate.i_subtree_wrapper import LinearTree
from ir_tree.translate.stm_wrapper import StmWrapper


class BaseLabelVisitor(IRVisitor):
    def __init__(self):
        IRVisitor.__init__(self)
        self.label = None

    def get_label(self) -> Label:
        return self.label

    def visit(self, obj: INode):
        if isinstance(obj, UnaryOp):
            self.visit_unary_op(obj)
        if isinstance(obj, Binop):
            self.visit_binop(obj)
        if isinstance(obj, Call):
            self.visit_call(obj)
        if isinstance(obj, Const):
            self.visit_const(obj)
        if isinstance(obj, Eseq):
            self.visit_eseq(obj)
        if isinstance(obj, Mem):
            self.visit_mem(obj)
        if isinstance(obj, Name):
            self.visit_name(obj)
        if isinstance(obj, Temp):
            self.visit_temp(obj)
        if isinstance(obj, ExpList):
            self.visit_exp_list(obj)
        if isinstance(obj, Exp):
            self.visit_exp(obj)
        if isinstance(obj, Jump):
            self.visit_jump(obj)
        if isinstance(obj, JumpC):
            self.visit_jump_c(obj)
        if isinstance(obj, LabelStm):
            self.visit_label_stm(obj)
        if isinstance(obj, Move):
            self.visit_move(obj)
        if isinstance(obj, Seq):
            self.visit_seq(obj)
        if isinstance(obj, StmWrapper):
            self.visit_stm_wrapper(obj)
        if isinstance(obj, ExpWrapper):
            self.visit_exp_wrapper(obj)

    def visit_unary_op(self, obj: UnaryOp):
        pass

    def visit_binop(self, obj: Binop):
        pass

    def visit_call(self, obj: Call):
        pass

    def visit_const(self, obj: Const):
        pass

    def visit_eseq(self, obj: Eseq):
        pass

    def visit_mem(self, obj: Mem):
        pass

    def visit_name(self, obj: Name):
        pass

    def visit_temp(self, obj: Temp):
        pass

    def visit_exp_list(self, obj: ExpList):
        pass

    def visit_exp(self, obj: Exp):
        pass

    def visit_jump(self, obj: Jump):
        pass

    def visit_jump_c(self, obj: JumpC):
        pass

    def visit_label_stm(self, obj: LabelStm):
        pass

    def visit_move(self, obj: Move):
        pass

    def visit_seq(self, obj: Seq):
        pass

    def visit_stm_wrapper(self, obj: StmWrapper):
        pass

    def visit_exp_wrapper(self, obj: ExpWrapper):
        pass

    def set_label(self, label):
        self.label = label


class InLabelVisitor(BaseLabelVisitor):
    def __init__(self):
        BaseLabelVisitor.__init__(self)

    def visit_label_stm(self, obj: LabelStm):
        self.set_label(obj.label_name)


class OutLabelVisitor(BaseLabelVisitor):
    def __init__(self):
        BaseLabelVisitor.__init__(self)

    def visit_jump(self, obj: Jump):
        self.set_label(obj.label_to_jump)

    def visit_jump_c(self, obj: JumpC):
        self.set_label(obj.true_label)


class NoJumpBlock:
    def __init__(self, tree: LinearTree):
        self.tree: LinearTree = tree
        self.in_label: Label = None
        self.out_label: Label = None
        assert len(self.tree) > 0
        in_visitor = InLabelVisitor()
        self.tree[0].accept(in_visitor)
        self.in_label = in_visitor.get_label()
        out_visitor = OutLabelVisitor()
        self.tree[-1].accept(out_visitor)
        self.out_label = out_visitor.get_label()

    @classmethod
    def copy(cls, other: 'NoJumpBlock'):
        obj = cls(list())
        obj.tree = other.tree
        other.tree = None
        obj.in_label = other.in_label
        other.in_label = None
        obj.out_label = other.out_label
        other.out_label = None
        return obj

    def release_tree(self) -> LinearTree:
        holder = self.tree
        self.tree = None
        return holder

    def get_tree(self):
        return self.tree

    def get_in_label(self):
        return self.in_label

    def get_out_label(self):
        return self.out_label


BaseBlocks: List[NoJumpBlock] = list


class NoJumpTree:
    def __init__(self, full_tree: LinearTree):
        self.blocks: BaseBlocks = list()
        self.curr_tree: LinearTree = list()
        while len(full_tree) > 0:
            in_visitor = InLabelVisitor()
            full_tree[0].accept(in_visitor)
            if in_visitor.get_label() is not None and len(self.curr_tree) > 0:
                self.add_with_jump_at_the_end(in_visitor.get_label())
                continue
            self.curr_tree.append(full_tree[0])
            full_tree.pop(0)
            out_visitor = OutLabelVisitor()
            self.curr_tree[-1].accept(out_visitor)
            if out_visitor.get_label() is not None and len(full_tree) > 0:
                self.add_ended_with(out_visitor.get_label(), full_tree)
                continue

        if len(self.curr_tree) > 0:
            self.add_last()

    @classmethod
    def copy(cls, other):
        obj = cls(list())
        obj.blocks = other.blocks
        other.blocks = None
        return obj

    def build_tree(self) -> LinearTree:
        tree: LinearTree = list()
        for i in range(len(self.blocks)):
            go_from = 0
            miss_first = i < len(self.blocks) - 1 and \
                         self.blocks[i].get_out_label() == self.blocks[i + 1].get_in_label()
            go_to = len(self.blocks[i].get_tree())
            if miss_first:
                go_to -= 1
            subtree: LinearTree = self.blocks[i].release_tree()
            while go_from < go_to:
                tree.append(subtree[go_from])
                go_from += 1

        self.delete_unused_labels(tree)
        return tree

    def add_with_jump_at_the_end(self, label: Label):
        out_visitor = OutLabelVisitor()
        self.curr_tree[-1].accept(out_visitor)
        if out_visitor.get_label() != label:
            self.curr_tree.append(Jump(label))
        self.blocks.append(NoJumpBlock(self.curr_tree))
        self.curr_tree = list()

    def add_ended_with(self, label: Label, full_tree: LinearTree) -> None:
        if len(full_tree) == 0:
            self.blocks.append(NoJumpBlock(self.curr_tree))
            self.curr_tree = list()
            return
        in_visitor = InLabelVisitor()
        full_tree[0].accept(in_visitor)
        if in_visitor.get_label() == label:
            self.blocks.append(NoJumpBlock(self.curr_tree))
            self.curr_tree = list()
            return  # reset curr_tree
        label = Label.get_next_enumerated_label()
        self.curr_tree.append(Jump(label))
        self.blocks.append(NoJumpBlock(self.curr_tree))
        self.curr_tree = list()
        self.curr_tree.append(LabelStm(label))
        return  # reset curr_tree

    def add_last(self):
        self.blocks.append(NoJumpBlock(self.curr_tree))

    @staticmethod
    def delete_unused_labels(tree: LinearTree):
        used_labels: Set[Label] = set()
        unused_labels: Dict[Label, List[int]] = dict()
        for i in range(len(tree)):
            tree_el = tree[i]
            in_visitor = InLabelVisitor()
            tree_el.accept(in_visitor)
            out_visitor = OutLabelVisitor()
            tree_el.accept(out_visitor)
            if out_visitor.get_label() is not None:
                used_labels.add(out_visitor.get_label())
                unused_labels.pop(out_visitor.get_label(), None)
            in_label = in_visitor.get_label()
            if in_label is not None and in_label not in used_labels:
                if in_label not in unused_labels:
                    unused_labels[in_label] = list()
                unused_labels[in_label].append(i)
        indexes = set()

        for key, value in unused_labels.items():
            for pos in value:
                indexes.add(pos)
        deleted = 0
        for pos in indexes:
            tree.pop(pos - deleted)
            deleted += 1


NoJumpBlocksForest: Dict[str, NoJumpTree] = dict
