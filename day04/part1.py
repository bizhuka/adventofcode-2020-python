import argparse
import os.path

import pytest

from support import timing

INPUT_TXT = os.path.join(os.path.dirname(__file__), 'input.txt')

######################################################
class Solution:
    t_required: list   

    def __init__(self):
        self.t_required = {'byr', 'iyr', 'eyr', 'hgt', 'hcl', 'ecl', 'pid'}        

    def valid_count(self, passports: list) -> int:
        result = 0
        for passport in passports:
            if self.is_valid(passport):
                result += 1
        return result

    def is_valid(self, passport) -> bool:
        required_list = self.t_required.copy()

        passwords = passport.splitlines()
        for password in passwords:
            pairs = password.split(" ")
            for pair in pairs:
                key, _ = pair.split(":")
                if key in required_list:
                    required_list.remove(key)
        return len(required_list) == 0


def compute(s: str) -> int:
    passports = s.split("\n\n")
    sol = Solution()
    
    return sol.valid_count(passports)

######################################################

INPUT_S = '''\
ecl:gry pid:860033327 eyr:2020 hcl:#fffffd
byr:1937 iyr:2017 cid:147 hgt:183cm

iyr:2013 ecl:amb cid:350 eyr:2023 pid:028048884
hcl:#cfa07d byr:1929

hcl:#ae17e1 iyr:2013
eyr:2024
ecl:brn pid:760753108 byr:1931
hgt:179cm

hcl:#cfa07d eyr:2025 pid:166559648
iyr:2011 ecl:brn hgt:59in'''


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
