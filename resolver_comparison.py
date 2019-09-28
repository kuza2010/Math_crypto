import argparse
import re
import inverse_element
import nod

# TODO: Regexp really funny!
equationPattern = r'[1-9][0-9]*x=[1-9][0-9]*\(mod[1-9][0-9]*\)'


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
    Simple comparison, where (a,b)=1 or (a,b)!=1 

    Example:
        input: "3x=1(mod5)" 
        output: 3x=1(mod5) => x = 2+5k, k ∈ Z''', formatter_class=argparse.RawDescriptionHelpFormatter)

    parser.add_argument('equation', type=validate, nargs=1,
                        help='- equation. You can input the equation without space.')
    parser.add_argument('-s', '--solution', type=bool, const=True, default=False, nargs='?',
                        help='- print solution')
    args = parser.parse_args()
    return args


# This func compress and return list param. Input - the equation.
# By default this function does not compress parameters
#
#   Return:
#       param[0] - a
#       param[1] - b
#       param[2] - m
def getParams(equation: str,
              printSolution: bool,
              decompressParam: bool = False):
    answ = []

    # get first num: 23x=42(mod5) => 23     a
    result = re.match(r'[1-9][0-9]*', equation)
    if result.group(0) is None:
        raise RuntimeError(f'Ooops... Can not find first number')
    else:
        answ.append(int(result.group(0)))

    # get second num: 23x=42(mod5) => 42    b
    tmp = re.search(r'=[1-9][0-9]*\(', equation)
    if tmp is None:
        raise RuntimeError(f'Ooops... Can not find second number')
    else:
        result = re.search(r'[1-9][0-9]*', tmp.group(0))
        answ.append(int(result.group(0)))

    # get the third num: 23x=42(mod5) => 5  m
    tmp = re.search(r'mod[1-9][0-9]*', equation)
    if tmp is None:
        raise RuntimeError(f'Ooops... Can not find third number')
    else:
        result = re.search(r'[1-9][0-9]*', tmp.group(0))
        answ.append(int(result.group(0)))

    if decompressParam:
        return compresParam(answ[0], answ[1], answ[2], printSolution)
    else:
        return answ[0], answ[1], answ[2]


def compresParam(a, b, m, printSolution: bool):
    # 74x=69(mod7) => 4x=6(mod7)
    # 21x=35(mod14) => 7x=7x(mod14)
    if a > m and b > m:
        a = int(a % m)
        b = int(b % m)

    if nod.getNod(m, a) == nod.getNod(m, b):
        tmp_m = int(m / nod.getNod(m, a))
        a = int(a / nod.getNod(m, a))
        b = int(b / nod.getNod(m, b))
        m = tmp_m

    if printSolution:
        print(f'compress: {a}x={b}(mod{m})')

    return a, b, m


def getX(a, b, m, printSolution: bool):
    one = inverse_element.getInverseOf(m, a)
    two = inverse_element.getInverseOf(m, b)
    if printSolution:
        print(f'x={one[a] * two[b]}mod({m})')
        print(f'x={(one[a] * two[b]) % m}')

    return (one[a] * two[b]) % m


# This method using for check available solution
# If a % b == 0 then no solution
def checkPossible(a: int, b: int):
    if a > b:
        return a % b == 0
    else:
        return b % a == 0


# This func return the answer for the equation where (a,m)=1
def getAnswerForPrime(params: [], printSolution: bool):
    compressParam = compresParam(params[0],
                                 params[1],
                                 params[2],
                                 printSolution)
    x = getX(compressParam[0],
             compressParam[1],
             compressParam[2],
             printSolution)
    print(f'x = {x}+{params[2]}k, k ∈ Z')
    return x


# This func return the answer for the equation where (a,m)>1
#   Return the answer for the equation or
#   -1 if the equation has no solution
def getAnswerForNoPrime(params: [], printSolution: bool):
    compressParam = compresParam(params[0],
                                 params[1],
                                 params[2],
                                 printSolution)
    if not checkPossible(compressParam[0], compressParam[1]):
        print('The equation does not solution because a|b != 0')
        return -1

    # get first x
    xList = []
    xTmp = getX(compressParam[0],
                compressParam[1],
                compressParam[2],
                printSolution)

    # get all X values at intervals [firstX; m]
    while xTmp < params[2]:
        xList.append(xTmp)
        xTmp += compressParam[2]

    for each in xList:
        print(f'x = {each}+{params[2]}k, k ∈ Z')
    return xList


def isPrimeNumber(numOne, numTwo, printSolution: bool = False):
    nod_am = nod.getNod(numOne, numTwo)
    if printSolution:
        print(f'nod({numOne},{numTwo}) = {nod_am}')
    return nod_am == 1


# This func return the answer for the equation.
# Parameter:
#   strEquation - the equation
def getAnswerFromString(strEquation: str, printSolution: bool):
    param = getParams(strEquation, printSolution)

    if isPrimeNumber(param[0], param[2], printSolution):
        return getAnswerForPrime(param, argParser.solution)
    else:
        return getAnswerForNoPrime(param, argParser.solution)


if __name__ == '__main__':
    argParser = getParser()

    if argParser.solution:
        print(f'Equation: {argParser.equation[0]}')
    getAnswerFromString(argParser.equation[0], argParser.solution)
