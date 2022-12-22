#!/usr/bin/env python3
import re
import sys

import common

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


def change_direction(direction, letter):
    diff = 1 if letter == "R" else -1
    return DIRECTIONS[(DIRECTION_VALUES[direction] + diff) % len(DIRECTIONS)]


def get_next_tile(tile, position, direction, tile_size):
    x, y = position
    dx, dy = direction
    new_x, new_y = x + dx, y + dy
    if 0 <= new_x < tile_size and 0 <= new_y < tile_size:
        return tile, (new_x, new_y), direction
    if new_x < 0:
        tile, transition, direction = tile.left
    if new_x == tile_size:
        tile, transition, direction = tile.right
    if new_y < 0:
        tile, transition, direction = tile.up
    if new_y == tile_size:
        tile, transition, direction = tile.down
    return tile, transition(x, y), direction


def move(tile, position, steps, direction, tile_size):
    for _ in range(steps):
        new_tile, new_position, new_direction = get_next_tile(tile, position, direction, tile_size)
        new_x, new_y = new_position
        if new_tile.tile[new_y][new_x] == '#':
            return tile, position, direction
        tile, position, direction = new_tile, new_position, new_direction
    return tile, position, direction


class Tile:
    def __init__(self, tile, num, x_offset, y_offset):
        self.tile = tile
        self.right = None
        self.left = None
        self.up = None
        self.down = None
        self.num = num
        self.x_offset = x_offset
        self.y_offset = y_offset


def generate_tiles(tiles_input_lines, tiles_starts, tile_size):
    tiles = []
    for i, tile_start in enumerate(tiles_starts):
        tile = []
        start_x, start_y = tile_start
        for y in range(start_y, start_y + tile_size):
            tile.append(tiles_input_lines[y][start_x:start_x + tile_size])
        tiles.append(Tile(tile, i, start_x, start_y))
    return tiles


def set_relations_example(tiles, tile_size):
    tiles[0].right = (tiles[5], lambda x, y: (tile_size - 1, tile_size - y - 1), LEFT)
    tiles[0].down = (tiles[3], lambda x, y: (x, 0), DOWN)
    tiles[0].left = (tiles[2], lambda x, y: (y, 0), DOWN)
    tiles[0].up = (tiles[1], lambda x, y: (tile_size - x - 1, 0), DOWN)

    tiles[1].right = (tiles[2], lambda x, y: (0, y), RIGHT)
    tiles[1].down = (tiles[4], lambda x, y: (tile_size - x - 1, tile_size - 1), UP)
    tiles[1].left = (tiles[5], lambda x, y: (tile_size - y - 1, tile_size - 1), UP)
    tiles[1].up = (tiles[0], lambda x, y: (tile_size - x - 1, 0), DOWN)

    tiles[2].right = (tiles[3], lambda x, y: (0, y), RIGHT)
    tiles[2].down = (tiles[4], lambda x, y: (0, tile_size - x - 1), RIGHT)
    tiles[2].left = (tiles[1], lambda x, y: (tile_size - 1, y), LEFT)
    tiles[2].up = (tiles[0], lambda x, y: (0, x), RIGHT)

    tiles[3].right = (tiles[5], lambda x, y: (tile_size - y - 1, 0), DOWN)
    tiles[3].down = (tiles[4], lambda x, y: (x, 0), DOWN)
    tiles[3].left = (tiles[2], lambda x, y: (tile_size - 1, y), LEFT)
    tiles[3].up = (tiles[0], lambda x, y: (x, tile_size - 1), UP)

    tiles[4].right = (tiles[5], lambda x, y: (0, y), RIGHT)
    tiles[4].down = (tiles[1], lambda x, y: (tile_size - x - 1, tile_size - 1), UP)
    tiles[4].left = (tiles[2], lambda x, y: (tile_size - y - 1, tile_size - 1), UP)
    tiles[4].up = (tiles[3], lambda x, y: (x, tile_size - 1), UP)

    tiles[5].right = (tiles[0], lambda x, y: (tile_size - 1, tile_size - y - 1), LEFT)
    tiles[5].down = (tiles[1], lambda x, y: (0, tile_size - x - 1), RIGHT)
    tiles[5].left = (tiles[4], lambda x, y: (tile_size - 1, y), LEFT)
    tiles[5].up = (tiles[3], lambda x, y: (tile_size - 1, tile_size - x - 1), LEFT)


