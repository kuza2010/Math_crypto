import argparse
import canonic_view
import nod

'''
Задание #12. Нахождение символа Лежандра и символа Якоби
'''


def isPrime(a):
    a = int(a)
    return all(a % i for i in range(2, a))


def factorize(n):
    factors = []

    p = 2
    while True:
        while n % p == 0 and n > 0:  # while we can divide by smaller number, do so
            factors.append(p)
            n = n / p
        p += 1  # p is not necessary prime, but n%p == 0 only for prime numbers
        if p > n / p:
            break
    if n > 1:
        factors.append(n)
    return factors


def calculateLegendre(a, p):
    """
    Calculate the legendre symbol (a, p) with p is prime.
    The result is either -1, 0 or 1

    >>> calculateLegendre(3, 29)
    -1
    >>> calculateLegendre(111, 41) # Beispiel aus dem Skript, S. 114
    -1
    >>> calculateLegendre(113, 41) # Beispiel aus dem Skript, S. 114
    1
    >>> calculateLegendre(2, 31)
    1
    >>> calculateLegendre(5, 31)
    1
    >>> calculateLegendre(150, 1009)
    1
    >>> calculateLegendre(25, 1009)
    1
    >>> calculateLegendre(2, 1009)
    1
    >>> calculateLegendre(3, 1009)
    1
    """
    if a >= p or a < 0:
        return calculateLegendre(a % p, p)
    elif a == 0 or a == 1:
        return a
    elif a == 2:
        if p % 8 == 1 or p % 8 == 7:
            return 1
        else:
            return -1
    elif a == p - 1:
        if p % 4 == 1:
            return 1
        else:
            return -1
    elif not isPrime(a):
        factors = factorize(a)
        product = 1
        for pi in factors:
            product *= calculateLegendre(pi, p)
        return product
    else:
        if ((p - 1) / 2) % 2 == 0 or ((a - 1) / 2) % 2 == 0:
            return calculateLegendre(p, a)
        else:
            return (-1) * calculateLegendre(p, a)


def calculateJacobi(a, m):
    if m % 2 == 0:
        raise ArithmeticError(f'input: {m} is even number!')
    if nod.get_nod(a, m) != 1:
        raise ArithmeticError(f'nod({a},{m})={nod.get_nod(a, m)}')

    canonic = list(canonic_view.prime_factors_list(m).keys())
    legendre = [calculateLegendre(a, each) for each in canonic]
    res = 1
    for each in legendre:
        res *= each
    return res


def validate(string: str):
    value = int(string)
    return value


def getParser():
    parser = argparse.ArgumentParser(description='''
    About script:
    =========================================
    Math foundations of cryptology. Script #12.1.
    Нахождение символа Лежандра, Якоби.
    Пример:
        Ввод: 126 53 --legendre
        Ввод: 125 53 --jacobi
        Вывод: -1''', formatter_class=argparse.RawDescriptionHelpFormatter)

    parser.add_argument('number', type=validate, nargs=2,
                        help='- two numbers: -126,53')
    parser.add_argument('-l', '--legendre', type=bool, const=True, default=False, nargs='?',
                        help='- find legendre symbol')
    parser.add_argument('-j', '--jacobi', type=bool, const=True, default=False, nargs='?',
                        help='- find jacobi or legendre symbol')
    args = parser.parse_args()
    return args


if __name__ == "__main__":
    argParser = getParser()

    if argParser.legendre:
        print(f'Legendre symbol {argParser.number[0], argParser.number[1]}='
              f'{calculateLegendre(argParser.number[0], argParser.number[1])}')
    elif argParser.jacobi:
        print(f'Jacobi symbol {argParser.number[0], argParser.number[1]}='
              f'{calculateJacobi(argParser.number[0], argParser.number[1])}')
