#!/bin/bash
"""exec" "pyenv" "exec" "python" "$0" "$@"""

import common

HELP_INFO = [
    "Script is solving task 9 of advent of code 2021",
    "Arguments:",
    common.TAB + "input file"
]
arguments_keywords = ["inputFile"]

script_arguments = common.parse_arguments(arguments_keywords, HELP_INFO)
if script_arguments is None:
    exit(1)

input_file_name = script_arguments["inputFile"]
print("solving file: " + input_file_name)
input_lines = common.read_lines_from_file(input_file_name)

knots = [[0, 0] for i in range(10)]
k1, k9 = {(0, 0)}, {(0, 0)}
DIRECTIONS = {
    'R': (0, 1),
    'L': (0, -1),
    'D': (1, 0),
    'U': (-1, 0)
}

for move in input_lines:
    direction, length = move.split()
    length = int(length)
    for _ in range(length):
        knots[0] = [knots[0][0] + DIRECTIONS[direction][0], knots[0][1] + DIRECTIONS[direction][1]]
        for head in range(9):
            tail = head + 1
            if abs(knots[head][0] - knots[tail][0]) > 1 or abs(knots[head][1] - knots[tail][1]) > 1:
                if knots[head][0] - knots[tail][0] > 0:
                    knots[tail][0] += 1
                elif knots[head][0] - knots[tail][0] < 0:
                    knots[tail][0] -= 1
                if knots[head][1] - knots[tail][1] > 0:
                    knots[tail][1] += 1
                elif knots[head][1] - knots[tail][1] < 0:
                    knots[tail][1] -= 1
        k1.add(tuple(knots[1]))
        k9.add(tuple(knots[9]))

result1 = len(k1)
result2 = len(k9)

print(f"task1: {result1}")
print(f"task2: {result2}")
