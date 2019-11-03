from canonic_view import prime_factors_list
import argparse


def validate(string: str):
    value = int(string)

    if value <= 0:
        raise argparse.ArgumentTypeError(f'Incorrect value: {string}')

    return value


def getParser():
    parser = argparse.ArgumentParser(description='''
    About script:
    =========================================
    Math foundations of cryptology. Задание #5.
    Расчет функции Эйлера для m

    Пример: 
        42= 2^1 * 3^1 * 7^1''', formatter_class=argparse.RawDescriptionHelpFormatter)

    parser.add_argument('number', type=validate, nargs=1, help='- integer digit')
    # print table
    parser.add_argument('-pd', '--print-decomposition', type=bool, const=True, default=False, nargs='?',
                        help='- print decompose view')
    parser.add_argument('-pc', '--print_canonic', type=bool, const=True, default=False, nargs='?',
                        help='- print canonic view')

    args = parser.parse_args()
    return args


def euler(number: int):
    decDict = prime_factors_list(number)
    result = 1
    resultString = []  # contains all multiplier

    # key - number, value - degree
    for key in decDict.keys():
        numOne = key ** decDict[key]  # num^x
        numTwo = key ** (decDict[key] - 1)  # num^(x-1)
        tmpResult = numOne - numTwo  # num^x - num^(x-1)

        resultString.append(f'({key}^{decDict[key]}-{key}^{(decDict[key] - 1)}) *')
        result = result * tmpResult

    # return answer, decompose list
    return result, resultString


def getPrettyStr(number: int, lists: list):
    return f'{(" ".join(lists))[:-1]} = {number}'


if __name__ == '__main__':
    argParser = getParser()

    num = argParser.number[0]
    answer = euler(num)

    if argParser.print_decomposition:
        print(f'Euler: F({num}) = {getPrettyStr(answer[0], answer[1])}')
    else:
        print(f'Euler: F({num}) = {answer[0]}')
