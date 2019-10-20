import argparse
from utils import euler
from utils import nod
from utils import canonic_view
import itertools


def validate(string: str):
    value = int(string)
    if value <= 0:
        raise argparse.ArgumentTypeError(f'Incorrect value: {string}')
    return value


def get_parser():
    parser = argparse.ArgumentParser(description='''
    About script:
    =========================================
    Math foundations of cryptology. Script #10.
    Нахождение первообразного корня (образующего элемента) и формирование с его
    помощью приведенной системы вычетов 

    Пример:
        Ввод: 11 
        Вывод: первообразный корень по модулю 11: a = 2''', formatter_class=argparse.RawDescriptionHelpFormatter)

    parser.add_argument('module', type=validate, nargs=1,
                        help='- module, positive number.')
    parser.add_argument('-s', '--solution', type=bool, const=True, default=False, nargs='?',
                        help='- print solution')
    args = parser.parse_args()
    return args


def get_all_degree(numbers: []):
    degrees = set(numbers)

    if len(numbers) > 2:
        for length in range(2, len(numbers)):
            for combination in itertools.combinations(numbers, length):
                degree = 1
                for each in combination:
                    degree *= each
                degrees.add(degree)

    return list(degrees)


def find_root_and_system(m: int, print_solution: bool):
    eul = euler.euler(m)[0]
    canonic_number = canonic_view.to_list_prime(canonic_view.prime_factors_list(eul))
    if print_solution:
        print(f'Euler: φ({m}) = {eul}')
        print(f'Canon view: {eul} = {canonic_view.pretty_str(canonic_view.prime_factors_list(eul))}')

    a = 2
    while a < eul:
        isRoot = True
        for each in canonic_number:
            if isRoot:
                degree = int(eul / each)
                if (a ** degree) % m == 1:
                    isRoot = False
            else:
                break
        if isRoot and nod.get_nod(a, m) == 1:
            system = get_system(a, canonic_view.get_all_prime(m), m)
            return a, system
        a += 1
    return -1, []


def get_system(a: int, degrees: [], m: int):
    system = []
    for degree in degrees:
        system.append(f'{a}^{degree}={int(a ** degree % m)}')
    return system


if __name__ == '__main__':
    args = get_parser()
    root = find_root_and_system(args.module[0], args.solution)
    if root[0] >= 2:
        print(f'Первообразный корень по модулю {args.module[0]}: a = {root[0]}')
        print(f'Приведенной системы вычетов: {", ".join(root[1])}')
    else:
        print(f'Первообразных корней по модулю {args.module[0]} не найдено')
