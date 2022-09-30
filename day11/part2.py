import argparse
from dataclasses import dataclass, field
import os.path
from typing import Counter
from collections import namedtuple
from support import timing

INPUT_TXT = os.path.join(os.path.dirname(__file__), 'input.txt')

######################################################


class Seat:
    empty = 'L'
    occupied = '#'
    floor = '.'


Axis = namedtuple('Axis', ['x', 'y'])


def get_seats(input) -> dict[Axis, str]:
    result = dict()
    for y, line in enumerate(input.splitlines()):
        for x, char in enumerate(line):
            result[Axis(x, y)] = char
    return result


def get_shifts() -> list[Axis]:
    result = []
    shifts = [-1, 0, 1]
    for x in shifts:
        for y in shifts:
            if x != 0 or y != 0:
                result.append(Axis(x, y))
    return result


@dataclass
class Solution:
    seats: dict[Axis, str] = field(default_factory=lambda: dict())
    y_count: int = 0
    x_count: int = 0

    def __init__(self, input: str) -> None:
        self.seats = get_seats(input)
        self.y_count = input.count("\n")
        self.x_count = len(self.seats) // (self.y_count + 1) - 1

    def part2(self, times: int = 1000000, i_occupied: int = 5) -> int:
        shifts = get_shifts()
        for _ in range(times):
            counter: Counter[Axis] = Counter()
            for key, seat in self.seats.items():
                if seat != Seat.occupied:
                    continue
                for shift in shifts:
                    x, y = key.x, key.y
                    while True:
                        x += shift.x
                        y += shift.y
                        axis = Axis(x, y)
                        if axis.x > self.x_count or axis.x < 0 or axis.y > self.y_count or axis.y < 0:
                            break
                        if self.seats[axis] == Seat.floor:
                            continue

                        counter[axis] += 1
                        break

            new_seats: dict[Axis, str] = dict()
            for key, seat in self.seats.items():
                match seat:
                    case Seat.floor:
                        pass
                    case Seat.empty:
                        if counter[key] == 0:
                            seat = Seat.occupied
                    case Seat.occupied:
                        if counter[key] >= i_occupied:
                            seat = Seat.empty

                new_seats[key] = seat

            # No change at all?
            if self.seats == new_seats:
                break

            # For next loop
            self.seats = new_seats

        return sum([1 for seat in new_seats.values() if seat == Seat.occupied])


def compute(s: str) -> int:
    solution = Solution(s)
    return solution.part2()

######################################################


def test() -> None:
    results = [
        "#.##.##.#########.###.#.#..#..####.##.###.##.##.###.#####.##..#.#.....###########.######.##.#####.##",
        "#.LL.LL.L##LLLLLL.LLL.L.L..L..LLLL.LL.LLL.LL.LL.LLL.LLLLL.LL..L.L.....LLLLLLLLL##.LLLLLL.L#.LLLLL.L#",
        "#.L#.##.L##L#####.LLL.#.#..#..##L#.##.###.##.#L.###.#####.#L..#.#.....LLL####LL##.L#####.L#.L####.L#",
        "#.L#.L#.L##LLLLLL.LLL.L.L..#..##LL.LL.L#L.LL.LL.L##.LLLLL.LL..L.L.....LLLLLLLLL##.LLLLL#.L#.L#LL#.L#",
        "#.L#.L#.L##LLLLLL.LLL.L.L..#..##L#.#L.L#L.L#.#L.L##.L####.LL..#.#.....LLL###LLL##.LLLLL#.L#.L#LL#.L#",
        "#.L#.L#.L##LLLLLL.LLL.L.L..#..##L#.#L.L#L.L#.LL.L##.LLLL#.LL..#.L.....LLL###LLL##.LLLLL#.L#.L#LL#.L#",
    ]

    for index, result in enumerate(results):
        cut = Solution(
            "L.LL.LL.LL\nLLLLLLL.LL\nL.L.L..L..\nLLLL.LL.LL\nL.LL.LL.LL\nL.LLLLL.LL\n..L.L.....\nLLLLLLLLLL\nL.LLLLLL.L\nL.LLLLL.LL")
        ret = cut.part2(index + 1)
        assert ret == result.count(Seat.occupied), f"Index = {index}"
    assert ret == 26


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument('data_file', nargs='?', default=INPUT_TXT)
    args = parser.parse_args()

    with open(args.data_file) as f, timing():
        print(compute(f.read()))

    return 0


if __name__ == '__main__':
    exit(main())
