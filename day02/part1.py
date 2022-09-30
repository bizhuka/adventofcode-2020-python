import argparse
import os.path

import pytest

from support import timing

INPUT_TXT = os.path.join(os.path.dirname(__file__), 'input.txt')

######################################################


def compute(s: str) -> int:
    result = 0

    lines = s.splitlines()
    for line in lines:
        sp0 = line.split(": ")
        sp1 = sp0[0].split(" ")
        sp2 = sp1[0].split("-")
        if is_ok(int(sp2[0]), int(sp2[1]), sp1[1], sp0[1]):
            result += 1

    return result


def is_ok(cnt_from: int, cnt_to: int, letter: str, password: str) -> bool:
    count = 0
    for char in list(password):
        if char == letter:
            count += 1
    return count >= cnt_from and count <= cnt_to

######################################################


INPUT_S = '''\
1-3 a: abcde
1-3 b: cdefg
2-9 c: ccccccccc
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
