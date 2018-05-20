# coding: utf-8

from source.framework.dot_print import DotPrint

from .lifecycle_node import LifecycleNode


class LifecyclePrinter(DotPrint):
    def __init__(self, name):
        super().__init__(name)

    def print_prefix(self):
        self.dot.write(
            '''digraph g {
graph [ rankdir = TD ];
node [
fontsize = "16"
shape = "ellipse"
];
edge [
];'''
        )

    def print(self, nodes: [LifecycleNode]):
        node_to_name = {}
        for node in nodes:
            name = self.add_node(node.format())
            node_to_name[node] = name
        for node in nodes:
            self.parent_name = node_to_name[node]
            for to in node.next:
                self.add_arrow(node_to_name[to])

    def print_postfix(self):
        self.print_arrows()
        self.dot.write('}')
