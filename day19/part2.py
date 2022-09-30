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

    def __init__(self, rules_txt: str, change_8_11: bool) -> None:
        self.rules = dict()
        for rule_txt in rules_txt.split("\n"):
            match = rule_txt.split(": ")

            if change_8_11:
                match match[0]:
                    case "8":
                        match[1] = "42 | 42 8"
                    case "11":
                        match[1] = "42 31 | 42 11 31"

            self.rules[match[0]] = Rule(match[1])

    def get_rule(self, index: str, depth: int = 20) -> str:
        if depth == 0:
            return ""

        rule = self.rules.get(index, None)
        if rule is None:
            rule = Rule(index)
            self.rules[index] = rule

        if rule.regex:
            return rule.regex

        if rule.raw[0] == '"' and rule.raw[-1] == '"':
            rule.regex = f"{ rule.raw[1:-1]}"
        elif " " in rule.raw or "|" in rule.raw:
            lt_key = rule.raw.split()  # split by any whitespace
            rule.regex = "(" + "".join(["|" if lv_key == "|" else self.get_rule(lv_key, depth-1)
                                        for lv_key in lt_key]) + ")"
        else:
            rule.regex = self.get_rule(rule.raw, depth-1)

        return rule.regex


def compute(s: str, change_8_11: bool) -> int:
    rules_txt, check_txt = s.split('\n\n')
    solution = Solution(rules_txt, change_8_11)

    regex = re.compile(f'^{ solution.get_rule("0") }$')
    return sum([1 if regex.search(check) else 0
                for check in check_txt.split('\n')])

######################################################


INPUT_S = '''\
42: 9 14 | 10 1
9: 14 27 | 1 26
10: 23 14 | 28 1
1: "a"
11: 42 31
5: 1 14 | 15 1
19: 14 1 | 14 14
12: 24 14 | 19 1
16: 15 1 | 14 14
31: 14 17 | 1 13
6: 14 14 | 1 14
2: 1 24 | 14 4
0: 8 11
13: 14 3 | 1 12
15: 1 | 14
17: 14 2 | 1 7
23: 25 1 | 22 14
28: 16 1
4: 1 1
20: 14 14 | 1 15
3: 5 14 | 16 1
27: 1 6 | 14 18
14: "b"
21: 14 1 | 1 14
25: 1 1 | 1 14
22: 14 14
8: 42
26: 14 22 | 1 20
18: 15 15
7: 14 5 | 1 21
24: 14 1

abbbbbabbbaaaababbaabbbbabababbbabbbbbbabaaaa
bbabbbbaabaabba
babbbbaabbbbbabbbbbbaabaaabaaa
aaabbbbbbaaaabaababaabababbabaaabbababababaaa
bbbbbbbaaaabbbbaaabbabaaa
bbbababbbbaaaaaaaabbababaaababaabab
ababaaaaaabaaab
ababaaaaabbbaba
baabbaaaabbaaaababbaababb
abbbbabbbbaaaababbbbbbaaaababb
aaaaabbaabaaaaababaa
aaaabbaaaabbaaa
aaaabbaabbaaaaaaabbbabbbaaabbaabaaa
babaaabbbaaabaababbaabababaaab
aabbbbbaabbbaaaaaabbbbbababaaaaabbaaabba
'''


def test() -> None:
    assert compute(INPUT_S, False) == 3
    assert compute(INPUT_S, True) == 12


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument('data_file', nargs='?', default=INPUT_TXT)
    args = parser.parse_args()

    with open(args.data_file) as f, timing():
        print(compute(f.read(), True))

    return 0


if __name__ == '__main__':
    exit(main())
