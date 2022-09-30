import argparse
from dataclasses import dataclass, field
import os.path
from typing import Set, List
import pytest
from pprint import pprint
from math import prod
from support import timing

INPUT_TXT = os.path.join(os.path.dirname(__file__), 'input.txt')

######################################################


@dataclass
class Note:
    name: str
    scope: Set[int] = field(default_factory=lambda: set())

    columns: Set[int] = field(default_factory=lambda: set())
    column: int = None

    def __init__(self, name: str) -> None:
        self.name = name
        self.scope = set()
        self.columns = set()
        self.column = None


class Solution:
    correct_tickets: list[list[int]]
    notes: dict[str, Note]

    def __init__(self, input) -> None:
        self.correct_tickets = list()
        self.notes = dict()

        mode = 0
        modes = {'your ticket:': 1,  'nearby tickets:': 2}
        for line in input.replace('\n\n', '\n').splitlines():
            if line in modes.keys():
                mode = modes[line]
                continue

            if mode == 0:
                name, diap = line.split(": ", maxsplit=1)
                note = Note(name)
                self.notes[name] = note
                for ranges in diap.split(" or "):
                    _from, _to = ranges.split("-")
                    note.scope.update(range(int(_from), int(_to)+1))
                continue

            check_ticket = [int(num) for num in line.split(",")]
            ok = True
            if mode == 2:
                for number in check_ticket:
                    count = sum(
                        1 for note in self.notes.values() if number not in note.scope)
                    if count == len(self.notes):
                        ok = False
                        break
            if ok:
                self.correct_tickets.append(check_ticket)

    def detect_column(self) -> None:
        for note in self.notes.values():
            for column in range(len(self.notes)):
                ok = True
                for correct_ticket in self.correct_tickets:
                    number = correct_ticket[column]
                    if number not in note.scope:
                        ok = False
                        break
                if ok:
                    note.columns.add(column)

        changed = True
        while changed:
            changed = False

            for note in self.notes.values():
                if note.column is not None or len(note.columns) != 1:
                    continue

                note.column = note.columns.pop()
                changed = True

                for note_exclude in self.notes.values():
                    if note_exclude.column is not None or not note_exclude.columns:
                        continue
                    note_exclude.columns.discard(note.column)

    def multiply(self, needle: str) -> int:
        my_ticket = self.correct_tickets[0]
        return prod([my_ticket[dep_note.column]
                     for dep_note in self.notes.values() if dep_note.name.startswith(needle)])


def compute(input: str) -> int:
    solution = Solution(input)
    solution.detect_column()
    return solution.multiply('departure')

######################################################


INPUT_S = '''\
class: 0-1 or 4-19
row: 0-5 or 8-19
seat: 0-13 or 16-19

your ticket:
11,12,13

nearby tickets:
3,9,18
15,1,5
5,14,9
'''


def test() -> None:
    solution = Solution(INPUT_S)
    solution.detect_column()

    results = {'class': 12, 'row': 11, 'seat': 13}
    my_ticket = solution.correct_tickets[0]
    for key, value in results.items():
        assert my_ticket[solution.notes[key].column] == value


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument('data_file', nargs='?', default=INPUT_TXT)
    args = parser.parse_args()

    with open(args.data_file) as f, timing():
        pprint(compute(f.read()))

    return 0


if __name__ == '__main__':
    exit(main())
