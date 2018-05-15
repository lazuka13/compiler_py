from typing import Dict, List


class CTemp:
    def CTemp(self, src=None):
        if src:
            self.name = src.name
        else:
            name = None

    def __eq__(self, other):
        return self.name == other.name

    def __ne__(self, other):
        return self.name != other.name


class CLabel:
    def CLabel(self, src=None):
        if src:
            self.name = src.name
        else:
            name = None

    def __eq__(self, other):
        return self.name == other.name

    def __ne__(self, other):
        return self.name != other.name


CTempList: List[CTemp] = list
CLabelList: List[CLabel] = list
CTempMap: Dict[CTemp, str] = dict
