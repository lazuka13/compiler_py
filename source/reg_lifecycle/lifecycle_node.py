# coding: utf-8

from source.code_generation.instruction import IInstruction, MoveInstruction


class LifecycleNode(object):
    def __init__(self, instruction: IInstruction, used: list, defined: list):
        self._instruction = instruction
        self._is_move = False
        self._used = set(used)
        self._defined = set(defined)
        self._next = []
        self._prev = []
        self._in = set()
        self._out = set()
        if isinstance(instruction, MoveInstruction) and instruction.dst:
            self._is_move = instruction.pure_move()

    @property
    def instruction(self):
        return self._instruction

    @property
    def out(self):
        return self._out

    @property
    def next(self):
        return self._next

    @property
    def prev(self):
        return self._prev

    def update(self):
        inserted = False
        for t in self._used:
            inserted |= (t not in self._in)
            self._in.add(t)
        for out_node in self._next:
            for in_node in out_node._in:
                inserted |= (in_node not in self._out)
                self._out.add(in_node)
        for out_node in self._out:
            if out_node not in self._defined:
                inserted |= (out_node not in self._in)
                self._in.add(out_node)

        return inserted

    def add_connection(self, target: 'LifecycleNode'):
        self._next.append(target)
        target._prev.append(self)

    def format(self):
        return ('move |' if self._is_move else ' |') + self._instruction.format()
