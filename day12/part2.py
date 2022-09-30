import argparse
import os.path
import pytest
from support import timing

INPUT_TXT = os.path.join(os.path.dirname(__file__), 'input.txt')

######################################################


def compute(s: str) -> int:
    x_east = y_north = 0
    x_east_way, y_north_way = 10, 1

    lines = s.splitlines()
    for index, line in enumerate(lines):
        action = line[0]
        number = int(line[1:])

        match action:
            case "N":
                y_north_way += number
            case "S":
                y_north_way -= number
            case "E":
                x_east_way += number
            case "W":
                x_east_way -= number
            case "F":
                x_east += x_east_way * number
                y_north += y_north_way * number
            case "R" | "L":
                sign_1 = 1 if action == 'L' else -1
                sign_2 = sign_1 * -1
                for _ in range(number // 90):
                    lv_temp = x_east_way
                    x_east_way = y_north_way * sign_2
                    y_north_way = lv_temp * sign_1
            case _:
                raise AssertionError(f"Wrong action '{ action }' at { index + 1 } line")

    return abs(x_east) + abs(y_north)

######################################################


INPUT_S = '''\
F10
N3
F7
R90
F11
'''


@pytest.mark.parametrize(
    ('input_s', 'expected'),
    (
        (INPUT_S, 286),
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
