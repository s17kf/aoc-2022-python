#!/bin/bash
"""exec" "pyenv" "exec" "python" "$0" "$@"""

import common

input_lines = common.init_day(4)
if input_lines is None:
    exit(1)

section_pairs = []
for line in input_lines:
    numbers = []
    for sections in line.split(','):
        for number in sections.split('-'):
            numbers.append(int(number))
    section_pairs.append((set(range(numbers[0], numbers[1] + 1)),
                          set(range(numbers[2], numbers[3] + 1))))

fully_overlapped_count = 0
somehow_overlapped_count = 0
for sections in section_pairs:
    if sections[0].issubset(sections[1]) or sections[1].issubset(sections[0]):
        fully_overlapped_count += 1
    if len(sections[0].intersection(sections[1])) > 0:
        somehow_overlapped_count += 1

print(f"task1: {fully_overlapped_count}")
print(f"task2: {somehow_overlapped_count}")
