#!/usr/bin/env python3

import common


input_lines = common.init_day(21)
if input_lines is None:
    exit(1)

operations = {
    '+': lambda a, b: a + b,
    '-': lambda a, b: a - b,
    '*': lambda a, b: a * b,
    '/': lambda a, b: a // b
}

monkeys_waiting = {}
monkeys_done = {}
for line in input_lines:
    splitted = line.split()
    monkey = splitted[0].rstrip(":")
    if len(splitted) == 2:
        monkeys_done[monkey] = int(splitted[1])
        continue
    monkeys_waiting[monkey] = (splitted[1], splitted[3], splitted[2])

while len(monkeys_waiting) > 0:
    already_done = []
    for monkey, data in monkeys_waiting.items():
        a, b, operation = data
        if a in monkeys_done and b in monkeys_done:
            monkeys_done[monkey] = operations[operation](monkeys_done[a], monkeys_done[b])
            already_done.append(monkey)
    for monkey in already_done:
        del monkeys_waiting[monkey]


print(f"task1: {monkeys_done['root']}")
# print(f"task2: {result2}")
