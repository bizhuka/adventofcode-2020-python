from dataclasses import dataclass
import argparse
import os.path

import pytest

from support import timing

INPUT_TXT = os.path.join(os.path.dirname(__file__), 'input.txt')

######################################################


class Rule:
    all_rules: list
    unq_ids: set

    def __init__(self, main, subs):
        self.main = main
        self.subs = subs

    @classmethod
    def init(cls, s:str) -> None:
        cls.all_rules = list()
        cls.unq_ids = set()

        lines = s.splitlines()
        for line in lines:
            arr = line.split(" bags contain ")
            cls.all_rules.append(Rule(arr[0], arr[1]))
    
    @classmethod
    def count(cls,  sub_bag:str) -> None:
        for index, rule in enumerate(cls.all_rules):            
            if sub_bag in rule.subs:
                cls.unq_ids.add(index)
                Rule.count(rule.main)        

def compute(s: str) -> int:
    Rule.init(s)
    Rule.count("shiny gold") 
    return len(Rule.unq_ids)

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
        (INPUT_S, 4),
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
