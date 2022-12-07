#!/bin/bash
"""exec" "pyenv" "exec" "python" "$0" "$@"""

import common
from enum import Enum, auto
from collections import Counter
import numpy
from common import numpy_matrix

HELP_INFO = [
    "Script is solving task 3 of advent of code 2021",
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


def get_priority(letter):
    return ord(letter) - ord('A') + 27 if letter < 'a' else ord(letter) - ord('a') + 1


rucksacks = [(list(rucksack[:int(len(rucksack)/2)]), list(rucksack[int(len(rucksack)/2):]))
             for rucksack in input_lines]
common_snacks = []
for rucksack in rucksacks:
    for snack in rucksack[0]:
        if snack in rucksack[1]:
            common_snacks.append(get_priority(snack))
            break

rucksacks_v2 = []
for i, rucksack in enumerate(input_lines):
    if i % 3 == 0:
        rucksacks_v2.append([])
    rucksacks_v2[-1].append(rucksack)

common_snacks_v2 = []
for group in rucksacks_v2:
    for snack in group[0]:
        if snack in group[1] and snack in group[2]:
            common_snacks_v2.append(get_priority(snack))
            break

result1 = sum(common_snacks)
result2 = sum(common_snacks_v2)

print(f"task1: {result1}")
print(f"task2: {result2}")
