def nod(a: int, b: int):
    while a != 0 and b != 0:
        if a > b:
            a %= b
        else:
            b %= a

    gcd = a + b
    return gcd


def getSubtractClassFor(num: int):
    lists = []

    for each in range(1, num):
        if nod(each, num) == 1:
            lists.append(each)

    return lists


if __name__ == '__main__':
    # selfcheck
    print(f'7 = {getSubtractClassFor(7)}')
    print(f'9 = {getSubtractClassFor(9)}')
    print(f'6 = {getSubtractClassFor(6)}')
    print(f'42 = {getSubtractClassFor(42)}')
