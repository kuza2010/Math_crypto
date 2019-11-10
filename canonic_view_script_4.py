import argparse
import vilson_script_3
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
    Math foundations of cryptology. Задание #4.
    Каноническое разложение числа на простые множители.
    Пример: 
        input: 21 
        output: CanonicView: 21 = (3^1)*(7^1)''', formatter_class=argparse.RawDescriptionHelpFormatter)

    parser.add_argument('number', type=validate, nargs=1, help='- integer digit')

    args = parser.parse_args()
    return args


def to_list_prime(prime_dict: dict):
    primes = []
    for key in prime_dict.keys():
        for value in range(prime_dict[key]):  # num of entries
            primes.append(key)

    return primes


def prime_factors_list(n):
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


def get_all_prime(m: int):
    if vilson_script_3.isPrimary(m):
        return range(m)
    else:
        return vilson_script_3.get_all_primary(m, True)


def pretty_str(prim: dict):
    # key - number, value - degree
    factors = list(map(lambda each: f'({each}^{prim[each]})', prim.keys()))
    resultStr = '*'.join(factors)
    return resultStr


if __name__ == '__main__':
    print(f'selfcheck......')
    test_data = [21, 13, 111, 283]
    for each in test_data:
        prim = prime_factors_list(each)
        print(f'CanonicView: {each} = {pretty_str(prim)}')
    print(f'selfcheck completed')
