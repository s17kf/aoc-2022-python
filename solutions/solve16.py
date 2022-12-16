#!/usr/bin/env python3

import copy
import time
from typing import Dict

import common


class Valve:
    def __init__(self, name: str, rate: int):
        self.name = name
        self.rate = rate
        self.nexts = []

    def add_next(self, valve):
        self.nexts.append(valve)

    def __repr__(self):
        return f"Valve=({self.name}, {self.rate}, {[valve.name for valve in self.nexts]})"


class DistanceDict(dict):
    def __missing__(self, key):
        return 1000


def get_distances(start_point: Valve):
    distances = DistanceDict()
    distances[start_point.name] = 0
    for next_valve in start_point.nexts:
        distances[next_valve.name] = 1
    next_valves = set(start_point.nexts)
    while len(next_valves) > 0:
        valve = next_valves.pop()
        for next_valve in valve.nexts:
            if distances[next_valve.name] > distances[valve.name] + 1:
                distances[next_valve.name] = distances[valve.name] + 1
                next_valves.add(next_valve)
    return distances


def remove_zero_rate_distances(distances: Dict[str, int], valves: Dict[str, Valve]):
    # distances = get_distances(start_point, valves)
    for valve in valves.values():
        if valve.rate == 0:
            del distances[valve.name]


def copy_all_valves(valves: Dict[str, Valve]):
    copied_valves = {}
    for name, valve in valves.items():
        copied_valves[name] = Valve(valve.name, valve.rate)
    for valve in valves.values():
        for next_valve in valve.nexts:
            copied_valves[valve.name].add_next(copied_valves[next_valve.name])
    return copied_valves


def get_released_pressure(openings):
    released_pressure = 0
    for minute, rate in openings.items():
        if minute < 31:
            released_pressure += (31 - minute) * rate
    return released_pressure


global_best_pressure = 0


def find_highest_pressure(valves: Dict[str, Valve],
                          valve_to_distances: Dict[str, Dict[str, int]],
                          current_valve_name="AA",
                          openings={},
                          current_minute=1):
    current_valve = valves[current_valve_name]
    # distances = get_no_zero_rate_distances(current_valve, valves)
    # distances = [distance for distance in get_distances(current_valve, valves) if ]
    # distances = get_distances(current_valve)
    distances = copy.copy(valve_to_distances[current_valve.name])
    remove_zero_rate_distances(distances, valves)
    if len(distances) == 0 or current_minute > 30:
        return openings

    openings_variants = []
    for valve_name, distance in distances.items():
        new_valves = copy_all_valves(valves)
        valve = new_valves[valve_name]
        new_minute = current_minute + distance + 1
        new_openings = copy.copy(openings)
        new_openings[new_minute] = valve.rate
        valve.rate = 0
        openings_variants.append(find_highest_pressure(new_valves,
                                                       valve_to_distances,
                                                       valve.name,
                                                       new_openings,
                                                       new_minute))

    best_openings = openings
    for other_openings in openings_variants:
        if get_released_pressure(best_openings) < get_released_pressure(other_openings):
            best_openings = other_openings
    pressure = get_released_pressure(best_openings)
    global global_best_pressure
    if pressure > global_best_pressure:
        global_best_pressure = pressure
        print(pressure, best_openings)
    return best_openings


def main():
    input_lines = common.init_day(16)
    if input_lines is None:
        exit(1)

    all_valves = {}
    non_zero_rate_count = 0
    for i, line in enumerate(input_lines):
        valve_text = line.split(';')[0].split()
        name = valve_text[1]
        rate = int(valve_text[4].split('=')[1])
        all_valves[name] = Valve(name, rate)
        non_zero_rate_count += 1 if rate > 0 else 0

    for line in input_lines:
        valve_name = line.split()[1]
        nexts = [name.strip(",") for name in line.split()[9:]]
        for next_name in nexts:
            all_valves[valve_name].add_next(all_valves[next_name])

    valve_to_distances = {}
    for name, valve in all_valves.items():
        valve_to_distances[name] = get_distances(valve)
    openings = find_highest_pressure(all_valves, valve_to_distances)
    released_pressure = get_released_pressure(openings)
    # print(f"{released_pressure}: {openings}")

    result1 = released_pressure
    result2 = 1

    print(f"task1: {result1}")
    print(f"task2: {result2}")


start_time = time.time()
main()
print("--- %s seconds ---" % (time.time() - start_time))
