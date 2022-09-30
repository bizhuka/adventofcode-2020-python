import re


class Solution:
    t_required: list
    check_values: bool
    eye_colors: set

    def __init__(self, check_values=False):
        self.t_required = {'byr', 'iyr', 'eyr', 'hgt', 'hcl', 'ecl', 'pid'}
        self.check_values = check_values
        self.eye_colors = { 'amb', 'blu', 'brn', 'gry', 'grn', 'hzl', 'oth'}

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
