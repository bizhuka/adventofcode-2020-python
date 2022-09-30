import argparse
import os.path
from pprint import pprint

import pytest

from support import timing

INPUT_TXT = os.path.join(os.path.dirname(__file__), 'input.txt')

######################################################
class Solution:
    numbers:list[int]

    def __init__(self, input) -> None:
        self.numbers = [int(line) for line in input.splitlines()]
    
    def part2(self, preamble)->int:
        part1_result = self.part1(preamble)
        for ind, lv_num in enumerate(self.numbers):
            result_range = [lv_num]
            for ind_next in range(ind+1, len(self.numbers)):
                num_next = self.numbers[ind_next]                
                result_range.append(num_next)

                lv_num += num_next
                if lv_num == part1_result:
                    result_range.sort()
                    return result_range[0] + result_range[len(result_range)-1] 

                if lv_num > part1_result:
                    break
        return -1

    def part1(self, preamble)->int:
        visited = { self.numbers[ind] for ind in range(0,preamble) }    
        for ind in range(preamble,len( self.numbers)):
            number = self.numbers[ind]
            
            # visited = set()
            found = False
            for prev_ind in range(ind-preamble,ind):
                num_prev = self.numbers[prev_ind]
                # visited.add(num_prev)            
                if number - num_prev in visited:
                    found = True
                    break
            if not found:
                return number
            visited.add( self.numbers[ind] )
            visited.remove( self.numbers[ind-preamble] )        
        return -1

def compute(input: str, preamble) -> int:
    solution = Solution(input)
    return solution.part2(preamble)

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
576
'''


@pytest.mark.parametrize(
    ('input_s', 'expected'),
    (
        (INPUT_S, 62),
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
