# coding: utf-8

from source.framework.dot_print import DotPrint

from .variable_graph import VariableGraph


COLORS = [
    "red",
    "blue",
    "deeppink",
    "indigo",
]


class VariableGraphPrinter(DotPrint):
    def __init__(self, filename):
        super().__init__(filename)

    def print_prefix(self):
        self.dot.write(
            '''strict graph g {
graph [ rankdir = TD ];
node [
fontsize = "16"
shape = "ellipse"
];
edge [
];
'''
        )

    def print(self, graph: VariableGraph):
        node_to_name = {}
        for t, node in graph.nodes.items():
            node_color = 'black'
            if 0 <= node.color and node.color < len(COLORS):
                node_color = COLORS[node.color]
            node_to_name[t] = self.add_node(t.name + ' [' + str(t.id) + ']', node_color)

        for t, node in graph.nodes.items():
            self.parent_name = node_to_name[t]
            for to in node.connections:
                self.add_arrow(node_to_name[to.reg])
            for to in node._moves:
                self.add_arrow(node_to_name[to.reg], True)

    def print_postfix(self):
        self.print_arrows(False)
        self.dot.write('}\n')
