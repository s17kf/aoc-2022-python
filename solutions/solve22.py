#!/usr/bin/env python3
import re

import common

EMPTY = "o"
RIGHT = (1, 0)
LEFT = (-1, 0)
DOWN = (0, 1)
UP = (0, -1)
DIRECTIONS = [RIGHT, DOWN, LEFT, UP]
DIRECTION_VALUES = {
    RIGHT: 0,
    DOWN: 1,
    LEFT: 2,
    UP: 3
}


def get_column(matrix, i):
    return [row[i] for row in matrix]


def change_direction(direction, letter):
    diff = 1 if letter == "R" else -1
    return (direction + diff) % len(DIRECTIONS)


def move(tiles, position, steps, direction, width, height):
    x, y = position
    dx, dy = direction
    for _ in range(steps):
        temp_x, temp_y = x + dx, y + dy
        if tiles[temp_y % height][temp_x % width] == ".":
            x, y = temp_x, temp_y
            continue
        while tiles[temp_y % height][temp_x % width] == EMPTY:
            temp_x += dx
            temp_y += dy
        if tiles[temp_y % height][temp_x % width] == "#":
            return x % width, y % height
        x, y = temp_x, temp_y
    return x % width, y % height


def main():
    input_lines = common.init_day(22)
    if input_lines is None:
        exit(1)

    numbers = re.split("[RL]", input_lines[-1])
    letters = [c for c in re.split("[\d]+", input_lines[-1]) if c != ""]

    print(f"R: {''.join(letters).count('R')}")
    print(f"L: {''.join(letters).count('L')}")

    tiles = input_lines[0:-2]

    max_line_length = 0
    for line in tiles:
        if len(line) > max_line_length:
            max_line_length = len(line)

    for i in range(len(tiles)):
        while (len(tiles[i])) < max_line_length:
            tiles[i] += " "
        tiles[i] = tiles[i].replace(" ", EMPTY)

    x = y = 0
    for c in tiles[0]:
        if c == ".":
            break
        x += 1

    print(x)
    width = len(tiles[0])
    print(width)
    height = len(tiles)

    direction = 0
    for steps in numbers:
        x, y = move(tiles, (x, y), int(steps), DIRECTIONS[direction], width, height)

        if len(letters) > 0:
            direction = change_direction(direction, letters.pop(0))

    print(letters)
    print(x, y, direction)
    result1 = 1000 * (y + 1) + 4 * (x + 1) + direction

    result2 = 1

    print(f"task1: {result1}")
    print(f"task2: {result2}")


main()
