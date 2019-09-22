import argparse
import re
import nod
import inverse_element

equationPattern = r'([1-9]+)x=([1-9]+)\(mod([2-9]+)\)'


def validate(string: str):
    result = re.search(equationPattern, string)
    if result is not None:
        return string
    else:
        raise argparse.ArgumentTypeError(f'Incorrect input: {string}')


def getParser():
    parser = argparse.ArgumentParser(description='''
    About script:
    =========================================
    Math foundations of cryptology. Script #4.
    Simple comparison, where (a,b)=1

    Example:
        input: "3x=1(mod5)" 
        output: 3x=1(mod5) => x = 2+5k, k ∈ Z''', formatter_class=argparse.RawDescriptionHelpFormatter)

    parser.add_argument('equation', type=validate, nargs=1,
                        help='- equation. You can input the equation without space.')
    parser.add_argument('-s', '--solution', type=bool, const=True, default=False, nargs='?',
                        help='- print solution')
    args = parser.parse_args()
    return args


# This func compress and return list param.
# Input - the equation.
#   Return:
#       param[0] - a
#       param[1] - b
#       param[2] - m
def getParams(equation: str, printSolution: bool):
    answ = []

    # get first num: 23x=42(mod5) => 23
    result = re.match(r'([1-9]+)', equation)
    if result.group(0) is None:
        raise RuntimeError(f'Ooops... Can not find first number')
    else:
        answ.append(int(result.group(0)))

    # get second num: 23x=42(mod5) => 42
    tmp = re.search(r'=([1-9]+)\(', equation)
    if result is None:
        raise RuntimeError(f'Ooops... Can not find second number')
    else:
        result = re.search(r'([1-9]+)', tmp.group(0))
        answ.append(int(result.group(0)))

    # get the third num: 23x=42(mod5) => 5
    tmp = re.search(r'mod([2-9]+)', equation)
    if result is None:
        raise RuntimeError(f'Ooops... Can not find third number')
    else:
        result = re.search(r'([2-9]+)', tmp.group(0))
        answ.append(int(result.group(0)))

    return short(answ[0], answ[1], answ[2], printSolution)


def short(a, b, m, printSolution: bool):
    # 74x=69(mod7) => 4x=6(mod7)
    if a > m and b > m:
        if printSolution:
            print(f'{argParser.equation[0]}\n{a % m}x={b % m}(mod{m})')
        a = a % m
        b = b % m

    return a, b, m


def getX(a, b, m, printSolution: bool):
    one = inverse_element.getInverseOf(m, a)
    two = inverse_element.getInverseOf(m, b)
    if printSolution:
        print(f'x={one[a] * two[b]}mod({m})')
        print(f'x={(one[a] * two[b]) % m}')

    return (one[a] * two[b]) % m


# This func return the answer for the equation.
# Parameter should be reduced!
def getAnswer(params: [], printSolution: bool):
    x = getX(params[0], params[1], params[2], printSolution)
    if printSolution:
        print(f'x = {x}+{params[2]}k, k ∈ Z')
    return x


# This func return the answer for the equation.
# Parameter:
#   strEquation - the equation
def getAnswerFromString(strEquation: str, printSolution: bool):
    param = getParams(strEquation, printSolution)
    return getAnswer(param, argParser.solution)


if __name__ == '__main__':
    argParser = getParser()

    if argParser.solution:
        print(f'Equation: {argParser.equation[0]}')
    print(f'X={getAnswerFromString(argParser.equation[0], argParser.solution)}')
