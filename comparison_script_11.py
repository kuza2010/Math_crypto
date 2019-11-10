import argparse
import re

from nod_script_1_2 import get_nod
from euler_script_5 import euler as get_euler
from root_script_10 import find_root_and_system
from inverse_element_script_6 import get_inverse_of
from enum import Enum

i_regexp = "[1-9][0-9]*x\^[1-9][0-9]*=[1-9][0-9]*\(mod[1-9][0-9]*\)"
d_regexp = "[1-9][0-9]*\^x=[1-9][0-9]*\(mod[1-9][0-9]*\)"


class OperationType(Enum):
    INDICATIVE = 'multiple'
    DEGREE = 'addition'


def validate(template: str, type: OperationType):
    print(type)
    result = None

    if type == OperationType.DEGREE:
        result = re.search(d_regexp, template)
    elif type == OperationType.INDICATIVE:
        result = re.search(i_regexp, template)

    if result is None:
        raise RuntimeError('Invalid input!')

    return result.group(0)


def create_parser():
    parser = argparse.ArgumentParser(description='''
    About script:
    =========================================
    Math foundations of cryptology. Задание #11.
    Решение степенного (показательного) сравнения

    Пример: 
        ''', formatter_class=argparse.RawDescriptionHelpFormatter)

    parser.add_argument('equation', type=str, help='- equation')
    parser.add_argument('-i', '--indicative', const=True, type=bool, default=False, nargs='?',
                        help='- as indicative equation')
    parser.add_argument('-d', '--degree', const=True, type=bool, default=False, nargs='?',
                        help='- as degree equation')

    args = parser.parse_args()
    return args


def is_solution_possible(m: int, d: int):
    return not m % d != 0


def get_param(equation: str, type: OperationType) -> {}:
    params = {}
    nums = re.findall(r'[1-9][0-9]*', equation)

    if type == OperationType.INDICATIVE:
        params.update({'b': int(nums[0])})
        params.update({'a': int(nums[2])})
        params.update({'m': int(nums[3])})
        params.update({'l': int(nums[1])})  # l - lambda
    elif type == OperationType.DEGREE:
        params.update({'b': int(nums[0])})
        params.update({'a': int(nums[1])})
        params.update({'m': int(nums[2])})

    return params


def get_index_for(m: int, a: int):
    i = 0
    root_for_m = find_root_and_system(m, False)[0]

    if root_for_m == -1:
        raise RuntimeError(f'Can not find index for {m}, because root not found')

    while i < m:
        if root_for_m ** i % m == a:
            return i
        i += 1

    raise RuntimeError(f'Can not find index for {m}')


def resolve(equation: str, type: OperationType):
    print(f'input: {equation} type {type}')

    params = get_param(equation, type)
    if type == OperationType.INDICATIVE:
        return resolve_indication(params['a'], params['b'], params['l'], params['m'])
    elif type == OperationType.DEGREE:
        return resolve_degrees(params['a'], params['b'], params['m'])


# b*x^l = a*(mod m)
def resolve_indication(a, b, l, m):
    # find inverse and recount a
    if get_inverse_of(m, b) is None:
        raise RuntimeError('No solution!')
    a = int(a * get_inverse_of(m, b) % m)

    # find index and recount a
    a = index = get_index_for(m, a)

    # find betta as euler(m)
    betta = get_euler(m)[0]

    # check possible
    nod = get_nod(l, betta)
    if not is_solution_possible(index, nod):
        raise RuntimeError("No solution, because (d,index) !=0")

    # cut the equation
    m = int(betta / nod)
    a = int(a / nod)
    b = int(b / nod)
    l = int(l / nod)

    # final cut
    b = int(b * get_inverse_of(m, a) % m)

    print(f'x = {find_root_and_system(m, False)[0]}^({b} + {m}k)')

    return None

# b^x = a*(mod m)
def resolve_degrees(a, b, m):
    a = int(get_index_for(m, a))
    b = int(get_index_for(m, b))

    if a == 0 or b == 0:
        raise RuntimeError('No solution!')

    # find betta as euler(m)
    betta = get_euler(m)[0]

    # check possible
    nod = get_nod(b, betta)
    if not is_solution_possible(a, nod):
        raise RuntimeError("No solution, because (a,index) !=0")

    a = int(a / nod)
    b = int(b / nod)
    m = int(betta / nod)

    # final cut
    a = int(a * get_inverse_of(m, b) % m)

    print(f'x = {a} + {m}k ')


if __name__ == '__main__':
    argv = create_parser()
    equation = validate(argv.equation, OperationType.INDICATIVE if argv.indicative else OperationType.DEGREE)
    resolve(equation, OperationType.INDICATIVE if argv.indicative else OperationType.DEGREE)
