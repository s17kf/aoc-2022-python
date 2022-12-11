#!/bin/bash
"""exec" "pyenv" "exec" "python" "$0" "$@"""
import math

import common
from enum import Enum, auto
from collections import Counter
import numpy
from common import numpy_matrix


class Monkey:
    def __init__(self, items, operator, multiplier, divisor, next_on_true, next_on_false,
                 divide=True):
        self.items = items
        self.operation = lambda x, y: x * y if operator == "*" else x + y
        self.multiply_by_old = multiplier == "old"
        self.multiplier = " " if self.multiply_by_old else int(multiplier)
        self.divisor = int(divisor)
        self.next_on_true = int(next_on_true)
        self.next_on_false = int(next_on_false)
        self.inspected_items = 0
        self.divide = divide

    def do_round(self):
        self.inspected_items += len(self.items)
        for i, item in enumerate(self.items):
            multiplier = item if self.multiply_by_old else self.multiplier
            # self.items[i] *= item if self.multiply_by_old else self.multiplier
            self.items[i] = self.operation(item, multiplier)
        if self.divide:
            self.items = [math.floor(item / 3) for item in self.items]
        result = []
        for item in self.items:
            next_monkey = self.next_on_true if item % self.divisor == 0 else self.next_on_false
            result.append((item, next_monkey))
        self.items = []
        return result

    def add_item(self, item):
        self.items.append(item)
        # self.inspected_items += 1

    def get_inspected_items(self):
        return self.inspected_items

    def __repr__(self):
        return f"{self.items}, m({self.multiplier}), d({self.divisor}), " + \
               f"t({self.next_on_true}) f({self.next_on_false})"


def do_round(monkeys):
    for monkey in monkeys:
        items = monkey.do_round()
        for item in items:
            item, next_monkey = item
            monkeys[next_monkey].add_item(item)

def main():
    input_lines = common.init_day(11)
    if input_lines is None:
        exit(1)

    monkeys_data = common.get_list_of_groups_divided_empty_line(input_lines, ";")
    monkeys = []
    monkeys2 = []
    for i, monkey_data in enumerate(monkeys_data):
        monkey_data = monkey_data.split(";")
        # print(monkey_data)
        items = [int(item.rstrip(",")) for item in monkey_data[1].split()[2:]]
        operator, multiplier = monkey_data[2].split()[-2:]
        divisor = monkey_data[3].split()[-1]
        next_on_true = monkey_data[4].split()[-1]
        next_on_false = monkey_data[5].split()[-1]
        monkeys.append(Monkey(items, operator, multiplier, divisor, next_on_true, next_on_false))
        monkeys2.append(
            Monkey(items, operator, multiplier, divisor, next_on_true, next_on_false, False))

    for monkey in monkeys:
        print(monkey)

    for _ in range(20):
        do_round(monkeys)

    print()
    for monkey in monkeys:
        print(monkey.get_inspected_items(), monkey)

    monkey_values = sorted([monkey.get_inspected_items() for monkey in monkeys], reverse=True)

    result1 = monkey_values[0] * monkey_values[1]

    for i in range(1):
        if i % 100 == 0:
            print(i)
        do_round(monkeys2)

    print()
    for monkey in monkeys2:
        print(monkey.get_inspected_items(), monkey)

    monkey_values2 = sorted([monkey.get_inspected_items() for monkey in monkeys2], reverse=True)
    print(monkey_values2)
    result2 = monkey_values2[0] * monkey_values2[1]

    print(f"task1: {result1}")
    print(f"task2: {result2}")


main()
