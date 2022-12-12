#!/usr/bin/env python3

import common


def get_neighbours(point, width, length):
    result = []
    i, j = point
    if i > 0:
        result.append((i - 1, j))
    if i < length - 1:
        result.append((i + 1, j))
    if j > 0:
        result.append((i, j - 1))
    if j < width - 1:
        result.append((i, j + 1))
    return result


def update_distances(heightmap, distances, next_points, width, length):
    while not common.is_empty(next_points):
        point = next_points.pop(0)
        for next_point in get_neighbours(point, width, length):
            if heightmap[point] - heightmap[next_point] >= -1 and \
                    distances[next_point] > distances[point] + 1:
                distances[next_point] = distances[point] + 1
                if next_point not in next_points:
                    next_points.append(next_point)


def main():
    input_lines = common.init_day(12)
    if input_lines is None:
        exit(1)

    start = end = 0
    length = len(input_lines)
    width = len(input_lines[0])
    distances = {}
    for i in range(length):
        for j in range(width):
            distances[(i, j)] = 9999

    heightmap = {}
    for i, line in enumerate(input_lines):
        for j, c in enumerate(line):
            if c == 'S':
                start = (i, j)
                c = 'a'
            elif c == 'E':
                end = (i, j)
                c = 'z'
            heightmap[(i, j)] = ord(c)

    distances[start] = 0
    next_points = [start]
    update_distances(heightmap, distances, next_points, width, length)
    result1 = distances[end]

    for point, height in heightmap.items():
        if height == ord('a'):
            distances[point] = 0
            next_points.append(point)
    update_distances(heightmap, distances, next_points, width, length)
    result2 = distances[end]

    print(f"task1: {result1}")
    print(f"task2: {result2}")


main()
