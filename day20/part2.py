import argparse
from dataclasses import dataclass
from math import sqrt
import os.path
from pprint import pprint
from turtle import right
from typing import List, Dict
import collections
import pytest

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

    def set_borders(self) -> List[str]:
        # Left, Top, Right, Bottom
        self.borders = [''.join(map(lambda line: line[0], self.field)),
                        ''.join(self.field[0]),
                        ''.join(map(lambda line: line[-1], self.field)),
                        ''.join(self.field[-1])]
        return self.borders


def get_border_id(border: str) -> str:
    return max(border, border[::-1])


def all_combinations(field: List[List[str]]) -> List[List[str]]:
    def rotate90(field: List[List[str]]) -> List[List[str]]:
        size = len(field)
        return [[field[y][size - 1 - x] for y in range(size)] for x in range(size)]

    def flip(field: List[List[str]]) -> List[List[str]]:
        size = len(field)
        return [[field[y][x] for y in range(size)] for x in range(size)]

    for _ in range(2):
        for _ in range(4):
            yield field
            field = rotate90(field)
        field = flip(field)


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
    corners = [tile_id for tile_id, cnt in counter.items() if cnt == 2]

    # part2
    char_width = len(tiles[tile_id].borders[0]) - 2
    size = int(sqrt(len(tiles)))
    all_field = [[' '] * (size * char_width) for i in range(size * char_width)]

    def set_field(tile: Tile, x: int, y: int):
        for dx in range(char_width):
            for dy in range(char_width):
                all_field[x * char_width + dx][y * char_width + dy] = \
                    tile.field[dx + 1][dy + 1]

    def get_other_match_tile(tile: Tile, border_id: str) -> Tile:
        arr = matches[border_id]
        assert len(arr) == 2 and tile.id in arr
        return tiles[sum(arr) - tile.id]

    def set_tile(tile: Tile, x: int, y: int, left: str = '', top: str = '') -> None:
        for tile.field in all_combinations(tile.field):
            _left, _top, _right, _bottom = tile.set_borders()
            if (left and left != _left) or (top and top != _top):
                continue
            set_field(tile, x, y)

            if size > y + 1:
                borderTile = get_other_match_tile(tile, get_border_id(_right))
                set_tile(borderTile, x, y + 1, left=_right)
            if y == 0 and size > x + 1:
                borderTile = get_other_match_tile(tile, get_border_id(_bottom))
                set_tile(borderTile, x + 1, y, top=_bottom)
            return

    cornerTile = tiles[corners[0]]
    for cornerTile.field in all_combinations(cornerTile.field):
        if all(map(lambda b: len(matches[get_border_id(b)]) == 1, cornerTile.set_borders()[:2])):
            set_tile(cornerTile, 0, 0,
                     left=cornerTile.borders[0],
                     top=cornerTile.borders[1])

    # find all monsters
    monster = ['                  # ',
               '#    ##    ##    ###',
               ' #  #  #  #  #  #   ']

    def get_roughness(field_comb: List[List[str]]) -> int:
        monsters_count = 0
        for x in range(size * char_width - len(monster)):
            for y in range(size * char_width - len(monster[0])):
                if all([monster[dx][dy] != '#' or field_comb[x + dx][y + dy] == '#'
                        for dy in range(len(monster[0]))
                        for dx in range(len(monster))]):
                    monsters_count += 1

                    for dx in range(len(monster)):
                        for dy in range(len(monster[0])):
                            if monster[dx][dy] == '#':
                                field_comb[x + dx][y + dy] = 'O'
        if monsters_count == 0:
            return 0
        return sum(map(lambda s: ''.join(s).count('#'), field_comb))

    return sum(map(get_roughness, all_combinations(all_field)))

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
        (INPUT_S, 273),
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
