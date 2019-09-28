import inverse_element


class ChineseEquation:

    def __init__(self, b, m, printable_view: str):
        # -1 value is not set
        self.__M = -1
        self.__y = -1
        self.__b = int(b)
        self.__m = int(m)
        self.__view = printable_view

        print(f'Create Chinese equation with param: b={b}, m={m}, {printable_view}')

    @property
    def b(self):
        return int(self.__b)

    @property
    def m(self):
        return int(self.__m)

    @property
    def M(self):
        return int(self.__M)

    @property
    def y(self):
        return int(self.__y)

    @b.setter
    def b(self, value: int):
        self.__b = value

    @m.setter
    def m(self, value: int):
        self.__m = value

    def find_self_m(self, M: int, print_solution: bool = False):
        self.__M = int(M / self.__m)

        if self.m * self.M != M:
            raise RuntimeError(f'Ooops... Set m failed. Self {self.M}!={M}')
        if print_solution:
            print(f'set M = {self.M}')

        self.find_self_y(print_solution)

    def find_self_y(self, print_solution: bool = False):
        self.__y = inverse_element.get_inverse_of(self.m, self.M)
        if print_solution:
            print(f'set y = {self.y}')

    def __str__(self):
        return f'{self.__view}  M={self.M}, y= {self.y}'
