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
                zeros = ['0' for _ in range(len(mask))]
                and_mask = mask.replace('0', '1').replace('X', '0')
                and_0_pos = [index for index, char in enumerate(and_mask) if char == '0']

                lv_or = int(mask.replace('X', '0'), 2)
                lv_and = int(and_mask, 2)

            case Type.memory.value:
                address, value = line[1], line[2]
                address = address & lv_and | lv_or

                add_number = zeros.copy()
                for index in range(2 ** len(and_0_pos)):
                    for zero_pos in and_0_pos:
                        add_number[zero_pos] = '1' if index % 2 == 0 else '0'
                        index //= 2

                    result[address + int("".join(add_number), 2)] = value

    return sum(result.values())

######################################################


INPUT_S = '''\
mask = 000000000000000000000000000000X1001X
mem[42] = 100
mask = 00000000000000000000000000000000X0XX
mem[26] = 1
'''


@pytest.mark.parametrize(
    ('input_s', 'expected'),
    (
        (INPUT_S, 208),
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
