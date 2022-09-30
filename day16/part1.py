import argparse
from dataclasses import dataclass, field
import os.path
from typing import Set
import pytest

from support import timing

INPUT_TXT = os.path.join(os.path.dirname(__file__), 'input.txt')

######################################################


@dataclass
class Note:
    name: str
    scope: Set[int] = field(default_factory=lambda: set())

    def __init__(self, name: str) -> None:
        self.name = name
        self.scope = set()


def compute(input: str) -> int:
    result = 0

    notes: list[Note] = []
    mode = 0
    modes = {'your ticket:': 1,  'nearby tickets:': 2}
    for line in input.replace('\n\n', '\n').splitlines():
        if line in modes.keys():
            mode = modes[line]
            continue

        match mode:
            case 0:
                name, lines = line.split(": ", maxsplit=1)
                note = Note(name)
                notes.append(note)
                for line in lines.split(" or "):
                    _from, _to = line.split("-")
                    note.scope.update(range(int(_from), int(_to)+1))
            case 1:
                pass  # skip my ticket
            case 2:
                for number in [int(num) for num in line.split(",")]:
                    count = sum(1 for note in notes if number not in note.scope)
                    if count == len(notes):
                        result += number
    return result

######################################################


INPUT_S = '''\
class: 1-3 or 5-7
row: 6-11 or 33-44
seat: 13-40 or 45-50

your ticket:
7,1,14

nearby tickets:
7,3,47
40,4,50
55,2,20
38,6,12
'''


@pytest.mark.parametrize(
    ('input_s', 'expected'),
    (
        (INPUT_S, 71),
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
