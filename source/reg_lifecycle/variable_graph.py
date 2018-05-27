# coding: utf-8

from x86.x86_instruction_set import MoveInstruction, Temp

from .lifecycle_graph import LifecycleGraph


class VariableGraph(object):
    class INode(object):
        def __init__(self):
            self.color = None
            self.connections = set()
            self.moves = set()

        def just_add_connection(self, _with: 'INode'):
            self.connections.add(_with)

        def just_add_move(self, _with: 'INode'):
            self.moves.add(_with)

        def just_remove_connection(self, _with: 'INode'):
            if _with in self.connections:
                self.connections.remove(_with)

        def just_remove_move(self, _with: 'INode'):
            if _with in self.moves:
                self.moves.remove(_with)

        def set_color(self, color: int):
            pass

    class Node(INode):
        def __init__(self, temp):
            super().__init__()
            self._temp = temp
            self.color = -3
            self.connections = set()
            self._moves = set()

        def set_color(self, color: int):
            self.color = color

        def add_connection(self, _with):
            if _with == self:
                return

            if _with in self._moves:
                self._moves.remove(_with)
                _with._moves.remove(self)

            if _with not in self.connections:
                self.connections.add(_with)
                _with.connections.add(self)

        def add_move(self, _with):
            self.add_connection(_with)

        @property
        def reg(self):
            return self._temp

    class MergedNode(INode):
        def __init__(self, a: 'INode', b: 'INode'):
            super().__init__()
            self.left = a
            self.right = b
            self.color = -3

            for node in a.connections:
                assert node != b
                self.just_add_connection(node)
                node.just_remove_connection(a)
                node.just_add_connection(self)

            for node in b.connections:
                assert node != a
                self.just_add_connection(node)
                node.just_remove_connection(b)
                node.just_add_connection(self)

            for node in a.moves:
                if node != b:
                    node.just_remove_move(a)
                    if node not in self.connections:
                        self.just_add_move(node)
                        node.just_add_move(self)

            for node in b.moves:
                if node != a:
                    node.just_remove_move(b)
                    if node not in self.connections:
                        self.just_add_move(node)
                        node.just_add_move(self)

        def destroy(self):
            for node in self.connections:
                node.just_remove_connection(self)
            for node in self.moves:
                node.just_remove_move(self)
            for node in self.left.connections:
                node.just_add_connection(self.left)
            for node in self.right.connections:
                node.just_add_connection(self.right)
            for node in self.left.moves:
                node.just_add_move(self.left)
            for node in self.right.moves:
                node.just_add_move(self.right)

        def set_color(self, color: int):
            self.color = color
            self.left.set_color(color)
            self.right.set_color(color)

        @property
        def reg(self):
            assert False

    def __init__(self, graph: LifecycleGraph, fp: Temp):
        self._bad_node = None
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

        self._dynamic_nodes = set(self._nodes.values())

        for key, value in self._nodes.items():
            if key == fp:
                for connected_node in value.connections:
                    connected_node.just_remove_connection(value)
                for connected_node in value.moves:
                    connected_node.just_remove_move(value)
                self._dynamic_nodes.remove(value)
                self._nodes.pop(key)
                break

        colors_number = 4
        nodes_stack = []
        merged_nodes = []
        types = []
        is_simplified = True
        is_merged = True
        is_frozen = True
        is_spilled = True

        while is_simplified or is_merged or is_frozen or is_spilled:
            is_simplified = is_merged = is_frozen = is_spilled = False
            for node in self._dynamic_nodes:
                assert node.color == -3
                for connected_node in node.connections:
                    assert connected_node in self._dynamic_nodes
                for connected_node in node.moves:
                    assert connected_node in self._dynamic_nodes

            erase_nodes = []
            for node in self._dynamic_nodes:
                if node.color == -3 and not node.moves and len(node.connections) < colors_number:
                    node.set_color(-2)
                    nodes_stack.append(node)
                    types.append('s')
                    erase_nodes.append(node)
                    for connected_node in node.connections:
                        connected_node.just_remove_connection(node)
                    is_simplified = True
                    break
            while erase_nodes:
                self._dynamic_nodes.remove(erase_nodes.pop())
            if is_simplified:
                continue

            a = None
            b = None
            for node in self._dynamic_nodes:
                if node.color == -3 and node.moves:
                    a = node
                    for move_node in node.moves:
                        common_connections = set()
                        common_connections.update(node.connections)
                        common_connections.update(node.moves)
                        if len(common_connections) < colors_number:
                            b = move_node
                            break
                    if b is not None:
                        break
            if b is not None:
                is_merged = True
                merged_nodes.append(self.MergedNode(a, b))
                types.append('m')
                merged_nodes[-1].set_color(-3)
                self._dynamic_nodes.remove(a)
                self._dynamic_nodes.remove(b)
                self._dynamic_nodes.add(merged_nodes[-1])
            if is_merged:
                continue

            for node in self._dynamic_nodes:
                if node.color == -3 and len(node.moves) == 1:
                    move_node = node.moves[0]
                    move_node.just_remove_move(node)
                    node.just_add_move(move_node)
                    move_node.just_add_connection(node)
                    node.just_add_connection(move_node)
                    is_frozen = True
                    break
            if is_frozen:
                continue

            erase_nodes = []
            for node in self._dynamic_nodes:
                if node.color == -3 and not node.moves:
                    assert len(node.connections) >= colors_number
                    node.set_color(-1)
                    nodes_stack.append(node)
                    types.append('s')
                    erase_nodes.append(node)
                    for connected_node in node.connections:
                        connected_node.just_remove_connection(node)
                    is_spilled = True
                    break
            while erase_nodes:
                self._dynamic_nodes.remove(erase_nodes.pop())
            if is_spilled:
                continue

        assert not self._dynamic_nodes

        while(types):
            if types[-1] == 's':
                connected_colors = set()
                for connected_node in nodes_stack[-1].connections:
                    connected_node.just_add_connection(nodes_stack[-1])
                    connected_colors.add(connected_node.color)
                color = None
                for color in range(colors_number):
                    if color not in connected_colors:
                        break

                if self._bad_node is None and color >= colors_number:
                    self._bad_node = nodes_stack[-1]

                nodes_stack[-1].set_color(color)
                nodes_stack.pop()
            elif types[-1] == 'm':
                merged_nodes[-1].destroy()
                merged_nodes.pop()
            types.pop()

    @property
    def nodes(self):
        return self._nodes
