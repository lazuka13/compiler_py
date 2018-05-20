# coding: utf-8

from source.framework.dot_print import DotPrint

from .variable_graph import VariableGraph


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
        for t in graph.nodes.keys():
            node_to_name[t] = self.add_node(t.name + ' [' + str(t.id) + ']')

        for t, node in graph.nodes.items():
            self.parent_name = node_to_name[t]
            for to in node._connections:
                self.add_arrow(node_to_name[to.reg])
            for to in node._moves:
                self.add_arrow(node_to_name[to.reg], True)

    def print_postfix(self):
        self.print_arrows(False)
        self.dot.write('}\n')
