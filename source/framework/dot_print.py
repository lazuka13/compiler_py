# coding: utf-8


class DotPrint(object):
    class Arrow(object):
        def __init__(self, _from, _to, dashed):
            self._from = _from
            self._to = _to
            self._dashed = dashed

    def __init__(self, filename):
        self.arrows = []
        self.dot = open(filename, 'w')
        self.parent_name = None
        self.node_counter = 0

    def add_arrow(self, name, dashed=False):
        self.arrows.append(self.Arrow('"' + self.parent_name + '"', '"' + name + '"', dashed))

    def add_node(self, label):
        name = "name" + str(self.node_counter)
        self.dot.write('"{name}" [\nlabel = "<f0> {label}"\nshape = "record"\n];\n'.format(name=name, label=label))
        self.node_counter += 1
        return name

    def print_arrows(self, direct=True):
        for i in range(len(self.arrows)):
            arrow = self.arrows[i]
            self.dot.write(arrow._from)
            self.dot.write((' -> ' if direct else ' -- '))
            self.dot.write(arrow._to)
            self.dot.write('[ \n' + ('style=dashed ' if arrow._dashed else '') + 'id = ' + str(i) + '\n];\n')
