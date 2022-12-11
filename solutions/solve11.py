#!/usr/bin/env python3

import common
from math import prod


class Monkey:
    def __init__(self, items, operation, multiplier, divisor, next_on_true, next_on_false):
        self.items = items.copy()
        self.operation = operation
        self.multiplier = " " if multiplier == "old" else int(multiplier)
        self.divisor = int(divisor)
        self.next_on_true = int(next_on_true)
        self.next_on_false = int(next_on_false)
        self.inspected_items = 0

    def do_round(self, reduce_operation, reduce_operand, all_monkeys):
        self.inspected_items += len(self.items)
        for item in self.items:
            item = reduce_operation(self.operation(item, self.multiplier), reduce_operand)
            next_monkey = self.next_on_true if item % self.divisor == 0 else self.next_on_false
            all_monkeys[next_monkey].add_item(item)
        self.items = []

    def add_item(self, item):
        self.items.append(item)

    def get_inspected_items(self):
        return self.inspected_items


def do_rounds(rounds, monkeys, reduce_operation, reduce_operand):
    for round in range(rounds):
        for monkey in monkeys:
            monkey.do_round(reduce_operation, reduce_operand, monkeys)
    return prod(sorted([monkey.get_inspected_items() for monkey in monkeys], reverse=True)[0:2])


def main():
    input_lines = common.init_day(11)
    if input_lines is None:
        exit(1)

    reduce_value_part2 = 1
    monkeys = []
    monkeys2 = []
    monkeys_data = common.get_list_of_groups_divided_empty_line(input_lines, ";")
    for monkey_data in monkeys_data:
        monkey_data = monkey_data.split(";")
        items = [int(item.rstrip(",")) for item in monkey_data[1].split()[2:]]
        operator, multiplier = monkey_data[2].split()[-2:]
        operation = (lambda x, y: x + y) if operator == '+' else (lambda x, y: x ** 2) \
            if multiplier == "old" else (lambda x, y: x * y)
        divisor = monkey_data[3].split()[-1]
        next_on_true = monkey_data[4].split()[-1]
        next_on_false = monkey_data[5].split()[-1]
        monkeys.append(
            Monkey(items, operation, multiplier, divisor, next_on_true, next_on_false))
        monkeys2.append(
            Monkey(items, operation, multiplier, divisor, next_on_true, next_on_false))
        reduce_value_part2 *= int(divisor)

    result1 = do_rounds(20, monkeys, (lambda item, op: item // op), 3)
    result2 = do_rounds(10000, monkeys2, (lambda item, op: item % op), reduce_value_part2)

    print(f"task1: {result1}")
    print(f"task2: {result2}")


main()
