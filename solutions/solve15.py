#!/usr/bin/env python3

import common


def get_distance(p1, p2):
    return abs(p1[0] - p2[0]) + abs(p1[1] - p2[1])


def is_beacon_possible(sensor_to_length, x, y):
    for sensor, length in sensor_to_length.items():
        if get_distance(sensor, (x, y)) <= length:
            return False
    return True


input_lines = common.init_day(15)
if input_lines is None:
    exit(1)

sensor_to_beacon = {}
for line in input_lines:
    sensor, beacon = line.split(":")
    sensor = sensor.lstrip("Sensor at")
    sensor = tuple(int(value.lstrip("xy=")) for value in sensor.split(", "))
    beacon = beacon.lstrip("closest beacon is at")
    beacon = tuple(int(value.lstrip("xy=")) for value in beacon.split(", "))
    sensor_to_beacon[sensor] = beacon

sensor_to_closest_beacon_length = {}
for sensor, beacon in sensor_to_beacon.items():
    sensor_to_closest_beacon_length[sensor] = get_distance(sensor, beacon)

row_to_inspect = 2000000  # 10 for example data
start = -1000000
end = 5000000
positions_without_beacon = 0
all_beacons = set(sensor_to_beacon.values())
for x in range(start, end):
    if is_beacon_possible(sensor_to_closest_beacon_length, x, row_to_inspect):
        continue
    positions_without_beacon += 1
    for beacon in all_beacons:
        if beacon[1] == row_to_inspect and beacon[0] == x:
            positions_without_beacon -= 1

print(positions_without_beacon)
result1 = positions_without_beacon

# Part 2:
possible_beacons = set()
for sensor, length in sensor_to_closest_beacon_length.items():
    y = sensor[1]
    for i, x in enumerate(range(sensor[0] - length - 1, sensor[0] + 1)):
        possible_beacons.add((x, y - i))
        possible_beacons.add((x, y + i))
    for i, x in enumerate(range(sensor[0] + length + 1, sensor[0] - 1, -1)):
        possible_beacons.add((x, y - i))
        possible_beacons.add((x, y + i))

print(f"possible beans count: {len(possible_beacons)}")
start = 0
# end = 20  # 20 is for example data
end = 4000000

for possible_beacon in possible_beacons:
    x, y = possible_beacon
    if not start <= x <= end:
        continue
    if not start <= y <= end:
        continue
    if possible_beacon in sensor_to_beacon:
        continue
    if not is_beacon_possible(sensor_to_closest_beacon_length, x, y):
        continue
    print(x, y, x * 4000000 + y)
    result2 = x * 4000000 + y
    break

print(f"task1: {result1}")
print(f"task2: {result2}")
