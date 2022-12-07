#!/bin/bash
"""exec" "pyenv" "exec" "python" "$0" "$@"""

import common
from enum import Enum, auto
from collections import Counter
import numpy
from common import numpy_matrix

HELP_INFO = [
    "Script is solving task 2 of advent of code 2021",
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

A, B, C, X, Y, Z = "A", "B", "C", "X", "Y", "Z"
x, y, z = 1, 2, 3

points_for_shape = {
    X: {
        A: [x + 3, z],
        B: [x, x],
        C: [x + 6, y]
    },
    Y: {
        A: [y + 6, x + 3],
        B: [y + 3, y + 3],
        C: [y, z + 3]
    },
    Z: {
        A: [z, y + 6],
        B: [z + 6, z + 6],
        C: [z + 3, x + 6]
    }
}

scores = [[], []]
for line in input_lines:
    opponent_shape, your_shape = line.split()
    scores[0].append(points_for_shape[your_shape][opponent_shape][0])
    scores[1].append(points_for_shape[your_shape][opponent_shape][1])

result1 = sum(scores[0])
result2 = sum(scores[1])

print(f"task1: {result1}")
print(f"task2: {result2}")
