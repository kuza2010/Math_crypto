from enum import Enum

from euler_script_5 import euler
from nod_script_1_2 import get_nod


class OperationType(Enum):
    MULTIPLE = 'multiple'
    ADDITION = 'addition'

    def __str__(self):
        return self.value


class Group(object):

    def __init__(self, order: int, elements: [], type: OperationType):
        self.__order = order
        self.__elements = elements
        self.__type = type

    @property
    def order(self):
        return self.__order

    @property
    def elements(self):
        return self.__elements

    @property
    def type(self):
        return self.__type

    def find_adjacent_classes(self, m):
        result = []

        if self.type == OperationType.MULTIPLE:
            count_anjacent_classes = euler(m)[0] / len(self.elements) - 1

            for i in range(1, m):
                if count_anjacent_classes == 0:
                    break

                if get_nod(i, m) != 1 or i in self.elements:
                    continue

                tmp = []
                for each in self.elements:
                    tmp.append(each * i % m)

                count_anjacent_classes -= 1
                result.append(tmp)
        elif self.type == OperationType.ADDITION:
            if euler(m)[0] == m - 1:
                return []

            for i in range(1, int(m / len(self.elements))):
                tmp = []

                for each in self.elements:
                    tmp.append(int((each + i) % m))

                result.append(tmp)

        return result

    def __str__(self) -> str:
        return f'Subgroup: a = {self.order}, subgroup elements is: {self.elements}'
