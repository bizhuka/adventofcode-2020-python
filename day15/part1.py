import argparse
from dataclasses import dataclass
from typing import Dict
import os.path
from select import select

import pytest
from support import timing

INPUT_TXT = os.path.join(os.path.dirname(__file__), 'input.txt')

######################################################


@dataclass
class Pair:
    ind1: int = 0
    ind2: int = 0

    def __init__(self, index) -> None:
        self.ind1 = index


@dataclass
class Solution:
    pairs: Dict[int, Pair]
    _last_one: int

    def __init__(self, input: str) -> None:
        numbers = [int(line) for line in input.split(",")]
        self.pairs = {num: Pair(index+1) for index, num in enumerate(numbers)}
        self._last_one = numbers[len(numbers)-1]

    def compute(self, count: int) -> int:
        for index in range(len(self.pairs)+1, count+1):
            pair = self.pairs[self._last_one]

            new_num = 0 if pair.ind2 == 0 else pair.ind2 - pair.ind1
            pair = self.pairs.get(new_num, None)
            self._last_one = new_num
            if pair is None:
                pair = Pair(index)
                self.pairs[new_num] = pair
                continue            

            if pair.ind2 == 0:
                pair.ind2 = index
            else:
                pair.ind1 = pair.ind2
                pair.ind2 = index
        return self._last_one


def compute(s: str) -> int:
    solution = Solution(s)
    return solution.compute(2020)

######################################################


@pytest.mark.parametrize(
    ('input_s', 'expected'),
    (
        ('0,3,6', 436),
        ('1,3,2', 1),
        ('2,1,3', 10),
        ('1,2,3', 27),
        ('2,3,1', 78),
        ('3,2,1', 438),
        ('3,1,2', 1836),
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
