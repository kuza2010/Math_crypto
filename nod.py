import argparse
from tabulate import tabulate

# default value
xList = [1, 0]
yList = [0, 1]


def validate(string: str):
    value = int(string)

    if value <= 0:
        raise argparse.ArgumentTypeError(f'Incorrect value: {string}')

    return value


def getParser():
    parser = argparse.ArgumentParser(description='''
    About script:
    =========================================
    Math foundations of cryptology. Script #1.
    Find NOD for two numbers.
    
    Simple: 
        (175,77)=7''', formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument('numfirst', type=validate, nargs=1, help='- first digit')
    parser.add_argument('numsecond', type=validate, nargs=1, help='- second digit')
    # append u,v: (a,b)=au+bv

    parser.add_argument('-d', '--decompose', type=bool, const=True, default=False, nargs='?',
                        help='- linear decomposition NOD')
    # print table
    parser.add_argument('-p', '--print-table', type=bool, const=True, default=False, nargs='?',
                        help='- print decompose table')
    args = parser.parse_args()
    return args


def initTable(isDecompose: bool, numOne, numTwo):
    table = []
    if isDecompose:
        table.append([numOne, '*', xList[0], yList[0]])
        table.append([numTwo, '*', xList[1], yList[1]])
    else:
        table.append([numOne, '*'])
        table.append([numTwo, '*'])

    return table


def getHeaders(isDecompose: bool):
    header = ["Остаток", "Частное"]
    if isDecompose:
        header.append("X")
        header.append("Y")

    return header


def getNod(numOne, numTwo):
    nod = numTwo

    while numOne != 0 and numTwo != 0:
        mod = int(numOne % numTwo)  # remainder of the division
        if mod != 0:
            nod = mod
        numOne = numTwo
        numTwo = mod

    return nod


def getPrintableNOD(isDecompose: bool, isPrinting: bool, numOne: int, numTwo: int):
    if numOne == numTwo:
        print(f'{numOne} equals {numTwo} -> Nod({numOne},{numTwo}) = {numOne}')
        return

    constNum1 = numOne
    constNum2 = numTwo

    table = initTable(isDecompose, numOne, numTwo)
    answer = numTwo

    startPos = 2  # start from position 2

    while numOne != 0 and numTwo != 0:
        mod = int(numOne % numTwo)  # remainder of the division
        div = int(numOne / numTwo)  # integer

        if mod != 0:
            answer = mod

        numOne = numTwo
        numTwo = mod

        if not isDecompose:
            table.append([mod, div if div != 0 else " "])
        else:
            xi = ""
            yi = ""

            if mod != 0:
                xi = xList[startPos - 2] - (div * xList[startPos - 1])
                yi = yList[startPos - 2] - (div * yList[startPos - 1])

            xList.append(xi)
            yList.append(yi)

            table.append([mod, div if div != 0 else " ", xi, yi])

        startPos += 1

    if isPrinting:
        print(tabulate(table, headers=getHeaders(isDecompose), tablefmt="fancy_grid"))

    if not isDecompose:
        print(f'NOD({constNum1},{constNum2}) = {answer}')
    else:
        print(f'NOD({constNum1},{constNum2}) = {answer} => u={xList[len(xList) - 2]} v={yList[len(yList) - 2]}')

    # return nod, u, v
    return answer, xList[len(xList) - 2], yList[len(yList) - 2]


if __name__ == '__main__':
    argParser = getParser()
    a = argParser.numfirst[0]  # get first num
    b = argParser.numsecond[0]  # get second num

    answer = getPrintableNOD(argParser.decompose, argParser.print_table, a if a > b else b, b if b < a else a)
