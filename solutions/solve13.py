#!/usr/bin/env python3

import math
from functools import cmp_to_key

import common


def parse_array(array_line: str):
    parsed = []
    array = array_line.split(",")
    level = 0
    last_array = parsed
    for i, element in enumerate(array):
        while len(element) > 0 and element[0] == "[":
            level += 1
            last_array.append([])
            last_array = last_array[-1]
            element = element[1:]
        value = element.rstrip("]")
        if len(value) > 0:
            last_array.append(int(value))
        closed_lists = 0
        while len(element) > 0 and element[-1] == "]":
            closed_lists += 1
            element = element[:-1]
            level -= 1
        last_array = parsed
        for _ in range(level):
            last_array = last_array[-1]
    return parsed


def compare_arrays(a1, a2):
    for i in range(min(len(a1), len(a2))):
        e1 = a1[i]
        e2 = a2[i]
        if isinstance(e1, int) and isinstance(e2, int):
            if e1 == e2:
                continue
            else:
                return e1 - e2
        elif isinstance(e1, list) and isinstance(e2, list):
            result = compare_arrays(e1, e2)
            if result == 0:
                continue
        elif isinstance(e1, list):
            result = compare_arrays(e1, [e2])
            if result == 0:
                continue
        else:
            result = compare_arrays([e1], e2)
            if result == 0:
                continue
        return result
    return len(a1) - len(a2)


input_lines = common.init_day(13)
if input_lines is None:
    exit(1)

pairs = common.get_list_of_groups_divided_empty_line(input_lines, ";")

for i in range(0):
    print("rangeTest")

good_order = []
for i, pair in enumerate(pairs):
    left, right = pair.split(";")
    left = left[1:-1]
    right = right[1:-1]
    left = parse_array(left)
    right = parse_array(right)
    if compare_arrays(left, right) < 0:
        good_order.append(i + 1)

signals = []
for pair in pairs:
    for signal in pair.split(";"):
        signals.append(parse_array(signal))

divider_packets = [[[2]], [[6]]]
signals += divider_packets

signals.sort(key=cmp_to_key(compare_arrays))

divider_indices = []
for i, signal in enumerate(signals):
    if signal in divider_packets:
        divider_indices.append(i + 1)

result1 = sum(good_order)
result2 = math.prod(divider_indices)

print(f"task1: {result1}")
print(f"task2: {result2}")
