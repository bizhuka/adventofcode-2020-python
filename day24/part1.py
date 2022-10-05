import argparse
from dataclasses import dataclass
import os.path
from typing import Dict, Set, Tuple
import re
import pytest

from support import timing

INPUT_TXT = os.path.join(os.path.dirname(__file__), 'input.txt')

######################################################


def compute(s: str) -> int:
    adjacents: Dict[str, Tuple[int, int, int]] = {
        'e': (1, 0, -1),
        'se': (0, 1, -1),
        'sw': (-1, 1, 0),
        'w': (-1, 0, 1),
        'nw': (0, -1, 1),
        'ne': (1, -1, 0)
    }
    cubes: Set[Tuple[int, int, int]] = set()

    dirs = re.compile('se|sw|nw|ne|e|w')
    for line in s.splitlines():
        x = y = z = 0
        for dir in dirs.findall(line):
            dx, dy, dz = adjacents[dir]
            x += dx
            y += dy
            z += dz
        # or cubes ^= {(x, y, z)}
        cubes = cubes.symmetric_difference({(x, y, z)})

    return len(cubes)

######################################################


INPUT_S = '''\
sesenwnenenewseeswwswswwnenewsewsw
neeenesenwnwwswnenewnwwsewnenwseswesw
seswneswswsenwwnwse
nwnwneseeswswnenewneswwnewseswneseene
swweswneswnenwsewnwneneseenw
eesenwseswswnenwswnwnwsewwnwsene
sewnenenenesenwsewnenwwwse
wenwwweseeeweswwwnwwe
wsweesenenewnwwnwsenewsenwwsesesenwne
neeswseenwwswnwswswnw
nenwswwsewswnenenewsenwsenwnesesenew
enewnwewneswsewnwswenweswnenwsenwsw
sweneswneswneneenwnewenewwneswswnese
swwesenesewenwneswnwwneseswwne
enesenwswwswneneswsenwnewswseenwsese
wnwnesenesenenwwnenwsewesewsesesew
nenewswnwewswnenesenwnesewesw
eneswnwswnwsenenwnwnwwseeswneewsenese
neswnwewnwnwseenwseesewsenwsweewe
wseweeenwnesenwwwswnew
'''


@pytest.mark.parametrize(
    ('input_s', 'expected'),
    (
        (INPUT_S, 10),
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
