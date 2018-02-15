class Type:
    def __init__(self, label):
        self.label = label


class BasicType(Type):
    def __init__(self, label):
        Type.__init__(self, label)


class ClassType(Type):
    def __init__(self, id):
        Type.__init__(self, id.name)
        self.id = id
