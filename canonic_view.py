import argparse
from collections import Counter


def validate(string: str):
    value = int(string)

    if value <= 0:
        raise argparse.ArgumentTypeError(f'Incorrect value: {string}')

    return value


def getParser():
    parser = argparse.ArgumentParser(description='''
    About script:
    =========================================
    Math foundations of cryptology. Script #2.
    Find primary factorial given numbers.

    Simple: 
        42= 2^1 * 3^1 * 7^1''', formatter_class=argparse.RawDescriptionHelpFormatter)

    parser.add_argument('number', type=validate, nargs=1, help='- integer digit')

    args = parser.parse_args()
    return args


def getPrimeFactors(n):
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
    resultStr = ""
    # key - number, value - degree
    for key in prim.keys():
        resultStr = f'{resultStr}({key}^{prim[key]})*'

    return resultStr


if __name__ == '__main__':
    argParser = getParser()
    prim = getPrimeFactors(argParser.number[0])
    print(f'CanonicView: {argParser.number[0]} = {getPrettyStr(prim)[:-1]}')
