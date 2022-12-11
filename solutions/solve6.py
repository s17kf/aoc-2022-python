#!/usr/bin/env python3
import common

input_lines = common.init_day(6)
if input_lines is None:
    exit(1)


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
