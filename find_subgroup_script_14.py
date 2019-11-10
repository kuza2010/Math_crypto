import argparse

import Group
from euler_script_5 import euler

from enum import Enum


class OperationType(Enum):
    MULTIPLE = 'multiple'
    ADDITION = 'addition'

    def __str__(self):
        return self.value


def basis_validator(string: str):
    num = int(string)
    if num <= 1:
        raise argparse.ArgumentTypeError(f'Incorrect input: {string}, value must be > 1')
    return num


def create_parser():
    parser = argparse.ArgumentParser(description='''
    About script:
    =========================================
    Math foundations of cryptology.
    Задание 14. Разложение группы на подгруппы и формирование для каждой подгруппы
    смежных классов (для Z*m , Z+m ) ''', formatter_class=argparse.RawDescriptionHelpFormatter)

    parser.add_argument('operation', type=OperationType, choices=list(OperationType),
                        help='- Operation. Choose between: addition or multiple.')
    parser.add_argument('basis', help='- the basis', type=basis_validator)

    argv = parser.parse_args()
    return argv


def get_euler(m):
    return euler(m)[0]


def fill_subgroup(a, n, m, type: OperationType):
    result = []

    for i in range(1, n + 1):
        if type == OperationType.MULTIPLE:
            result.append(int(a ** i % m))
        elif type == OperationType.ADDITION:
            result.append(a * i % m)

    return result


def decompose_multiple_group(m: int):
    subgroups = []
    orders = []

    for a in range(1, m):
        eul = get_euler(m)
        n = 1
        while n <= eul:
            if a ** n % m == 1:
                if n in orders:
                    break
                subgroups.append(Group.Group(a,
                                             fill_subgroup(a, n, m, OperationType.MULTIPLE),
                                             Group.OperationType.MULTIPLE))
                orders.append(n)
                break
            n += 1

    return subgroups


def decompose_addition_group(m: int):
    subgroups = []
    orders = []

    if get_euler(m) == m - 1:
        subgroups.append(Group.Group(1, [0], Group.OperationType.ADDITION))
        subgroups.append(Group.Group(2, list(range(m)), Group.OperationType.ADDITION))
        return subgroups

    for a in range(1, m + 1):
        for n in range(1, m + 1):
            if a * n % m == 0:
                if n in orders:
                    break
                subgroups.append(Group.Group(a,
                                             fill_subgroup(a, n, m, OperationType.ADDITION),
                                             Group.OperationType.ADDITION))
                orders.append(n)
                break

    return subgroups


def decompose_group(m: int, operation: OperationType):
    subgroups = []

    if operation == OperationType.MULTIPLE:
        subgroups = decompose_multiple_group(m)
    else:
        subgroups = decompose_addition_group(m)

    print(f'****Basis m({m})****')
    for sub in subgroups:
        print(sub)
        ajacent = sub.find_adjacent_classes(argv.basis)
        print(f'Adjacent classes:')
        for clazz in ajacent:
            print(clazz)

    return subgroups


if __name__ == '__main__':
    argv = create_parser()

    decompose_group(argv.basis, argv.operation)
