# coding: utf-8

from x86.x86_instruction_set import RegMove, MoveInstruction

from .lifecycle_graph import LifecycleGraph


class VariableGraph(object):
    class Node(object):
        def __init__(self, temp):
            self._temp = temp
            self._connections = set()
            self._moves = set()

        def add_connection(self, _with):
            if _with == self:
                return

            if _with in self._moves:
                self._moves.remove(_with)
                _with._moves.remove(self)

            if _with not in self._connections:
                self._connections.add(_with)
                _with._connections.add(self)

        def add_move(self, _with):
            if _with == self:
                return
            elif _with in self._connections:
                return

            if _with not in self._moves:
                self._moves.add(_with)
                _with.connections.add(self)

        @property
        def reg(self):
            return self._temp

    def __init__(self, graph: LifecycleGraph):
        self._nodes = {t: self.Node(t) for t in graph.regs}
        for node in graph.nodes_list:
            instruction = node.instruction
            outs = node.out
            if isinstance(instruction, MoveInstruction) and instruction.pure_move:
                defined = instruction.dst
                used = instruction.src
                assert len(defined) == 1 and len(used) == 1

                self._nodes[defined[0]].add_move(self._nodes[used[0]])
                for t in outs:
                    if t != used[0]:
                        self._nodes[defined[0]].add_connection(self._nodes[t])
            else:
                for d in instruction.dst:
                    for t in outs:
                        self._nodes[d].add_connection(self._nodes[t])

    @property
    def nodes(self):
        return self._nodes
