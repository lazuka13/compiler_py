LABEL_PREFIX = 'label_'


class Label:
    Map = dict()

    def __init__(self, name):
        self.name = name

    @staticmethod
    def get_label(name):
        found = Label.Map.get(name)
        if found is None:
            label = Label(name)
            Label.Map[name] = label
            print('uuu label', type(label))
            return label
        else:
            print('uuu found', type(found))
            return found

    @staticmethod
    def get_next_enumerated_label():
        id = 0
        while LABEL_PREFIX + str(id) in Label.Map:
            id += 1
        label_name = LABEL_PREFIX + str(id)
        id += 1
        print('uuu label_name', type(label_name))
        return Label.get_label(label_name)
