#!/bin/bash
"""exec" "pyenv" "exec" "python" "$0" "$@"""

import common

input_lines = common.init_day(2)
if input_lines is None:
    exit(1)

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
