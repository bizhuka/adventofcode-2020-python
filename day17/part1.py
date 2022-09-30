import argparse
import os.path
from typing import Counter
from collections import namedtuple
from support import timing

INPUT_TXT = os.path.join(os.path.dirname(__file__), 'input.txt')

######################################################


class State:
    active = '#'
    inactive = '.'


Axis = namedtuple('Axis', ['x', 'y', 'z'])


def get_active_cubes(input, z=0) -> set[Axis]:
    result = set()
    for y, line in enumerate(input.splitlines()):
        for x, char in enumerate(line):
            if char == State.active:
                result.add(Axis(x, y, z))
    return result


def get_shits() -> list[Axis]:
    result = []
    shifts = [-1, 0, 1]
    for x in shifts:
        for y in shifts:
            for z in shifts:
                if x != 0 or y != 0 or z != 0:
                    result.append(Axis(x, y, z))
    return result


def compute(s: str, times: int = 6) -> int:
    active_cubes = get_active_cubes(s)
    shits = get_shits()

    for _ in range(times):
        counter: Counter[Axis] = Counter()
        for cube in active_cubes:
            for shift in shits:
                counter[Axis(cube.x + shift.x,
                             cube.y + shift.y,
                             cube.z + shift.z)] += 1

        new_cubes = set()
        for cube, value in counter.items():
            if value == 3 and cube not in active_cubes:
                new_cubes.add(cube)

        for cube in active_cubes:
            if counter[cube] in {2, 3}:
                new_cubes.add(cube)

        active_cubes = new_cubes

    return len(active_cubes)

######################################################


INPUT_S = '''
.#.
..#
###
'''


def test() -> None:
    z_m1 = get_active_cubes("#..\n..#\n.#.", z=-1)
    z_0 = get_active_cubes("#.#\n.##\n.#.")
    z_p1 = get_active_cubes("#..\n..#\n.#.", z=1)

    assert compute(INPUT_S, times=1) == len(z_m1) + len(z_0) + len(z_p1)
    assert compute(INPUT_S, times=6) == 112


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument('data_file', nargs='?', default=INPUT_TXT)
    args = parser.parse_args()

    with open(args.data_file) as f, timing():
        print(compute(f.read()))

    return 0


if __name__ == '__main__':
    exit(main())
