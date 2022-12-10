#!/bin/bash
"""exec" "pyenv" "exec" "python" "$0" "$@"""

import common

input_lines = common.init_day(5)
if input_lines is None:
    exit(1)

stacks_lines, steps_lines = common.get_list_of_groups_divided_empty_line(input_lines, '\n')

stacks_lines = stacks_lines.split("\n")
steps = steps_lines.split("\n")

stacks_count = int(stacks_lines[-1].split()[-1])

stacks = []
for i in range(stacks_count):
    stacks.append([])
for level in list(reversed(stacks_lines))[1:]:
    for i in range(stacks_count):
        crate = level[i*4+1]
        if crate != ' ':
            stacks[i].append(crate)

stacks2 = []
for stack in stacks:
    stacks2.append(stack.copy())

for step in steps:
    null, count, null, source, null, dest = step.split()
    count, source, dest = (int(count), int(source) - 1, int(dest) - 1)
    for i in range(count):
        crate = stacks[source].pop()
        stacks[dest].append(crate)

    stacks_to_move = stacks2[source][-count:]
    del stacks2[source][-count:]
    stacks2[dest] += stacks_to_move

result1 = ''.join([stack[-1] for stack in stacks])
result2 = ''.join([stack[-1] for stack in stacks2])

print(f"task1: {result1}")
print(f"task2: {result2}")
