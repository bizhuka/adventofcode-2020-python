import argparse
from itertools import count
from operator import indexOf, le
import os.path
import re
import pytest

from support import timing

INPUT_TXT = os.path.join(os.path.dirname(__file__), 'input.txt')

######################################################

ONE_EXPRESSION = re.compile(r'[\(\)]')
SPLIT_BY_TILDA = re.compile(r'[\+\*]')


def _do_calc(input: str) -> int:
    while '(' in input:
        in_parentheses = __get_first_exp(input)
        input = input.replace('(' + in_parentheses + ')',
                              str(_do_calc(in_parentheses)))

    signs = SPLIT_BY_TILDA.findall(input)
    input = re.sub(SPLIT_BY_TILDA, '~', input)
    numbers = [int(number) for number in input.split('~')]

    for sign in signs:
        match sign:
            case '*':
                numbers[0] *= numbers[1]
            case '+':
                numbers[0] += numbers[1]
        numbers.pop(1)
    assert len(numbers) == 1

    return numbers[0]


def __get_first_exp(input: str) -> str:
    prev_char = ''
    prev_pos = -1
    for match in ONE_EXPRESSION.finditer(input):
        pos = match.regs[0][0]
        char = input[pos]
        if prev_char == '(' and char == ')':
            return input[prev_pos + 1: pos]
        prev_char = char
        prev_pos = pos

    raise AssertionError("Wrong sequence of '(', ')' ")


def compute(s: str) -> int:
    return sum([_do_calc(line.replace(" ", "")) for line in s.splitlines()])

######################################################


@pytest.mark.parametrize(
    ('input_s', 'expected'),
    (
        ("1 + 2 * 3 + 4 * 5 + 6", 71),
        ("2 * 3 + (4 * 5)", 26),
        ("5 + (8 * 3 + 9 + 3 * 4 * 3)", 437),
        ("5 * 9 * (7 * 3 * 3 + 9 * 3 + (8 + 6 * 4))", 12240),
        ("((2 + 4 * 9) * (6 + 9 * 8 + 6) + 6) + 2 + 4 * 2", 13632),
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
