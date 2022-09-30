import argparse
import os.path
import math
import pytest

from support import timing

INPUT_TXT = os.path.join(os.path.dirname(__file__), 'input.txt')

######################################################


def compute(s: str) -> int:
    arr = s.split("\n", maxsplit=1)
    buses = [1 if line == "x" else int(line) for line in arr[1].split(",")]

    count = 0
    stepsize = buses[0]
    for index in range(1, len(buses)):
        bus = buses[index]
        while (count + index) % bus != 0:
            count += stepsize
        stepsize *= bus
    return count

######################################################


@pytest.mark.parametrize(
    ('input_s', 'expected'),
    (
        ('777\n3,7,11,5', 867),
        ('777\n17,x,13,19', 3417),
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
