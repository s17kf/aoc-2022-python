#!/usr/bin/env python3

import copy
import time

import common

WIDTH = 7
SHAPE1 = [[c for c in "..####."]]
SHAPE2 = [[c for c in "...#..."],
          [c for c in "..###.."],
          [c for c in "...#..."]]
SHAPE3 = [[c for c in "....#.."],
          [c for c in "....#.."],
          [c for c in "..###.."]]
SHAPE4 = [[c for c in "..#...."],
          [c for c in "..#...."],
          [c for c in "..#...."],
          [c for c in "..#...."]]
SHAPE5 = [[c for c in "..##..."],
          [c for c in "..##..."]]

SHAPES = [SHAPE1, SHAPE2, SHAPE3, SHAPE4, SHAPE5]


def get_column(matrix, i):
    return [row[i] for row in matrix]


def move_right(rock):
    for i, row in enumerate(rock):
        rock[i] = ['.'] + row[:WIDTH - 1]


def move_left(rock):
    for i, row in enumerate(rock):
        rock[i] = row[1:] + ['.']


def try_push_right(rock, tower, height):
    if '#' in get_column(rock, WIDTH - 1):
        return
    if height >= 0:
        move_right(rock)
        return
    for rock_row, tower_row in enumerate(range(height, min(0, height + len(rock)))):
        for j in range(WIDTH - 1):
            if rock[-rock_row - 1][j] == '#' == tower[tower_row][j + 1]:
                return
    move_right(rock)


def try_push_left(rock, tower, height):
    if '#' in get_column(rock, 0):
        return
    if height >= 0:
        move_left(rock)
        return
    for rock_row, tower_row in enumerate(range(height, min(0, height + len(rock)))):
        for j in range(1, WIDTH):
            if rock[-rock_row - 1][j] == '#' == tower[tower_row][j - 1]:
                return
    move_left(rock)


def can_move_down(rock, tower, height):
    if height > 0:
        return True
    for i in range(len(rock)):
        if height + i == 1:
            return True
        for j in range(WIDTH):
            if rock[-i - 1][j] == '#' == tower[height + i - 1][j]:
                return False
    return True


def add_rock(rock, tower, height):
    if -height >= len(rock):
        for i in range(len(rock)):
            for j, c in enumerate(rock[-i - 1]):
                if c == '#':
                    tower[height + i][j] = c
        return
    for i in range(-height):
        for j, c in enumerate(rock[-i - 1]):
            if c == '#':
                tower[height + i][j] = c
    for i in range(-height + 1, len(rock) + 1):
        tower.append(rock[-i])


def print_rock(rock):
    for row in rock:
        print(row)
    print()


def simulate_falling_shape(tower, shape_no, pattern, movements, blow):
    rock = copy.deepcopy(SHAPES[shape_no % len(SHAPES)])
    height = 3
    while True:
        blow = (blow + 1) % movements
        if pattern[blow] == '>':
            try_push_right(rock, tower, height)
        elif pattern[blow] == '<':
            try_push_left(rock, tower, height)
        else:
            print(pattern[blow])
            exit(10)
        if can_move_down(rock, tower, height):
            height -= 1
            continue
        break
    return rock, height, blow


def simulate(tower, pattern, shapes_to_fall, look_for_cycle=False, start_shape=0, blow=-1):
    movements = len(pattern)
    full_lines = {}
    for shape_no in range(start_shape, shapes_to_fall):
        old_tower_length = len(tower)
        rock, height, blow = simulate_falling_shape(tower, shape_no, pattern, movements, blow)
        add_rock(rock, tower, height)
        if look_for_cycle:
            tower_length_difference = len(tower) - old_tower_length
            for i in range(len(rock)):
                tower_line_minus_index = height - tower_length_difference + i
                tower_line = tower[tower_line_minus_index]
                if tower_line == tower[0]:
                    tower_line_no = len(tower) + tower_line_minus_index
                    for key, value in full_lines.items():
                        if value == (shape_no % 5, blow):
                            cycle_start_height, cycle_start_shape = key
                            cycle_height = tower_line_no - cycle_start_height
                            cycle_shapes = shape_no - cycle_start_shape
                            next_shape_no = shape_no + 1
                            tower_rest = tower[tower_line_no:]
                            return cycle_start_height, cycle_start_shape, \
                                cycle_height, cycle_shapes, next_shape_no, \
                                blow, tower_rest
                    full_lines[(tower_line_no, shape_no)] = (shape_no % 5, blow)
    return len(tower)


def main():
    input_lines = common.init_day(17)
    if input_lines is None:
        exit(1)

    pattern = input_lines[0]
    tower = [[c for c in "#######"]]
    print(f"task1: {simulate(tower, pattern, 2022) - 1}")

    tower = [[c for c in "#######"]]
    shapes_to_fall = 1000000000000
    cycle_start_height, cycle_start_shape, cycle_height, cycle_shapes, next_shape_no, blow, \
        tower_rest = simulate(tower, pattern, shapes_to_fall, True)
    shapes_left = shapes_to_fall - cycle_start_shape
    cycles_fit = shapes_left // cycle_shapes
    next_shape_no += (cycles_fit - 1) * cycle_shapes
    additional_height = simulate(tower_rest, pattern, shapes_to_fall, False, next_shape_no, blow)

    result2 = cycle_start_height + cycles_fit * cycle_height + additional_height - 1
    print(f"task2: {result2}")


start_time = time.time()
main()
print("--- %s seconds ---" % (time.time() - start_time))
