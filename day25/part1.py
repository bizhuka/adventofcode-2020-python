import argparse
import os.path

import pytest

from support import timing

INPUT_TXT = os.path.join(os.path.dirname(__file__), 'input.txt')

######################################################


def get_loop_size(target_value: int) -> int:
    num = 1
    ind = 0
    while True:
        ind += 1
        num = (num * 7) % 20201227
        if num == target_value:
            return ind


def get_encryption_key(count: int, number: int) -> int:
    result = 1
    for _ in range(count):
        result = result * number % 20201227
    return result


def compute(s: str) -> int:
    numbers = [int(line) for line in s.splitlines()]
    public_key = numbers[0]
    door_key = numbers[1]

    public_loop_size = get_loop_size(public_key)
    door_loop_size = get_loop_size(door_key)

    result1 = get_encryption_key(public_loop_size, door_key)
    result2 = get_encryption_key(door_loop_size, public_key)

    if result1 == result2:
        return result1

    return -1

######################################################


INPUT_S = '''\
5764801
17807724
'''


@pytest.mark.parametrize(
    ('input_s', 'expected'),
    (
        (INPUT_S, 14897079),
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
