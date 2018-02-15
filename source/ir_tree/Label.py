LABEL_PREFIX = 'label_'


class Label:
    Map = dict()

    def __init__(self, name):
        self.name = name

    @staticmethod
    def get_label(name):
        found = Label.Map.get(name)
        if found is not None:
            label = Label(name)
            Label.Map[name] = label
            return label
        else:
            return found

    @staticmethod
    def get_next_enumerated_label():
        id = 0
        while LABEL_PREFIX + str(id) in Label.Map:
            id += 1
        label_name = LABEL_PREFIX + str(id)
        id += 1
        return label_name
