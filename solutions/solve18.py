#!/usr/bin/env python3

import sys

import numpy as np

import common

SIZE = 20
ROCK = 2
AIR = 1
STEAM = 0

sys.setrecursionlimit(10000)


def get_free_sides(grid, x, y, z, free_space_value):
    free_sides = 0
    free_sides += 1 if x - 1 < 0 else 1 if grid[x - 1, y, z] == free_space_value else 0
    free_sides += 1 if y - 1 < 0 else 1 if grid[x, y - 1, z] == free_space_value else 0
    free_sides += 1 if z - 1 < 0 else 1 if grid[x, y, z - 1] == free_space_value else 0
    free_sides += 1 if x + 1 >= SIZE else 1 if grid[x + 1, y, z] == free_space_value else 0
    free_sides += 1 if y + 1 >= SIZE else 1 if grid[x, y + 1, z] == free_space_value else 0
    free_sides += 1 if z + 1 >= SIZE else 1 if grid[x, y, z + 1] == free_space_value else 0
    return free_sides


def get_neighbours(x, y, z):
    result = []
    if x > 0:
        result.append((x - 1, y, z))
    if x < SIZE - 1:
        result.append((x + 1, y, z))
    if y > 0:
        result.append((x, y - 1, z))
    if y < SIZE - 1:
        result.append((x, y + 1, z))
    if z > 0:
        result.append((x, y, z - 1))
    if z < SIZE - 1:
        result.append((x, y, z + 1))
    return result


def propagate_steam(grid, point, next_points):
    x, y, z = point
    for next_point in get_neighbours(x, y, z):
        nx, ny, nz = next_point
        if grid[nx, ny, nz] == AIR:
            next_points.append(next_point)
            grid[nx, ny, nz] = STEAM
    if len(next_points) == 0:
        return
    propagate_steam(grid, next_points.pop(0), next_points)


def count_free_sides(grid, rock, free_space_value):
    free_sides = 0
    for x in range(SIZE):
        for y in range(SIZE):
            for z in range(SIZE):
                if grid[x, y, z] == rock:
                    free_sides += get_free_sides(grid, x, y, z, free_space_value)
    return free_sides


def main():
    input_lines = common.init_day(18)
    if input_lines is None:
        exit(1)

    grid = np.ones((SIZE, SIZE, SIZE), dtype=np.int8)
    for line in input_lines:
        x, y, z = (int(c) for c in line.split(","))
        grid[x, y, z] = ROCK

    result1 = count_free_sides(grid, ROCK, AIR)
    grid[0, 0, 0] = STEAM
    propagate_steam(grid, (0, 0, 0), [])
    result2 = count_free_sides(grid, ROCK, STEAM)

    print(f"task1: {result1}")
    print(f"task2: {result2}")


main()
