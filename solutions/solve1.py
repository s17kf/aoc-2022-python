#!/bin/bash
"""exec" "pyenv" "exec" "python" "$0" "$@"""

import common

HELP_INFO = [
    "Script is solving task 1 of advent of code 2021",
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

reindeer_to_snacks = common.get_list_of_groups_divided_empty_line(input_lines)

reindeer_to_calories = []
for snacks in reindeer_to_snacks:
    reindeer_to_calories.append(sum(int(snack) for snack in snacks.split()))

result1 = max(reindeer_to_calories)
result2 = sum(sorted(reindeer_to_calories, reverse=True)[:3])

print(f"task1: {result1}")
print(f"task2: {result2}")
