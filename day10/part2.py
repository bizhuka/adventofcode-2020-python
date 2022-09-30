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

    def part2(self):
        list_counts = collections.Counter({0: 1})
        for ind in range(1, len(self.numbers)):
            lv_num1 = self.numbers[ind]

            prev_index = ind - 1
            while prev_index >= 0 and self.numbers[ prev_index ] - lv_num1 <= 3:
                list_counts[ ind ] += list_counts[ prev_index ]
                prev_index -= 1
        return list_counts[ ind ]

def compute(s: str) -> int:
    solution = Solution(s)
    return solution.part2()

######################################################

INPUT_S_1 = '''\
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

INPUT_S_2 = '''\
28
33
18
42
31
14
46
20
48
47
24
23
49
45
19
38
39
11
1
32
25
35
8
17
7
9
4
2
34
10
3
'''


@pytest.mark.parametrize(
    ('input_s', 'expected'),
    (
        (INPUT_S_1, 8),
        (INPUT_S_2, 19208),
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
