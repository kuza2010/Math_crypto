if __name__ == 'main':
    from subtract_class import getSubtractClassFor
    from euler import getEuler
else:
    from utils.subtract_class import getSubtractClassFor
    from utils.euler import euler


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
            euler = euler(m)[0]
            u = each ** (euler - 1)
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
            euler = euler(m)[0]
            u = each ** (euler - 1)
            answ[a] = u % m

    # return dictionary [K:V],
    #   K - a
    #   V - u
    return answ


def get_inverse_of(m: int, a: int):
    subtract = getSubtractClassFor(m)
    if a > m:
        a = a % m

    # SKIP 1?
    for each in subtract:
        if a == each:
            euler = euler(m)[0]
            u = each ** (euler - 1)
            return u % m


if __name__ == '__main__':
    print(f'U(7):\n{("".join(getPrettyStr(getAllInverseOf(7))))}')
    print(f'U(9):\n{("".join(getPrettyStr(getAllInverseOf(9))))}')
    print(f'U(5):\n{("".join(getPrettyStr(getAllInverseOf(5))))}')
    print(f'U(5):\n{("".join(getPrettyStr(getInverseOf(5, 3))))}')
    print(f'U(5):\n{("".join(getPrettyStr(getInverseOf(5, 2))))}')
    print(f'U(7):\n{("".join(getPrettyStr(getInverseOf(7, 143))))}')
    print(f'{get_inverse_of(13, -1)}')
