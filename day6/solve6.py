#!/bin/bash
"""exec" "pyenv" "exec" "python" "$0" "$@"""

import common

HELP_INFO = [
    "Script is solving task 6 of advent of code 2021",
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


def find_marker_end_index(characters, marker_length):
    marker = []
    for i, char in enumerate(characters):
        marker = (marker + [char])[-marker_length:]
        if len(set(marker)) == marker_length:
            return i + 1


sequence = input_lines[0]
result1 = find_marker_end_index(sequence, 4)
result2 = find_marker_end_index(sequence, 14)

print(f"task1: {result1}")
print(f"task2: {result2}")
