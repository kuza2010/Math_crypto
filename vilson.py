MAX_PRIMARY = 99999
MIN_PRIMARY = 1


def factor_by_div(number: int):
    counter = 0
    result = 1
    while counter < number - 1:
        if result < number:
            result = result * (counter + 1)
        else:
            result = (result % number) * (counter + 1)

        counter += 1

    return result


def isPrimary(number: int):
    if factor_by_div(number) % number == number - 1:
        return True
    return False


if __name__ == '__main__':
    current_num = MIN_PRIMARY

    while current_num <= MAX_PRIMARY:
        if isPrimary(current_num):
            print(f'number {current_num} is primary')
        current_num += 1
