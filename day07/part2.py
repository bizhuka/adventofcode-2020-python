from dataclasses import dataclass
import argparse
from itertools import count
import os.path

import pytest

from support import timing

INPUT_TXT = os.path.join(os.path.dirname(__file__), 'input.txt')

######################################################

@dataclass
class SubRule:
    count:int
    bag:str

class Rule:
    all_rules: dict

    def __init__(self, main : str, subs: str):
        self.main   = main
        self.subs   = subs

        self.t_subs = list()
        l_bugs = subs.replace(", ", "").replace(".", ""
                    ).replace("bags", "-").replace("bag","-"
                    ).split("-")

        for bag in l_bugs:
            if bag == "" or not bag[0].isnumeric():
                continue
            arr = bag.split(" ", maxsplit=1)
            self.t_subs.append(SubRule(int(arr[0]), arr[1].strip()))


    @classmethod
    def init(cls, s:str) -> None:
        cls.all_rules = dict()

        lines = s.splitlines()
        for line in lines:
            arr = line.split(" bags contain ", maxsplit=1)
            cls.all_rules[arr[0]] = Rule( arr[0], arr[1])
    
    @classmethod
    def count(cls,  main_bag:str) -> int:
        result = 1
        rule = cls.all_rules.get(main_bag, False)
        if rule:            
            for sub in rule.t_subs:
                result += sub.count * Rule.count(sub.bag)

        return result        

def compute(s: str) -> int:
    Rule.init(s)     
    return Rule.count("shiny gold") - 1

######################################################


INPUT_S = '''\
light red bags contain 1 bright white bag, 2 muted yellow bags.
dark orange bags contain 3 bright white bags, 4 muted yellow bags.
bright white bags contain 1 shiny gold bag.
muted yellow bags contain 2 shiny gold bags, 9 faded blue bags.
shiny gold bags contain 1 dark olive bag, 2 vibrant plum bags.
dark olive bags contain 3 faded blue bags, 4 dotted black bags.
vibrant plum bags contain 5 faded blue bags, 6 dotted black bags.
faded blue bags contain no other bags.
dotted black bags contain no other bags.'''


@pytest.mark.parametrize(
    ('input_s', 'expected'),
    (
        (INPUT_S, 32),
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
