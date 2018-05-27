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

    def add_node(self, label, color=None):
        name = "name" + str(self.node_counter)
        if color is None:
            self.dot.write('"{name}" [\nlabel = "{label}"\nshape = "record"\n];\n'.format(name=name, label=label))
        else:
            self.dot.write('"{name}" [\nlabel = "{label}"\nshape = "circle"\ncolor = "{color}" style="filled"];\n'.format(
                name=name, label=label, color=color
            ))
        self.node_counter += 1
        return name

    def print_arrows(self, direct=True):
        for i, arrow in enumerate(self.arrows):
            self.dot.write(arrow._from)
            self.dot.write((' -> ' if direct else ' -- '))
            self.dot.write(arrow._to)
            self.dot.write(
                '[ \n' + ('style=dashed ' if arrow._dashed else '') + 'id = ' + str(i) + '\npenwidth=4.0\n];\n'
            )
