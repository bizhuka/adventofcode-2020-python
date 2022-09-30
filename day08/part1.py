import argparse
from ast import Raise
from importlib.util import set_loader
from itertools import count
import os.path
from tkinter.messagebox import NO
from unittest import result

import pytest

from support import timing
from dataclasses import dataclass, field

INPUT_TXT = os.path.join(os.path.dirname(__file__), 'input.txt')

######################################################


@dataclass
class Rule:
    cmd: str
    number: int

class Main:
    rules: list[Rule]
    stack: set[int] = set()
    counter: int = 0    

    def __init__(self, s) -> None:
        self.rules = [Rule(line[0:3], int(line[4:]))
                      for line in s.splitlines()]

    def next(self, index: int) -> None:
        if index >= len(self.rules):
            return 
        rule: Rule = self.rules[index]

        if index in self.stack:
            return 
        self.stack.add(index)

        match rule.cmd:
            case 'nop':
                self.next(index+1)
            case 'acc':
                self.counter += rule.number
                self.next(index+1)
            case 'jmp':
                self.next(index + rule.number)                
            case _:
                raise NotImplementedError(rule.cmd)

def compute(s: str) -> int:
    main = Main(s)
    main.next(0)
    return main.counter


######################################################

INPUT_S = '''\
nop +0
acc +1
jmp +4
acc +3
jmp -3
acc -99
acc +1
jmp -4
acc +6
'''


@pytest.mark.parametrize(
    ('input_s', 'expected'),
    (
        (INPUT_S, 5),
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
