import argparse
import os.path
import math
import pytest

from support import timing

INPUT_TXT = os.path.join(os.path.dirname(__file__), 'input.txt')

######################################################


def compute(s: str) -> int:
    arr = s.split("\n", maxsplit=1)
    minute_arrival = int(arr[0])
    buses = [int(line) for line in arr[1].split(",") if line != "x"]

    bus_number = 0
    nearst_time = math.inf
    for bus in buses:
        if minute_arrival % bus == 0:
            nearst_time = minute_arrival
            bus_number = bus
            break

        nearst = minute_arrival // bus * bus + bus
        if nearst_time > nearst:
            nearst_time = nearst
            bus_number = bus

    if bus_number:
        return (nearst_time - minute_arrival) * bus_number
    return -1

######################################################


INPUT_S = '''\
939
7,13,x,x,59,x,31,19
'''


@pytest.mark.parametrize(
    ('input_s', 'expected'),
    (
        (INPUT_S, 295),
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
