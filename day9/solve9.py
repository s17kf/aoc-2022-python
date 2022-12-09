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

table = [ [ 0 for y in range( 2000 ) ] for x in range( 2000 ) ]

head = [999, 999]
tail = [999, 999]
table[tail[0]][tail[1]] = 1
# print(input_lines)
print(head, tail)

for move in input_lines:
    direction, length = move.split()
    # print(direction, length)
    length = int(length)
    match direction:
        case 'R':
            head[1] += length
        case 'L':
            head[1] -= length
        case 'D':
            head[0] += length
        case 'U':
            head[0] -= length
        case _:
            print(f"unsupported move '{direction}'")
    # print(abs(head [0] - tail[0]) > 1, abs(head[1] - tail[1] > 1))
    while abs(head [0] - tail[0]) > 1 or abs(head[1] - tail[1]) > 1:
        if head[0] - tail[0] > 0:
            tail[0] += 1
        elif head[0] - tail[0] < 0:
            tail[0] -= 1
        if head[1] - tail[1] > 0:
            tail[1] += 1
        elif head[1] - tail[1] < 0:
            tail[1] -= 1
        table[tail[0]][tail[1]] = 1
        # print(head, tail)

# for row in table:
#     print(row)

print(head)
print(tail)

result1 = sum([sum(row) for row in table])
result2 = 1

print(f"task1: {result1}")
print(f"task2: {result2}")
