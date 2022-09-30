import argparse
import os.path

import pytest

from support import timing

INPUT_TXT = os.path.join(os.path.dirname(__file__), 'input.txt')

######################################################


def row(s: str) -> int:
    bin = s.replace("F", "0").replace("B", "1")
    return int(bin, 2)


def col(s: str) -> int:
    bin = s.replace("L", "0").replace("R", "1")
    return int(bin, 2)


def seat_id(s: str) -> int:
    return row(s[:7]) * 8 + col(s[7:])


def compute(s: str) -> int:
    seat_ids = list()

    lines = s.splitlines()
    for line in lines:
        seat_ids.append( seat_id(line) )

    
    seat_ids.sort(reverse=True)
    for ind, seat in enumerate(seat_ids):
        next_seat = seat_ids[ind+1]
        if seat - next_seat == 2:
            return next_seat + 1

    return -1

######################################################


INPUT_S = '''\

'''


@pytest.mark.parametrize(
    ('seat', 'expected'),
    (
        ("FBFBBFFRLR", 357),
        ("BFFFBBFRRR", 567),
        ("FFFBBBFRRR", 119),
        ("BBFFBBFRLL", 820),
    ),
)
def test_seat_id(seat: str, expected: int) -> None:
    assert seat_id(seat) == expected


def test_row() -> None:
    assert row("FBFBBFF") == 44


def test_col() -> None:
    assert col("RLR") == 5


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument('data_file', nargs='?', default=INPUT_TXT)
    args = parser.parse_args()

    with open(args.data_file) as f, timing():
        print(compute(f.read()))

    return 0


if __name__ == '__main__':
    exit(main())
