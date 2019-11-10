import argparse
import re
import nod_script_1_2
from chinese_equation import ChineseEquation

equationPattern = r'x=[1-9][0-9]*\(mod[1-9][0-9]*\)'


def validate(string: str):
    for equation in string.split(';'):
        result = re.search(equationPattern, equation)
        if result is None:
            raise argparse.ArgumentTypeError(f'Incorrect input: {equation} in the system of equations: {string}')
    return string


def get_parser():
    parser = argparse.ArgumentParser(description='''
    About script:
    =========================================
    Math foundations of cryptology.
    Задание 8. Решение системы сравнений китайским алгоритмом

    Example:
        input: "3x=1(mod5)" 
        output: 3x=1(mod5) => x = 2+5k, k ∈ Z''', formatter_class=argparse.RawDescriptionHelpFormatter)

    parser.add_argument('equation', type=validate, nargs=1,
                        help='- equation. You can input the equation without space.')
    parser.add_argument('-s', '--solution', type=bool, const=True, default=False, nargs='?',
                        help='- print solution')
    args = parser.parse_args()
    return args


def print_equation(equation: str):
    result = ''
    for equation in equation.split(';'):
        result += f'\t[{equation}\n'

    print(f'The equation:\n{result}')


def get_params(equation_str: str):
    equations = []
    # get parameters
    for equation_str in equation_str.split(';'):
        b = 0
        m = 0
        tmp_b = re.search(r'=[1-9][0-9]*\(', equation_str)
        tmp_m = re.search(r'mod[1-9][0-9]*', equation_str)

        # get parameter - b
        if tmp_b is None:
            raise RuntimeError(f'Ooops... Can not find parameter b.')
        else:
            b = tmp_b.group(0)[1:-1]

        # get parameter - m
        if tmp_m is None:
            raise RuntimeError(f'Ooops... Can not find parameter m.')
        else:
            m = tmp_m.group(0)[3:]
        equations.append(ChineseEquation(b, m, equation_str))

    # validate nod
    for i in range(len(equations) - 1):
        nod_m1_m2 = nod_script_1_2.get_nod(equations[i].m, equations[i + 1].m)
        if nod_m1_m2 != 1:
            raise RuntimeError(f'Ooops... Equation has no solution because nod('
                               f'{equations[i].m},{equations[i + 1].m}) = {nod_m1_m2}.')

    return equations


def get_M(chinese_list: list, print_solution: bool = False):
    M = 1
    for equation in chinese_list:
        M = M * equation.m
    for equation in chinese_list:
        equation.find_self_m(M, print_solution)

    if print_solution:
        print(f'M = {M}')

    return M


def getAnswerFromString(str_equation: str, print_solution: bool):
    X = 0

    param = get_params(str_equation)
    M = get_M(param, print_solution)

    for each in param:
        X += each.y * each.M * each.b

    if print_solution:
        print(f'X = {X % M} + {M}K, k ∈ Z')

    return X % M, M


if __name__ == '__main__':
    argParser = get_parser()

    if argParser.solution:
        print_equation(argParser.equation[0])
    answ = getAnswerFromString(argParser.equation[0], argParser.solution)
    print(f'X={answ[0]} + {answ[1]}K, k ∈ z')
