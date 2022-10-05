import argparse
from dataclasses import dataclass
import os.path
from typing import List, Dict
import math
import collections
import pytest
import re

from support import timing

INPUT_TXT = os.path.join(os.path.dirname(__file__), 'input.txt')

######################################################

@dataclass
class Tile:
    id: int
    field: List[List[str]]
    borders: List[str]

    def __init__(self, input: str) -> None:
        lines = input.split('\n')
        self.id = int(lines[0].split(' ')[1].strip(':'))
        self.field = Tile.get_as_field(lines[1:])
        self.set_borders()

    @classmethod
    def get_as_field(cls, arr: List[str]) -> List[List[str]]:
        return list(map(list, arr))

    def set_borders(self):
        # Left, Top, Right, Bottom
        self.borders = [''.join(map(lambda line: line[0], self.field)),
                        ''.join(self.field[0]),
                        ''.join(map(lambda line: line[-1], self.field)),
                        ''.join(self.field[-1])]


def get_border_id(border: str) -> str:
    return max(border, border[::-1])


def compute(s: str) -> int:
    tiles: Dict[int, Tile] = dict()
    for line in s.split('\n\n'):
        tile = Tile(line)
        tiles[tile.id] = tile

    matches = dict()
    for tile in tiles.values():
        for border in tile.borders:
            matches.setdefault(get_border_id(border), []).append(tile.id)

    counter = collections.Counter()
    for tile_id in [match[0] for match in matches.values() if len(match) == 1]:
        counter[tile_id] += 1

    return math.prod([tile_id for tile_id, cnt in counter.items() if cnt == 2])

######################################################


INPUT_S = '''\
Tile 2311:
..##.#..#.
##..#.....
#...##..#.
####.#...#
##.##.###.
##...#.###
.#.#.#..##
..#....#..
###...#.#.
..###..###

Tile 1951:
#.##...##.
#.####...#
.....#..##
#...######
.##.#....#
.###.#####
###.##.##.
.###....#.
..#.#..#.#
#...##.#..

Tile 1171:
####...##.
#..##.#..#
##.#..#.#.
.###.####.
..###.####
.##....##.
.#...####.
#.##.####.
####..#...
.....##...

Tile 1427:
###.##.#..
.#..#.##..
.#.##.#..#
#.#.#.##.#
....#...##
...##..##.
...#.#####
.#.####.#.
..#..###.#
..##.#..#.

Tile 1489:
##.#.#....
..##...#..
.##..##...
..#...#...
#####...#.
#..#.#.#.#
...#.#.#..
##.#...##.
..##.##.##
###.##.#..

Tile 2473:
#....####.
#..#.##...
#.##..#...
######.#.#
.#...#.#.#
.#########
.###.#..#.
########.#
##...##.#.
..###.#.#.

Tile 2971:
..#.#....#
#...###...
#.#.###...
##.##..#..
.#####..##
.#..####.#
#..#.#..#.
..####.###
..#.#.###.
...#.#.#.#

Tile 2729:
...#.#.#.#
####.#....
..#.#.....
....#..#.#
.##..##.#.
.#.####...
####.#.#..
##.####...
##..#.##..
#.##...##.

Tile 3079:
#.#.#####.
.#..######
..#.......
######....
####.#..#.
.#...#.##.
#.#####.##
..#.###...
..#.......
..#.###...'''


@pytest.mark.parametrize(
    ('input_s', 'expected'),
    (
        (INPUT_S, 20899048083289),
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
