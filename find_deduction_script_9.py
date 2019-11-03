import argparse
import re
import canonic_view
import chinese_system

'''
Задание #9. Нахождение вычета a^k(mod m) для простого и составного m
'''

regex = '^[1-9][0-9]*\^[1-9][0-9]*\(mod[1-9][0-9]*\)'
eq_template = "{}(mod{})={}"
eq_template_final = "x={}(mod{})"


def validate(string: str):
    result = re.search(regex, string)
    if result is None:
        raise argparse.ArgumentTypeError(f'Incorrect input: {string}')

    return string


def get_parser():
    parser = argparse.ArgumentParser(description='''
    About script:
    =========================================
    Math foundations of cryptology.
    Задание 9. Нахождение вычета a^k(mod m) для простого и составного m

    Пример:
        input: "2^6754(mod1155)" 
        output: 2^6754(mod1155) = 709 + 1155, k ∈ Z''', formatter_class=argparse.RawDescriptionHelpFormatter)

    parser.add_argument('equation', type=validate, nargs=1,
                        help='- equation. You can input the equation without space.')
    parser.add_argument('-s', '--solution', type=bool, const=True, default=False, nargs='?',
                        help='- print solution')
    args = parser.parse_args()
    return args


def get_param(equation_str: str):
    param = re.findall("[1-9][0-9]*", equation_str)
    return int(param[0]), int(param[1]), int(param[2])


def find_deduction(equation: str, print_solution: bool):
    # 0-a, 1-k, 2-p
    params = get_param(equation)
    a = params[0]
    k = params[1]
    p = params[2]

    primes = canonic_view.prime_factors_list(p)
    system = []

    for prime in primes.keys():
        if print_solution:
            print('[' + eq_template.format(k, prime - 1, k % (prime - 1)))

    for prime in primes.keys():
        tmp_a = a ** (k % (prime - 1)) % prime
        system.append(eq_template_final.format(tmp_a, prime))
        if print_solution:
            print('[' + eq_template_final.format(tmp_a, prime))

    return chinese_system.getAnswerFromString(';'.join(system), print_solution)


if __name__ == '__main__':
    argv = get_parser()
    answ = find_deduction(argv.equation[0], argv.solution)
    print(f'X={answ[0]} + {answ[1]}K, k ∈ z')
