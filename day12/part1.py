import argparse
import os.path
import pytest
from support import timing

INPUT_TXT = os.path.join(os.path.dirname(__file__), 'input.txt')

######################################################


def compute(s: str) -> int:
    x_east = y_north = 0

    angles = [
        (1, 0),
        (0, 1),
        (-1, 0),
        (0, -1),
    ]
    angle_ind = 0

    lines = s.splitlines()
    for index, line in enumerate(lines):
        action = line[0]
        number = int(line[1:])

        match action:
            case "N":
                y_north += number
            case "S":
                y_north -= number
            case "E":
                x_east += number
            case "W":
                x_east -= number
            case "R" | "L":
                angle_ind += number // 90 * (1 if action == "L" else -1)
                angle_ind %= 4
            case "F":
                x, y = angles[angle_ind]
                x_east += x * number
                y_north += y * number
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
        (INPUT_S, 25),
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
