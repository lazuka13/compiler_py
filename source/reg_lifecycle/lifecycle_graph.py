# coding: utf-8

from source.code_generation.instruction import InstructionList

from .lifecycle_node import LifecycleNode


class LifecycleGraph(object):
    def __init__(self, instruction_list: InstructionList):
        self._regs = set()
        self._nodes = list()
        self.labels_positions = dict()

        for instruction in instruction_list.instructions:
            used = []
            for var in instruction.src:
                self._regs.add(var)
                used.append(var)
            defined = []
            for var in instruction.dst:
                self._regs.add(var)
                defined.append(var)

            self._nodes.append(LifecycleNode(instruction, used, defined))

            if instruction.__class__.__name__ == 'LabelInstruction':
                self.labels_positions[instruction.label] = len(self._nodes) - 1

            if len(self._nodes) > 1:
                self._nodes[-2].add_connection(self._nodes[-1])

        for i in range(len(instruction_list.instructions)):
            labels = instruction_list.instructions[i].label_list
            for l in labels:
                self._nodes[i].add_connection(self._nodes[self.labels_positions[l]])

    def build_Lifecycle(self):
        nodes_to_update = set()
        for n in self._nodes:
            nodes_to_update.add(n)

        while nodes_to_update:
            node = nodes_to_update.pop()
            if node.update():
                to_update_next = node.next
                for next in to_update_next:
                    nodes_to_update.add(next)

                to_update_prev = node.prev
                for next in to_update_prev:
                    nodes_to_update.add(next)

    @property
    def nodes_list(self):
        return self._nodes

    @property
    def regs(self):
        return self._regs
