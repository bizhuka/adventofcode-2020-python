import argparse
import os.path
from enum import Enum, unique
from typing import Tuple
from unittest import result
import pytest

from support import timing

INPUT_TXT = os.path.join(os.path.dirname(__file__), 'input.txt')

######################################################


@unique
class Type(Enum):
    mask = 'mask'
    memory = 'mem['


def parse(input: str) -> list[Tuple]:
    result = []
    for index, line in enumerate(input.splitlines()):
        type = line[:4]

        match type:
            case Type.mask.value:
                mask = line[7:]
                result.append((type, mask,))

            case Type.memory.value:
                arr = line.split(' = ', maxsplit=1)
                address = int(arr[0][4:-1])
                value = int(arr[1])
                result.append((type, address, value,))

            case _:
                raise AssertionError(
                    f"Wrong type '{ type }' at { index + 1 } line")
    return result


def compute(s: str) -> int:
    result = dict()
    for line in parse(s):
        match line[0]:
            case Type.mask.value:
                mask = line[1]
                lv_and = int(mask.replace('X', '1'), 2)
                lv_or = int(mask.replace('X', '0'), 2)

            case Type.memory.value:
                address, value = line[1], line[2]
                result[address] = value & lv_and | lv_or
    return sum(result.values())

######################################################


INPUT_S = '''\
mask = XXXXXXXXXXXXXXXXXXXXXXXXXXXXX1XXXX0X
mem[8] = 11
mem[7] = 101
mem[8] = 0
'''


@pytest.mark.parametrize(
    ('input_s', 'expected'),
    (
        (INPUT_S, 165),
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
