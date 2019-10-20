#!/usr/bin/python3

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


def get_all_primary(max_num: int, include_null: bool):
    primes = []
    counter = 1
    if include_null:
        primes.append(0)

    while counter < max_num - 1:
        if isPrimary(counter):
            primes.append(counter)
        counter += 1

    return primes


if __name__ == '__main__':
    current_num = MIN_PRIMARY

    while current_num <= MAX_PRIMARY:
        if isPrimary(current_num):
            print(f'number {current_num} is primary')
        current_num += 1
