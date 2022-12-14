#!/usr/bin/env python3

import common


def add_vertical_line(table, x, sy, ey):
    for y in range(min(sy, ey), max(sy, ey) + 1):
        table[y][x] = '#'


def add_horizontal_line(table, y, sx, ex):
    for x in range(min(sx, ex), max(sx, ex) + 1):
        table[y][x] = '#'


def add_line(table, start, end):
    sx, sy = start
    ex, ey = end
    add_vertical_line(table, int(sx), int(sy), int(ey)) if sx == ex else \
        add_horizontal_line(table, int(sy), int(sx), int(ex))


def is_move_possible(table, sand_position):
    x, y = sand_position
    return '.' in table[y + 1][x - 1: x + 2]


def move(table, sand_position):
    x, y = sand_position
    return (x, y + 1) if table[y + 1][x] == '.' else (x - 1, y + 1) if table[y + 1][x - 1] == '.' else (x + 1, y + 1)


def simulate_sand_falling(table, sand_source, termination_condition, additional_move_condition):
    sand_units = 0
    sand_position = sand_source
    while termination_condition(sand_position[1]):
        sand_position = sand_source
        while is_move_possible(table, sand_position) and additional_move_condition(sand_position[1]):
            sand_position = move(table, sand_position)
        table[sand_position[1]][sand_position[0]] = 'o'
        sand_units += 1
    return sand_units


def main():
    input_lines = common.init_day(14)
    if input_lines is None:
        exit(1)

    max_y = 0
    sand_source = (500, 0)
    table = [["." for _ in range(1000)] for _ in range(200)]
    for line in input_lines:
        points = line.split(" -> ")
        previous_point = points[0]
        for point in points[1:]:
            x, y = [int(num) for num in point.split(',')]
            add_line(table, previous_point.split(','), point.split(','))
            previous_point = point
            max_y = max(max_y, y)

    max_y = max_y + 2
    for i in range(len(table[max_y])):
        table[max_y][i] = '#'

    result1 = simulate_sand_falling(table, sand_source, lambda p: p < max_y - 1, lambda p: p < max_y - 1) - 1
    result2 = result1 + 1 + simulate_sand_falling(table,
                                                  sand_source,
                                                  lambda _: table[sand_source[1]][sand_source[0]] == '.',
                                                  lambda _: True)
    print(f"task1: {result1}")
    print(f"task2: {result2}")


main()
