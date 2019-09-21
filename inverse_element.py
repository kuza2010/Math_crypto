from subtract_class import getSubtractClassFor
from euler import getEuler


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
            euler = getEuler(m)[0]
            u = each ** (euler - 1)
            answ[each] = u % m

    # retur dictionary [K:V],
    #   K - a
    #   V - u
    return answ


if __name__ == '__main__':
    print(f'U(7):\n{("".join(getPrettyStr(getAllInverseOf(7))))}')
    print(f'U(9):\n{("".join(getPrettyStr(getAllInverseOf(9))))}')