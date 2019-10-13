import argparse
from utils import euler
from utils import nod
from utils import canonic_view


def validate(string: str):
    value = int(string)
    if value <= 0:
        raise argparse.ArgumentTypeError(f'Incorrect value: {string}')
    return value


def getParser():
    parser = argparse.ArgumentParser(description='''
    About script:
    =========================================
    Math foundations of cryptology. Script #10.
    Нахождение первообразного корня (образующего элемента) и формирование с его
    помощью приведенной системы вычетов 

    Пример:
        Ввод: 11 
        Вывод: первообразный корень mod(11) => a=[2, 6, 7, 8]''', formatter_class=argparse.RawDescriptionHelpFormatter)

    parser.add_argument('module', type=validate, nargs=1,
                        help='- module, positive number.')
    parser.add_argument('-s', '--solution', type=bool, const=True, default=False, nargs='?',
                        help='- print solution')
    args = parser.parse_args()
    return args


def findFirstRoot(m: int, print_solution: bool):
    eul = euler.getEuler(m)
    canonic_number = canonic_view.getPrimeFactorsList(eul[0]).keys()
    if print_solution:
        print(f'Euler: φ({m}) = {eul[0]}')
        print(f'Canon view: {eul[0]} = {canonic_view.getPrettyStr(canonic_view.getPrimeFactorsList(eul[0]))}')

    roots = []
    a = 2
    while a < eul[0]:
        isRoot = True
        for each in canonic_number:
            if isRoot:
                degree = int(eul[0] / each)
                if (a ** degree) % m == 1:
                    isRoot = False
            else:
                break
        if isRoot and nod.getNod(a, m) == 1:
            roots.append(a)
        a += 1

    return roots


if __name__ == '__main__':
    argParser = getParser()
    print(f'a = {findFirstRoot(argParser.module[0], argParser.solution)}')
