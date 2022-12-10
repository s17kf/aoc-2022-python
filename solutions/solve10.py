#!/bin/bash
"""exec" "pyenv" "exec" "python" "$0" "$@"""

import common


def try_print(cycle, x, image):
    if cycle % 40 in [x - 1, x, x + 1]:
        image[int(cycle / 40)][cycle % 40] = '#'


def main():
    input_lines = common.init_day(10)
    if input_lines is None:
        exit(1)

    x = 1
    interesting_cycles = [20, 60, 100, 140, 180, 220]
    image = [['.' for _ in range(40)] for _ in range(6)]
    signals = []
    cycle = 0
    for line in input_lines:
        cycle += 1
        if cycle >= 240:
            break
        operation = line.split()

        if cycle in interesting_cycles:
            signals.append(x * cycle)
        try_print(cycle, x, image)

        if operation[0] == "noop":
            continue

        cycle += 1
        if cycle >= 240:
            break
        if cycle in interesting_cycles:
            signals.append(x * cycle)
        x += int(operation[1])
        try_print(cycle, x, image)

    print(f"task1: {sum(signals)}")
    print(f"task2:")
    for row in image:
        print(' '.join(row))


main()
