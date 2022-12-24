#!/usr/bin/env python3.10

import time
from collections import defaultdict

import common

EMPTY = 0
RIGHT = 0b00001
DOWN = 0b00010
LEFT = 0b00100
UP = 0b01000
WALL = 0b10000


def get_next_positions(position: tuple, walls: dict, next_positions: set,
                       source_condition, source_next: tuple):
    y, x = position
    next_positions.add((y, x))
    if source_condition(y):
        next_positions.add(source_next)
        return
    for ny in (y - 1, y + 1):
        if not walls[(ny, x)]:
            next_positions.add((ny, x))
    for nx in (x - 1, x + 1):
        if not walls[(y, nx)]:
            next_positions.add((y, nx))


def add_wind(winds: dict, wind: int, destination: tuple, destination_if_wall: tuple, walls: dict):
    if walls[destination]:
        winds[destination_if_wall] += wind
        return
    winds[destination] += wind


def go(start: tuple, end: tuple, walls: dict, winds: dict, width: int, height: int,
       start_next: tuple):
    positions = {start}
    next_positions = set()
    new_winds = defaultdict(lambda: EMPTY)
    minute = 0
    while True:
        if end in positions:
            return minute, winds
        for position in positions:
            if winds[position] != EMPTY:
                continue
            get_next_positions(position, walls, next_positions, lambda v: v == start[0],
                               start_next)
        for (y, x), wind in winds.items():
            if wind == EMPTY:
                continue
            if wind & RIGHT:
                add_wind(new_winds, RIGHT, (y, x + 1), (y, 1), walls)
            if wind & LEFT:
                add_wind(new_winds, LEFT, (y, x - 1), (y, width - 2), walls)
            if wind & DOWN:
                add_wind(new_winds, DOWN, (y + 1, x), (1, x), walls)
            if wind & UP:
                add_wind(new_winds, UP, (y - 1, x), (height - 2, x), walls)

        minute += 1
        winds = new_winds
        new_winds = defaultdict(lambda: EMPTY)
        positions = next_positions
        next_positions = set()


def main():
    input_lines = common.init_day(24)
    if input_lines is None:
        exit(1)

    width = len(input_lines[0])
    height = len(input_lines)

    walls = defaultdict(lambda: False)
    winds = defaultdict(lambda: EMPTY)
    for y, line in enumerate(input_lines):
        for x, c in enumerate(line):
            match c:
                case '#':
                    walls[(y, x)] = True
                case '>':
                    winds[(y, x)] = RIGHT
                case '<':
                    winds[(y, x)] = LEFT
                case 'v':
                    winds[(y, x)] = DOWN
                case '^':
                    winds[(y, x)] = UP

    go_time, winds = go((0, 1), (height - 1, width - 2), walls, winds, width, height, (1, 1))
    go_back_time, winds = go((height - 1, width - 2), (0, 1), walls, winds, width, height,
                             (height - 2, width - 2))
    go_again_time, winds = go((0, 1), (height - 1, width - 2), walls, winds, width, height, (1, 1))
    
    print(go_time, go_back_time, go_again_time)
    print(f"task1: {go_time}")
    print(f"task2: {go_time + go_back_time + go_again_time}")


start_time_main = time.time()
main()
print("--- %s seconds ---" % (time.time() - start_time_main))
