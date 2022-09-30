import argparse
from ast import Raise
from importlib.util import set_loader
from itertools import count
import os.path
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

class State:
    stack: set[int]
    counter: int = 0    
    ok_line: int = 0
    def __init__(self) -> None:
        self.stack = set()


class Main:
    rules: list[Rule]
    state: State = State()

    def __init__(self, s) -> None:
        self.rules = [Rule(line[0:3], int(line[4:]))
                      for line in s.splitlines()]

    def next(self, index: int, repair: bool = False) -> bool:
        if index >= len(self.rules):
            return False
        rule: Rule = self.rules[index]

        ok = False
        if index in self.state.stack:
            return True
        self.state.stack.add(index)

        match rule.cmd:
            case 'nop':
                stoped = self.next(index+1, repair)
                if repair and stoped:
                    stoped = self.next(index + rule.number)
                    ok = not stoped
            case 'acc':
                self.state.counter += rule.number
                stoped = self.next(index+1, repair)
            case 'jmp':
                stoped = self.next(index + rule.number, repair)
                if repair and stoped:
                    stoped = self.next(index + 1)
                    ok = not stoped
            case _:
                raise NotImplementedError(rule.cmd)

        if ok:
            self.state.ok_line = index

        return stoped


def compute(s: str) -> int:
    main = Main(s)
    if main.next(0, True):
        return - 1
    
    rule = main.rules[ main.state.ok_line ]
    rule.cmd = 'nop' if rule.cmd == 'jmp' else 'nop'

    main.state = State()
    if main.next(0):
        return - 1

    return main.state.counter


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
acc +6'''


@pytest.mark.parametrize(
    ('input_s', 'expected'),
    (
        (INPUT_S, 8),
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
