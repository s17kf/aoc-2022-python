#!/usr/bin/env python3

import time
from collections import defaultdict

import numpy as np

import common

EMPTY = 0
ELF = 1


def add_west_east_x_if_possible(x, size, x_to_check):
    if x > 0:
        x_to_check.append(x - 1)
    if x < size - 1:
        x_to_check.append(x + 1)


def add_north_south_y_if_possible(y, size, y_to_check):
    add_west_east_x_if_possible(y, size, y_to_check)


def has_any_neighbour(grove, x, y, size):
    x_to_check, y_to_check = [x], [y]
    add_west_east_x_if_possible(x, size, x_to_check)
    add_north_south_y_if_possible(y, size, y_to_check)
    for nx in x_to_check:
        for ny in y_to_check:
            if nx == x and ny == y:
                continue
            if grove[ny, nx] == ELF:
                return True
    return False


def is_north_valid(grove, x, y, size):
    if y == 0:
        return False, (0, 0)
    x_to_check = [x]
    add_west_east_x_if_possible(x, size, x_to_check)
    for nx in x_to_check:
        if grove[y - 1, nx] == ELF:
            return False, (0, 0)
    return True, (-1, 0)


def is_south_valid(grove, x, y, size):
    if y == size - 1:
        return False, (0, 0)
    x_to_check = [x]
    add_west_east_x_if_possible(x, size, x_to_check)
    for nx in x_to_check:
        if grove[y + 1, nx] == ELF:
            return False, (0, 0)
    return True, (1, 0)


def is_west_valid(grove, x, y, size):
    if x == 0:
        return False, (0, 0)
    y_to_check = [y]
    add_north_south_y_if_possible(y, size, y_to_check)
    for ny in y_to_check:
        if grove[ny, x - 1] == ELF:
            return False, (0, 0)
    return True, (0, -1)


def is_east_valid(grove, x, y, size):
    if x == size - 1:
        return False, (0, 0)
    y_to_check = [y]
    add_north_south_y_if_possible(y, size, y_to_check)
    for ny in y_to_check:
        if grove[ny, x + 1] == ELF:
            return False, (0, 0)
    return True, (0, 1)


def simulate(grove, size, rounds):
    for validator_offset in range(rounds):
        wanted_moves = defaultdict(lambda: [])
        for y, row in enumerate(grove):
            for x, value in enumerate(row):
                if value == EMPTY:
                    continue
                if not has_any_neighbour(grove, x, y, size):
                    continue
                for i in range(len(VALIDATORS)):
                    validator = (i + validator_offset) % len(VALIDATORS)
                    is_valid, move = VALIDATORS[validator](grove, x, y, size)
                    if is_valid:
                        dy, dx = move
                        wanted_moves[(x + dx, y + dy)].append((x, y))
                        break
        if len(wanted_moves) == 0:
            return validator_offset + 1

        for dest, sources in wanted_moves.items():
            if len(sources) > 1:
                continue
            sx, sy = sources[0]
            dx, dy = dest
            grove[sy, sx] = EMPTY
            grove[dy, dx] = ELF
        if ELF in grove[0, :] or ELF in grove[size - 1, :] or ELF in grove[:, 0] \
                or ELF in grove[:, size - 1]:
            print(f"!!!!!!!!!!!!!! ELF want to escape in round {validator_offset + 1}")
    return rounds


def do_task1(grove, size):
    simulate(grove, size, 10)
    start_y = end_y = start_x = end_x = 0
    for y in range(size):
        if ELF in grove[y, :]:
            start_y = y
            break
    for y in range(size - 1, 0, -1):
        if ELF in grove[y, :]:
            end_y = y
            break
    for x in range(size):
        if ELF in grove[:, x]:
            start_x = x
            break
    for x in range(size - 1, 0, -1):
        if ELF in grove[:, x]:
            end_x = x
            break

    return (end_y - start_y + 1) * (end_x - start_x + 1) - sum(
        sum(grove[start_y:end_y + 1, start_x: end_x + 1]))


VALIDATORS = [is_north_valid, is_south_valid, is_west_valid, is_east_valid]
OFFSET = 60


def main():
    input_lines = common.init_day(23)
    if input_lines is None:
        exit(1)

    size = len(input_lines) + 2 * OFFSET
    grove = np.zeros((size, size), dtype=np.int8)

    for y, line in enumerate(input_lines):
        for x, c in enumerate(line):
            if c == "#":
                grove[y + OFFSET, x + OFFSET] = ELF

    print(f"task1: {do_task1(grove.copy(), size)}")
    print(f"task2: {simulate(grove, size, 10000000000000)}")


start_time = time.time()
main()
print("--- %s seconds ---" % (time.time() - start_time))
