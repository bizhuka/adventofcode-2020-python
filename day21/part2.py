import argparse
from dataclasses import dataclass
import os.path
from pprint import pprint

import pytest

from support import timing

INPUT_TXT = os.path.join(os.path.dirname(__file__), 'input.txt')

######################################################


@dataclass
class Food:
    ingredients: set[str]
    allergens: set[str]

    def __init__(self, line: str) -> None:
        ingredients, allergens = line.split(' (contains ', maxsplit=1)
        self.ingredients = set(ingredients.split())
        self.allergens = set(allergens[:-1].split(', '))


@dataclass
class Part2:
    ingredient: str
    allergen: str


def compute(s: str) -> int:
    foods: list[Food] = [Food(line) for line in s.splitlines()]
    parts: list[Part2] = list()

    def delete_both(allergen, ingredient) -> None:
        for food in foods:
            food.ingredients.discard(ingredient)
            food.allergens.discard(allergen)
        parts.append(Part2(ingredient, allergen))

    changed = True
    while changed:
        changed = False

        for food in foods:
            if len(food.allergens) != 1:
                continue

            allergen = list(food.allergens)[0]
            if len(food.ingredients) == 1:
                changed = True
                delete_both(allergen, food.ingredients.pop())
                continue

            inter_set = food.ingredients.copy()
            for food_compare in foods:
                if food is food_compare or allergen not in food_compare.allergens:
                    continue

                inter_set = inter_set.intersection(food_compare.ingredients)
                if len(inter_set) != 1:
                    continue

                changed = True
                delete_both(allergen, inter_set.pop())

    return ",".join([part.ingredient for part in sorted(parts, key=lambda x: x.allergen)])

######################################################


INPUT_S = '''\
mxmxvkd kfcds sqjhc nhms (contains dairy, fish)
trh fvjkl sbzzf mxmxvkd (contains dairy)
sqjhc fvjkl (contains soy)
sqjhc mxmxvkd sbzzf (contains fish)
'''


@pytest.mark.parametrize(
    ('input_s', 'expected'),
    (
        (INPUT_S, 5),
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
