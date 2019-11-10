from subtract_class import getSubtractClassFor
from euler_script_5 import euler

'''
Задание 6. Нахождение обратного элемента в Zm
'''


# By euler theorem`s
#
# U = A^(F(m)-1),
#   F(m) - Euler function

def getPrettyStr(dic: dict):
    str = []
    for key in dic:
        str.append(f'a={key}     u={dic[key]}\n')

    return str


def getAllInverseOf(m: int):
    answ = {}
    subtract = getSubtractClassFor(m)

    # SKIP 1?
    for each in subtract:
        if each == 1:
            answ[1] = 1
        else:
            tmp_euler = euler(m)[0]
            u = each ** (tmp_euler - 1)
            answ[each] = u % m

    # return dictionary [K:V],
    #   K - a
    #   V - u
    return answ


def getInverseOf(m: int, a: int):
    answ = {}
    subtract = getSubtractClassFor(m)
    if abs(a) > m:
        a = a % m

    # SKIP 1?
    for each in subtract:
        if a == each or (a < 0 and a + m == each):
            tmp_euler = euler(m)[0]
            u = each ** (tmp_euler - 1)
            answ[a] = u % m

    # return dictionary [K:V],
    #   K - a
    #   V - u
    return answ


def get_inverse_of(m: int, a: int):
    subtract = getSubtractClassFor(m)
    if a > m:
        a = a % m

    if a == 0:
        raise ValueError(f'Can not find inverse element for {a} by m = {m}')

    # SKIP 1?
    for each in subtract:
        if a == each:
            tmp_euler = euler(m)[0]
            u = each ** (tmp_euler - 1)
            return u % m


if __name__ == '__main__':
    print(get_inverse_of(11, 5))
    print(get_inverse_of(11, 3))
    print(get_inverse_of(5, 5))
