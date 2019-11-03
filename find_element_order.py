#!/usr/bin/python3
from enum import Enum
from functools import reduce
from vilson import isPrimary
from nod import get_nod

import argparse
import euler
import canonic_view

"""
Порядок элемента в группе.
Это наименьшее натуральное число n, такое, что: a^n=e.

^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
^                   З А Д А Н И Е                     ^
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Задание 13. Нахождение порядка всех элементов в группе:
1)Z по основанию m (+);
2)Z по основанию m (*)
"""


class OperationType(Enum):
    MULTIPLE = 'multiple'
    ADDITION = 'addition'

    def __str__(self):
        return self.value


def basis_validator(string: str):
    num = int(string)
    if num <= 2:
        raise argparse.ArgumentTypeError(f'Incorrect input: {string}, value must be > 2')
    return num


def create_parser():
    parser = argparse.ArgumentParser(description='''
    About script:
    =========================================
    Math foundations of cryptology.
    Задание 13. Нахождение порядка всех элементов в группе. ''', formatter_class=argparse.RawDescriptionHelpFormatter)

    parser.add_argument('operation', type=OperationType, choices=list(OperationType),
                        help='- Operation. Choose between: addition or multiple.')
    parser.add_argument('basis', help='- the basis', type=basis_validator)
    parser.add_argument('-s', '--solution', type=bool, const=True, default=False, nargs='?',
                        help='- print solution')
    argv = parser.parse_args()
    return argv


def find_elem_order(basis: int, op_type: OperationType, print_solution: bool) -> []:
    if op_type == OperationType.MULTIPLE:
        return order_multiple_group(basis)
    else:
        return order_addition_group(basis)


def order_multiple_group(m: int):
    eul = euler.euler(m)[0]
    canon = canonic_view.prime_factors_list(eul)
    elem_basis = []

    # find order for each elem
    for a in range(1, m):
        ri = []
        # bypass prime list
        for prime_elem in canon.keys():
            w = canon[prime_elem]  # get max W
            for wi in reversed(range(w + 1)):
                if (a ** ((m - 1) / (prime_elem ** wi))) % m == 1 or wi == 0:
                    ri.append(prime_elem ** (w - wi))
                    break

        elem_basis.append(f'ord{a}:={reduce(lambda x, y: x * y, ri)}')

    return elem_basis


def order_addition_group(m: int):
    elem_basis = []

    if isPrimary(m):
        return list(map(lambda a: f'ord{a}={m}', range(m)))

    for a in range(m):
        if get_nod(a, m) == 1:
            elem_basis.append(f'ord{a}={m}')
        else:
            for k in range(1, m):
                if a * k % m == 0:
                    elem_basis.append(f'ord{a}={k}')
                    break

    return elem_basis


if __name__ == '__main__':
    args = create_parser()
    orders = find_elem_order(args.basis, args.operation, args.solution)
    print(orders)
