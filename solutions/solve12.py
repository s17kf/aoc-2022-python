#!/usr/bin/env python3

import common


def get_neighbours(i, j, width, length):
    result = []
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
        i, j = next_points.pop(0)
        for neighbour in get_neighbours(i, j, width, length):
            n_i, n_j = neighbour
            if heightmap[i][j] - heightmap[n_i][n_j] >= -1:
                if distances[n_i][n_j] > distances[i][j] + 1:
                    distances[n_i][n_j] = distances[i][j] + 1
                    if neighbour not in next_points:
                        next_points.append(neighbour)


def main():
    input_lines = common.init_day(12)
    if input_lines is None:
        exit(1)

    start = end = 0
    length = len(input_lines)
    width = len(input_lines[0])
    distances = [[9999 for _ in range(width)] for _ in range(length)]

    heightmap = []
    for line in input_lines:
        heightmap.append([])
        for c in line:
            heightmap[-1].append(ord(c))

    for i, row in enumerate(heightmap):
        for j, point in enumerate(row):
            if point == ord('S'):
                start = (i, j)
                heightmap[i][j] = ord('a')
            elif point == ord('E'):
                end = (i, j)
                heightmap[i][j] = ord('z')

    distances[start[0]][start[1]] = 0
    next_points = [start]

    update_distances(heightmap, distances, next_points, width, length)
    result1 = distances[end[0]][end[1]]

    next_points = [start]
    for i, row in enumerate(heightmap):
        for j, height in enumerate(row):
            if height == ord('a'):
                distances[i][j] = 0
                next_points.append((i, j))

    update_distances(heightmap, distances, next_points, width, length)
    result2 = distances[end[0]][end[1]]

    print(f"task1: {result1}")
    print(f"task2: {result2}")


main()
