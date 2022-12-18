#!/usr/bin/env python3

import copy
import time

import common

WIDTH = 7


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


def can_move_down(rock, tower, height, rock_no):
    if height > 0:
        return True
    for i in range(len(rock)):
        if height + i == 1:
            return True
        for j in range(WIDTH):
            if rock[-i - 1][j] == '#' == tower[height + i - 1][j]:
                return False
    return True


def add_rock(rock, tower, height, rock_no):
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


def main():
    input_lines = common.init_day(17)
    if input_lines is None:
        exit(1)

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

    pattern = input_lines[0]

    tower = [[c for c in "#######"]]

    shapes_to_fall = 2022
    blow = -1
    movements = len(pattern)
    for shape_no in range(shapes_to_fall):
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
            if can_move_down(rock, tower, height, shape_no):
                height -= 1
                continue
            add_rock(rock, tower, height, shape_no)
            break

    # print()
    # for i in range(-1, -(len(tower) + 1), -1):
    #     print(''.join(tower[i]))

    result1 = len(tower) - 1
    result2 = 1

    print(f"task1: {result1}")
    print(f"task2: {result2}")

    # for shape in SHAPES:
    #     print_rock(shape)


start_time = time.time()
main()
print("--- %s seconds ---" % (time.time() - start_time))