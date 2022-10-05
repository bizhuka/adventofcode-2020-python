import argparse
import os.path
from attr import has
import pytest

from support import timing

INPUT_TXT = os.path.join(os.path.dirname(__file__), 'input.txt')

######################################################


def compute(s: str) -> int:
    player1_s, player2_s = s.split('\n\n', maxsplit=1)
    player1: list[int] = [int(line) for line in player1_s.splitlines()
                          if line.isnumeric()]
    player2: list[int] = [int(line) for line in player2_s.splitlines()
                          if line.isnumeric()]

    sub_game(player1, player2)

    return count_score(player1) + count_score(player2)


def count_score(arr: list[int]) -> int:
    return sum([num * (len(arr) - ind) for ind, num in enumerate(arr)])


def sub_game(player1: list[int], player2: list[int]) -> bool:
    hashes: set[str] = set()
    while len(player1) > 0 and len(player2) > 0:
        _hash = f"{ hash(tuple(player1)) } - { hash(tuple(player2)) }"
        if _hash in hashes:
            return True
        hashes.add(_hash)

        num1, num2 = player1.pop(0), player2.pop(0)
        first_win = num1 > num2

        if len(player1) + 1 > num1 and len(player2) + 1 > num2:
            first_win = sub_game(player1[:num1], player2[:num2])

        if first_win:
            player1.extend([num1, num2])
        else:
            player2.extend([num2, num1])

    return bool(player1)
######################################################


INPUT_S = '''\
Player 1:
9
2
6
3
1

Player 2:
5
8
4
7
10
'''


@pytest.mark.parametrize(
    ('input_s', 'expected'),
    (
        (INPUT_S, 291),
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
