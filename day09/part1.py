import argparse
import os.path
from pprint import pprint

import pytest

from support import timing

INPUT_TXT = os.path.join(os.path.dirname(__file__), 'input.txt')

######################################################
def compute(s: str, preamble) -> int:
    numbers = [int(line) for line in s.splitlines()]

    visited = { numbers[ind] for ind in range(0,preamble) }
    
    for ind in range(preamble,len(numbers)):
        number = numbers[ind]
        
        # visited = set()
        found = False
        for prev_ind in range(ind-preamble,ind):
            num_prev = numbers[prev_ind]
            # visited.add(num_prev)            
            if number - num_prev in visited:
                found = True
                break
        if not found:
            return number
        visited.add(numbers[ind])
        visited.remove(numbers[ind-preamble])        

    return -1

######################################################

INPUT_S = '''\
35
20
15
25
47
40
62
55
65
95
102
117
150
182
127
219
299
277
309
576'''


@pytest.mark.parametrize(
    ('input_s', 'expected'),
    (
        (INPUT_S, 127),
    ),
)
def test(input_s: str, expected: int) -> None:
    assert compute(input_s, 5) == expected


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument('data_file', nargs='?', default=INPUT_TXT)
    args = parser.parse_args()

    with open(args.data_file) as f, timing():
        print(compute(f.read(), 25))

    return 0


if __name__ == '__main__':
    exit(main())
