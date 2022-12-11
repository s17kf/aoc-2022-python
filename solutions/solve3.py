#!/usr/bin/env python3

import common


def get_priority(letter):
    return ord(letter) - ord('A') + 27 if letter < 'a' else ord(letter) - ord('a') + 1


input_lines = common.init_day(3)
if input_lines is None:
    exit(1)

rucksacks = [(list(rucksack[:int(len(rucksack)/2)]), list(rucksack[int(len(rucksack)/2):]))
             for rucksack in input_lines]
common_snacks = []
for rucksack in rucksacks:
    for snack in rucksack[0]:
        if snack in rucksack[1]:
            common_snacks.append(get_priority(snack))
            break

rucksacks_v2 = []
for i, rucksack in enumerate(input_lines):
    if i % 3 == 0:
        rucksacks_v2.append([])
    rucksacks_v2[-1].append(rucksack)

common_snacks_v2 = []
for group in rucksacks_v2:
    for snack in group[0]:
        if snack in group[1] and snack in group[2]:
            common_snacks_v2.append(get_priority(snack))
            break

result1 = sum(common_snacks)
result2 = sum(common_snacks_v2)

print(f"task1: {result1}")
print(f"task2: {result2}")
