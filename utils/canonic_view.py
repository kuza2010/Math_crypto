import argparse
from collections import Counter


def validate(string: str):
    value = int(string)

    if value <= 0:
        raise argparse.ArgumentTypeError(f'Value must be >= 0')

    return value


def getParser():
    parser = argparse.ArgumentParser(description='''
    About script:
    =========================================
    Math foundations of cryptology. Script #2.
    Prime factorization. Разложение простого числа на простые множители.
    Simple: 
        input: 21 
        output: CanonicView: 21 = (3^1)*(7^1)''', formatter_class=argparse.RawDescriptionHelpFormatter)

    parser.add_argument('number', type=validate, nargs=1, help='- integer digit')

    args = parser.parse_args()
    return args


def getPrimeFactorsList(n):
    i = 2
    primfac = []
    while i * i <= n:
        while n % i == 0:
            primfac.append(int(i))
            n = n / i
        i = i + 1
    if n > 1:
        primfac.append(int(n))

    # return dict [K:V] = [number: num of entries]
    return Counter(primfac)


def getPrettyStr(prim: dict):
    # key - number, value - degree
    factors = list(map(lambda each: f'({each}^{prim[each]})', prim.keys()))
    resultStr = '*'.join(factors)
    return resultStr


if __name__ == '__main__':
    print(f'selfcheck......')
    test_data = [21, 13, 111, 283]
    for each in test_data:
        prim = getPrimeFactorsList(each)
        print(f'CanonicView: {each} = {getPrettyStr(prim)}')
    print(f'selfcheck completed')