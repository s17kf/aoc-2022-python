#!/usr/bin/env python3.10

import math
import time
from copy import copy

import common

ORE, CLAY, OBSIDIAN, GEODE = 0, 1, 2, 3
ROBOTS = [ORE, CLAY, OBSIDIAN, GEODE]


class Blueprint:
    def __init__(self, id, ore_cost, clay_cost, obsidian_cost, geode_cost):
        self.id = id
        self.costs = [ore_cost, clay_cost, obsidian_cost, geode_cost]
        self.max_ore_robots = sum([clay_cost, obsidian_cost[0], geode_cost[0]])
        self.max_clay_robots = obsidian_cost[1]
        self.max_obsidian_robots = geode_cost[1]
        self.can_afford = [
            lambda minerals: minerals[ORE] >= ore_cost,
            lambda minerals: minerals[ORE] >= clay_cost,
            lambda minerals: minerals[ORE] >= obsidian_cost[0] and minerals[CLAY] >= obsidian_cost[
                1],
            lambda minerals: minerals[ORE] >= geode_cost[0] and minerals[OBSIDIAN] >= geode_cost[1]
        ]

    def perform_buy(self, robot, minerals, robots):
        match robot:
            case 0:
                minerals[ORE] -= self.costs[ORE]
                robots[ORE] += 1
            case 1:
                minerals[ORE] -= self.costs[CLAY]
                robots[CLAY] += 1
            case 2:
                minerals[ORE] -= self.costs[OBSIDIAN][0]
                minerals[CLAY] -= self.costs[OBSIDIAN][1]
                robots[OBSIDIAN] += 1
            case 3:
                minerals[ORE] -= self.costs[GEODE][0]
                minerals[OBSIDIAN] -= self.costs[GEODE][1]
                robots[GEODE] += 1
        return minerals, robots

    def __repr__(self):
        return f"id={self.id} costs={self.costs}"


def get_buyable_robots(blueprint, minerals):
    buyable_robots = []
    for robot in ROBOTS:
        if blueprint.can_afford[robot](minerals):
            buyable_robots.append(robot)
    return buyable_robots


def collect_minerals(minerals, all_robots):
    for mineral, robots in enumerate(all_robots):
        minerals[mineral] += robots


class State:
    def __init__(self, minerals, all_robots):
        self.minerals = copy(minerals)
        self.all_robots = copy(all_robots)
        self.hash = minerals[0] + 100 * minerals[1] + 10000 * minerals[2] + 1000000 * minerals[3] + \
                    10000000 * all_robots[0] + 100000000 * all_robots[1] + \
                    1000000000 * all_robots[2] + 10000000000 * all_robots[3]

    def __repr__(self):
        return f"minerals={self.minerals}, robots={self.all_robots}"

    def __eq__(self, other):
        return self.minerals == other.minerals and self.all_robots == other.all_robots

    def __hash__(self):
        return self.hash


def do_simulation(blueprint, states, last_minute=24, minute=0):
    if minute == last_minute:
        max_geodes = 0
        for state in states:
            if state.minerals[GEODE] > max_geodes:
                max_geodes = state.minerals[GEODE]
        return max_geodes
    new_states = set()
    for state in states:
        minerals, all_robots = state.minerals, state.all_robots
        buyable_robots = get_buyable_robots(blueprint, minerals)
        collect_minerals(minerals, all_robots)
        for robot in buyable_robots:
            if robot == ORE and state.all_robots[ORE] == blueprint.max_ore_robots:
                continue
            if robot == CLAY and state.all_robots[CLAY] == blueprint.max_clay_robots:
                continue
            if robot == OBSIDIAN and state.all_robots[OBSIDIAN] == blueprint.max_obsidian_robots:
                continue
            new_state = State(minerals, all_robots)
            blueprint.perform_buy(robot, new_state.minerals, new_state.all_robots)
            new_states.add(new_state)
    states = states.union(new_states)

    max_geodes = 0
    for state in states:
        if state.minerals[GEODE] > max_geodes:
            max_geodes = state.minerals[GEODE]
    if max_geodes > 0:
        best_sets = set()
        for state in states:
            if state.minerals[GEODE] >= max_geodes - 1:
                best_sets.add(state)
        states = best_sets
    return do_simulation(blueprint, states, last_minute, minute + 1)


def do_task(blueprints, minutes):
    quality_levels = []
    for blueprint in blueprints:
        print(blueprint)
        states = {State([0, 0, 0, 0], [1, 0, 0, 0])}
        localtime = time.localtime(time.time())
        print(f"started at {localtime.tm_hour}:{localtime.tm_min}:{localtime.tm_sec}")
        start_time = time.time()
        result = do_simulation(blueprint, states, minutes)
        print(result)
        print("--- %s seconds ---" % (time.time() - start_time))
        quality_levels.append((result, blueprint.id))
    return quality_levels


def main():
    input_lines = common.init_day(19)
    if input_lines is None:
        exit(1)

    blueprints = []
    for line in input_lines:
        id = int(line.split(":")[0].split()[1])
        ore_cost, clay_cost, obsidian_cost, geode_cost = line.split(". ")
        ore_cost = int(ore_cost.split()[6])
        clay_cost = int(clay_cost.split()[4])
        obsidian_cost = (int(obsidian_cost.split()[4]), int(obsidian_cost.split()[7]))
        geode_cost = (int(geode_cost.split()[4]), int(geode_cost.split()[7]))
        blueprints.append(Blueprint(id, ore_cost, clay_cost, obsidian_cost, geode_cost))


    quality_levels = do_task(blueprints, 24)
    quality_levels = [level * id for level, id in quality_levels]
    print(f"task1: {sum(quality_levels)} <-- {quality_levels}")

    quality_levels = do_task(blueprints[:3], 32)
    quality_levels = [level for level, _ in quality_levels]
    print(f"task2: {math.prod(quality_levels)}")


main_start_time = time.time()
main()
print("--- %s seconds ---" % (time.time() - main_start_time))
