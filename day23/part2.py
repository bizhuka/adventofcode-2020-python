import argparse
import os.path
from platform import node
from unittest import result
from collections import deque
from typing import List
# import pytest
# from support import timing

INPUT_TXT = os.path.join(os.path.dirname(__file__), 'input.txt')

######################################################


def compute(input: str, count) -> str:
    nodes = [0] * (len(input) if count != 1_000_000 * 10 else 1_000_000)

    current_cup = int(input[0])
    for ind, ch in enumerate(input):
        next_cup = current_cup if len(input) - 1 == ind else int(input[ind+1])
        nodes[int(ch) - 1] = next_cup

    if count == 1_000_000 * 10:
        nodes[int(ch) - 1] = len(input) + 1
        for cup_index in range(len(input), 1_000_000):
            nodes[cup_index] = cup_index + 2
        nodes[len(nodes) - 1] = current_cup

    for _ in range(count):
        splice1 = nodes[current_cup - 1]
        splice2 = nodes[splice1 - 1]
        splice3 = nodes[splice2 - 1]

        next1 = nodes[splice3 - 1]
        nodes[current_cup - 1] = next1

        number = current_cup
        while True:
            number -= 1
            if number == 0:
                number = len(nodes)
            if number != splice1 and number != splice2 and number != splice3:
                break
        nodes[splice3 - 1] = nodes[number - 1]
        nodes[number - 1] = splice1

        current_cup = next1

    if count == 1_000_000 * 10:
        num1 = nodes[0]
        return num1 * nodes[num1 - 1]

    return nodes_to_str(nodes, current_cup, count)


def nodes_to_str(nodes: List[int], current_cup, count) -> str:
    result = deque()
    while True:
        number = nodes[current_cup - 1]
        if number == 0:
            break
        result.append(str(current_cup))
        nodes[current_cup - 1] = 0
        current_cup = number

    final_result = count >= 100
    if final_result:
        count = -1 * result.index('1')
    result.rotate(count)

    return "".join(result)[1 if final_result else 0:]
######################################################


# @pytest.mark.parametrize(
#     ('input_s', 'expected'),
#     (
#         ('389125467', ['328915467', '325467891', '725891346', '325846791', '925841367',
#                        '725841936', '836741925', '741583926', '574183926', '583741926']),
#     ),
# )
# def test(input_s: str, expected: int) -> None:
#     for ind, num in enumerate(expected):
#         assert compute(input_s, ind + 1) == num


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument('data_file', nargs='?', default=INPUT_TXT)
    args = parser.parse_args()

    with open(args.data_file) as f: #, timing():
        print(compute(f.read(), 1_000_000 * 10))

    return 0


if __name__ == '__main__':
    exit(main())
