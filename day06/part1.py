import argparse
from cgitb import reset
import os.path
from unittest import result

import pytest

from support import timing

INPUT_TXT = os.path.join(os.path.dirname(__file__), 'input.txt')

######################################################
def compute(s: str) -> int:
    result = 0

    lines = s.split("\n\n")
    for line in lines:
        unq_char_set = set()
        for char in line:
            if char != "\n":
                unq_char_set.add(char)
        result += len(unq_char_set)

    return result

######################################################

INPUT_S = '''\
abc

a
b
c

ab
ac

a
a
a
a

b
'''


@pytest.mark.parametrize(
    ('input_s', 'expected'),
    (
        (INPUT_S, 11),
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
