#!/usr/bin/env python3

import common


def get_neighbours(pos, width, length):
    i, j = pos
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

start_i, start_j = start
distances[start_i][start_j] = 0
next_points = [start]

# below loop is for part 2 only
for i, row in enumerate(heightmap):
    for j, height in enumerate(row):
        if height == ord('a'):
            distances[i][j] = 0
            next_points.append((i, j))

while not common.is_empty(next_points):
    i, j = next_points.pop(0)
    height = heightmap[i][j]
    for neighbour in get_neighbours((i, j), width, length):
        n_i, n_j = neighbour
        if height - heightmap[n_i][n_j] >= -1:
            if distances[n_i][n_j] > distances[i][j] + 1:
                distances[n_i][n_j] = distances[i][j] + 1
                if neighbour not in next_points:
                    next_points.append(neighbour)

result1 = distances[end[0]][end[1]]
result2 = 1

print(f"task1: {result1}")
print(f"task2: {result2}")
