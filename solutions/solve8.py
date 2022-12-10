#!/bin/bash
"""exec" "pyenv" "exec" "python" "$0" "$@"""

import common
from enum import Enum, auto
from collections import Counter
import numpy
from common import numpy_matrix

HELP_INFO = [
    "Script is solving task 8 of advent of code 2021",
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


def get_column(matrix, i):
    return [row[i] for row in matrix]


def is_visible(tree, other_trees):
    for other in other_trees:
        if tree <= other:
            return False
    return True


def count_visible(tree, other_trees):
    i = 0
    for other in other_trees:
        i += 1
        if int(tree) <= int(other):
            break
    return i


visible_trees = []
visibility = []
visible_trees_count = []
for x, row in enumerate(input_lines):
    visibility.append([])
    for y, tree in enumerate(row):
        column = get_column(input_lines, y)

        # for part 1:
        if is_visible(tree, row[:y]) or is_visible(tree, row[y + 1:]) \
                or is_visible(tree, column[:x]) or is_visible(tree, column[x + 1:]):
            visible_trees.append(tree)

        # for part 2:
        visible_trees_count.append(count_visible(tree, reversed(row[:y])))
        visible_trees_count[-1] *= count_visible(tree, row[y + 1:])
        visible_trees_count[-1] *= count_visible(tree, reversed(column[:x]))
        visible_trees_count[-1] *= count_visible(tree, column[x + 1:])

result1 = len(visible_trees)
result2 = max(visible_trees_count)

print(f"task1: {result1}")
print(f"task2: {result2}")
