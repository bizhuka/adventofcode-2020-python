import argparse
import os.path
import re
import pytest

from support import timing

INPUT_TXT = os.path.join(os.path.dirname(__file__), 'input.txt')

######################################################
class Solution:
    t_required: list    
    eye_colors: set
    check_values: bool

    def __init__(self, check_values=False):
        self.t_required = {'byr', 'iyr', 'eyr', 'hgt', 'hcl', 'ecl', 'pid'}        
        self.eye_colors = { 'amb', 'blu', 'brn', 'gry', 'grn', 'hzl', 'oth'}
        self.check_values = check_values

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
                key, val = pair.split(":")

                if self.check_values and not self.is_ok(key, val):
                    continue

                if key in required_list:
                    required_list.remove(key)
        return len(required_list) == 0

    def is_ok(self, key, val) -> bool:
        if key == 'byr':
            res = re.findall('\d{4}$', val)
            if res:
                return '1920' <= res[0] <= '2002'
        elif key == 'iyr':
            res = re.findall('\d{4}$', val)
            if res:
                return '2010' <= res[0] <= '2020'
        elif key == 'eyr':
            res = re.findall('\d{4}$', val)
            if res:
                return '2020' <= res[0] <= '2030'
        elif key == 'hgt':
            res = re.findall('^(\d+)(cm|in)$', val)
            if res:
                if res[0][1] == 'cm':
                    return '150' <= res[0][0] <= '193'
                elif res[0][1] == 'in':
                    return '59' <= res[0][0] <= '76'
        elif key == 'hcl':
            return bool(re.findall('^\#[0-9a-f]{6}$', val))
        elif key == 'pid':
            return bool(re.findall('^\d{9}$', val))
        elif key == 'ecl':
            res = val in self.eye_colors
            return bool(res)

def compute(s: str) -> int:
    passports = s.split("\n\n")
    sol = Solution(True)
    
    return sol.valid_count(passports)

######################################################

INPUT_INVALID_ALL = '''\
eyr:1972 cid:100
hcl:#18171d ecl:amb hgt:170 pid:186cm iyr:2018 byr:1926

iyr:2019
hcl:#602927 eyr:1967 hgt:170cm
ecl:grn pid:012533040 byr:1946

hcl:dab227 iyr:2012
ecl:brn hgt:182cm pid:021572410 eyr:2020 byr:1992 cid:277

hgt:59cm ecl:zzz
eyr:2038 hcl:74454a iyr:2023
pid:3556412378 byr:2007
'''

INPUT_VALID_ALL = '''\
pid:087499704 hgt:74in ecl:grn iyr:2012 eyr:2030 byr:1980
hcl:#623a2f

eyr:2029 ecl:blu cid:129 byr:1989
iyr:2014 pid:896056539 hcl:#a97842 hgt:165cm

hcl:#888785
hgt:164cm byr:2001 iyr:2015 cid:88
pid:545766238 ecl:hzl
eyr:2022

iyr:2010 hgt:158cm hcl:#b6652a ecl:blu byr:1944 eyr:2021 pid:093154719
'''


@pytest.mark.parametrize(
    ('input_s', 'expected'),
    (
        (INPUT_INVALID_ALL, 0),
        (INPUT_VALID_ALL, 4),
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
