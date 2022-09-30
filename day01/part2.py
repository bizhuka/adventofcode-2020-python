import argparse
import os.path

import pytest
import itertools

from support import timing

INPUT_TXT = os.path.join(os.path.dirname(__file__), 'input.txt')

######################################################
CURR_YEAR = 2020


def compute(s: str) -> int:
    numbers = [int(line) for line in s.splitlines()]
    for ind1, num1 in enumerate(numbers):
        if num1 > CURR_YEAR:
            continue
        for ind2 in range(ind1 + 1, len(numbers)):
            num2 = numbers[ind2]
            if num1 + num2 > CURR_YEAR:
                continue
            for ind3 in range(ind2 + 1, len(numbers)):
                num3 = numbers[ind3]
                if num1 + num2 + num3 == CURR_YEAR:
                    return num1 * num2 * num3

    raise AssertionError('No right answer')

######################################################


INPUT_S = '''\
1721
979
366
299
675
1456
'''


@pytest.mark.parametrize(
    ('input_s', 'expected'),
    (
        (INPUT_S, 241861950),
    ),
)
def test(input_s: str, expected: int) -> None:
    assert compute(input_s) == expected


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument('data_file', nargs='?', default=INPUT_TXT)
    args = parser.parse_args()

    with open(args.data_file) as f, timing():
        print(compute(f.read()))

    return 0


if __name__ == '__main__':
    exit(main())
