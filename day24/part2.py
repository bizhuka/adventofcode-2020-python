import argparse
from dataclasses import dataclass
import os.path
import collections
from typing import Dict, Set, Tuple, Counter
import re
import pytest

from support import timing

INPUT_TXT = os.path.join(os.path.dirname(__file__), 'input.txt')

######################################################


def compute(input: str, times: int) -> int:
    adjacents: Dict[str, Tuple[int, int, int]] = {
        'e': (1, 0, -1),
        'se': (0, 1, -1),
        'sw': (-1, 1, 0),
        'w': (-1, 0, 1),
        'nw': (0, -1, 1),
        'ne': (1, -1, 0)
    }

    def get_black_cubes(input_s) -> Set[Tuple[int, int, int]]:
        cubes = set()
        dirs = re.compile('se|sw|nw|ne|e|w')
        for line in input_s.splitlines():
            x = y = z = 0
            for dir in dirs.findall(line):
                dx, dy, dz = adjacents[dir]
                x += dx
                y += dy
                z += dz
            # or cubes ^= {(x, y, z)}
            cubes = cubes.symmetric_difference({(x, y, z)})
        return cubes

    def calc_counts(black_cubes: Set[Tuple[int, int, int]]) -> Counter[Tuple[int, int, int]]:
        result = collections.Counter()
        for x, y, z in black_cubes:
            for dx, dy, dz in adjacents.values():
                result[(x+dx, y+dy, z+dz)] += 1
        return result

    black_cubes = get_black_cubes(input)
    for _ in range(times):
        counts = calc_counts(black_cubes)

        minus = set()
        for cube in black_cubes:
            if counts[cube] == 0 or counts[cube] > 2:
                minus.add(cube)

        plus = set()
        for cube, count in counts.items():
            if count == 2 and cube not in black_cubes:
                plus.add(cube)

        # black_cubes -= minus
        # black_cubes |= plus
        black_cubes.difference_update(minus)
        black_cubes.update(plus)

    return len(black_cubes)

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
    ('input_s', 'results'),
    (
        (INPUT_S, {1: 15,
                   2: 12,
                   3: 25,
                   4: 14,
                   5: 23,
                   6: 28,
                   7: 41,
                   8: 37,
                   9: 49,
                   10: 37,
                   20: 132,
                   30: 259,
                   40: 406,
                   50: 566,
                   60: 788,
                   70: 1106,
                   80: 1373,
                   90: 1844,
                   100: 2208}),
    ),
)
def test(input_s: str, results: Dict[int, int]) -> None:
    for day, result in results.items():
        assert compute(input_s, day) == result


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument('data_file', nargs='?', default=INPUT_TXT)
    args = parser.parse_args()

    with open(args.data_file) as f, timing():
        print(compute(f.read(), 100))

    return 0


if __name__ == '__main__':
    exit(main())
