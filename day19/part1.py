import argparse
from dataclasses import dataclass
import os.path
import re
import pytest

from support import timing

INPUT_TXT = os.path.join(os.path.dirname(__file__), 'input.txt')

######################################################


@dataclass
class Rule:
    raw: str
    regex: str = ''


@dataclass
class Solution:
    rules: dict[int, Rule]

    def __init__(self, rules_txt: str) -> None:
        self.rules = dict()
        for rule_txt in rules_txt.split("\n"):
            match = rule_txt.split(": ")
            self.rules[match[0]] = Rule(match[1])

    def get_rule(self, index: str) -> str:
        rule = self.rules.get(index, None)
        if rule is None:
            rule = Rule(index)
            self.rules[index] = rule

        if rule.regex:
            return rule.regex

        if rule.raw[0] == '"' and rule.raw[-1] == '"':
            rule.regex = f"{ rule.raw[1:-1]}"
        elif " " in rule.raw or "|" in rule.raw:
            lt_key = rule.raw.split() # split by any whitespace 
            rule.regex = "(" + "".join(["|" if lv_key == "|" else self.get_rule(lv_key)
                                        for lv_key in lt_key]) + ")"
        else:
            rule.regex = self.get_rule(rule.raw)

        return rule.regex


def compute(s: str) -> int:
    rules_txt, check_txt = s.split('\n\n')
    solution = Solution(rules_txt)

    regex = re.compile(f'^{ solution.get_rule("0") }$')
    return sum([1 if regex.search(check) else 0
                for check in check_txt.split('\n')])

######################################################


INPUT_S = '''\
0: 4 1 5
1: 2 3 | 3 2
2: 4 4 | 5 5
3: 4 5 | 5 4
4: "a"
5: "b"

ababbb
bababa
abbbab
aaabbb
aaaabbb
'''


@pytest.mark.parametrize(
    ('input_s', 'expected'),
    (
        (INPUT_S, 2),
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