def set_relations_real_input(tiles, tile_size):
    tiles[0].right = (tiles[1], lambda x, y: (0, y), RIGHT)
    tiles[0].down = (tiles[2], lambda x, y: (x, 0), DOWN)
    tiles[0].left = (tiles[3], lambda x, y: (0, tile_size - y - 1), RIGHT)
    tiles[0].up = (tiles[5], lambda x, y: (0, x), RIGHT)

    tiles[1].right = (tiles[4], lambda x, y: (tile_size - 1, tile_size - y - 1), LEFT)
    tiles[1].down = (tiles[2], lambda x, y: (tile_size - 1, x), LEFT)
    tiles[1].left = (tiles[0], lambda x, y: (tile_size - 1, y), LEFT)
    tiles[1].up = (tiles[5], lambda x, y: (x, tile_size - 1), UP)

    tiles[2].right = (tiles[1], lambda x, y: (y, tile_size - 1), UP)
    tiles[2].down = (tiles[4], lambda x, y: (x, 0), DOWN)
    tiles[2].left = (tiles[3], lambda x, y: (y, 0), DOWN)
    tiles[2].up = (tiles[0], lambda x, y: (x, tile_size - 1), UP)

    tiles[3].right = (tiles[4], lambda x, y: (0, y), RIGHT)
    tiles[3].down = (tiles[5], lambda x, y: (x, 0), DOWN)
    tiles[3].left = (tiles[0], lambda x, y: (0, tile_size - y - 1), RIGHT)
    tiles[3].up = (tiles[2], lambda x, y: (0, x), RIGHT)

    tiles[4].right = (tiles[1], lambda x, y: (tile_size - 1, tile_size - y -1), LEFT)
    tiles[4].down = (tiles[5], lambda x, y: (tile_size - 1, x), LEFT)
    tiles[4].left = (tiles[3], lambda x, y: (tile_size - 1, y), LEFT)
    tiles[4].up = (tiles[2], lambda x, y: (x, tile_size - 1), UP)

    tiles[5].right = (tiles[4], lambda x, y: (y, tile_size - 1), UP)
    tiles[5].down = (tiles[1], lambda x, y: (x, 0), DOWN)
    tiles[5].left = (tiles[0], lambda x, y: (y, 0), DOWN)
    tiles[5].up = (tiles[3], lambda x, y: (x, tile_size - 1), UP)


def prepare_tiles(tiles_input_lines, input_file_name):
    is_example = "example" in input_file_name
    tile_size = 4 if is_example else 50
    tiles_starts = [(8, 0), (0, 4), (4, 4), (8, 4), (8, 8), (12, 8)] if is_example else \
        [(50, 0), (100, 0), (50, 50), (0, 100), (50, 100), (0, 150)]
    tiles = generate_tiles(tiles_input_lines, tiles_starts, tile_size)

    set_relations_example(tiles, tile_size) if is_example else set_relations_real_input(tiles, tile_size)

    return tiles, tile_size


def main():
    input_lines = common.init_day(22)
    if input_lines is None:
        exit(1)

    numbers = re.split("[RL]", input_lines[-1])
    letters = [c for c in re.split("[\d]+", input_lines[-1]) if c != ""]

    tiles, tile_size = prepare_tiles(input_lines[0:-2], sys.argv[1])

    direction = RIGHT
    tile = tiles[0]
    position = (0, 0)
    for steps in numbers:
        tile, position, direction = move(tile, position, int(steps), direction, tile_size)

        if len(letters) > 0:
            direction = change_direction(direction, letters.pop(0))

    print(letters)
    x, y = position
    print(tile.num, x, y, direction)
    print(x + tile.x_offset, y + tile.y_offset)
    result1 = 1000 * (y + tile.y_offset + 1) + 4 * (x + tile.x_offset + 1) + DIRECTION_VALUES[direction]

    result2 = 1

    print(f"task1: {result1}")
    print(f"task2: {result2}")


main()
