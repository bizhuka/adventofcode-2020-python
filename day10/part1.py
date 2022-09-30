import argparse
import collections
import os.path
from re import S

import pytest

from support import timing

INPUT_TXT = os.path.join(os.path.dirname(__file__), 'input.txt')

######################################################
class Solution:
    numbers: list[int]
    def __init__(self, input) -> None:
        self.numbers = [int(line) for line in input.splitlines()]
        self.numbers.sort(reverse=True)
        self.numbers.append(0)
        self.numbers.insert(0, self.numbers[ 0 ] + 3)

    def part1(self):
        result = collections.Counter({})
        for ind in range(1, len(self.numbers)):
            result[ self.numbers[ind - 1] - self.numbers[ind] ] += 1

        return result[1] * result[3] 

def compute(s: str) -> int:
    solution = Solution(s)
    return solution.part1() 

######################################################

INPUT_S = '''\
16
10
15
5
1
11
7
19
6
12
4
'''


@pytest.mark.parametrize(
    ('input_s', 'expected'),
    (
        (INPUT_S, 7 * 5),
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
