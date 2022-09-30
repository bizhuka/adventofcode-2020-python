import argparse
from dataclasses import dataclass
import os.path
from select import select
import pytest
from support import timing

INPUT_TXT = os.path.join(os.path.dirname(__file__), 'input.txt')

######################################################


def compute(input: str, times: int = 30_000_000) -> int:
    numbers = [int(line) for line in input.split(",")]

    pairs = {num: [index+1, 0] for index, num in enumerate(numbers)}
    last_num = numbers[len(numbers)-1]

    for index in range(len(pairs)+1, times+1):
        pair = pairs[last_num]

        last_num = 0 if pair[1] == 0 else pair[1] - pair[0]
        pair = pairs.get(last_num, None)
        if pair is None:
            pairs[last_num] = [index, 0]
            continue

        if pair[1] == 0:
            pair[1] = index
        else:
            pair[0] = pair[1]
            pair[1] = index

    return last_num

######################################################


@pytest.mark.parametrize(
    ('input_s', 'expected'),
    (
        ('0,3,6', 175594),
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
