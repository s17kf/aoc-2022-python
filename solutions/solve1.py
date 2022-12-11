#!/usr/bin/env python3

import common

input_lines = common.init_day(1)
if input_lines is None:
    exit(1)

reindeer_to_snacks = common.get_list_of_groups_divided_empty_line(input_lines)

reindeer_to_calories = []
for snacks in reindeer_to_snacks:
    reindeer_to_calories.append(sum(int(snack) for snack in snacks.split()))

result1 = max(reindeer_to_calories)
result2 = sum(sorted(reindeer_to_calories, reverse=True)[:3])

print(f"task1: {result1}")
print(f"task2: {result2}")
