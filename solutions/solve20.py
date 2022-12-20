#!/usr/bin/env python3

import common

LAST_NODE = None


class Node:
    def __init__(self, value):
        global LAST_NODE
        self.value = value
        self.next = None
        if LAST_NODE is not None:
            LAST_NODE.next = self
        self.prev = LAST_NODE
        LAST_NODE = self


def move_forward(node: Node, steps: int, all_nodes_size):
    if steps % (all_nodes_size - 1) == 0:
        return

    prev_node = node
    node.prev.next = node.next
    node.next.prev = node.prev

    for i in range(steps % (all_nodes_size - 1)):
        prev_node = prev_node.next

    node.next = prev_node.next
    node.prev = prev_node
    prev_node.next = node
    node.next.prev = node


def move_backward(node: Node, steps: int, all_nodes_size):
    if steps % (all_nodes_size - 1) == 0:
        return

    next_node = node
    node.prev.next = node.next
    node.next.prev = node.prev

    for i in range(steps % (all_nodes_size - 1)):
        next_node = next_node.prev

    node.prev = next_node.prev
    node.next = next_node
    next_node.prev = node
    node.prev.next = node


def decrypt(numbers, decryption_key=1, repetitions=1):
    global LAST_NODE
    LAST_NODE = None
    all_nodes = []
    zero_index = 0
    for i, value in enumerate(numbers):
        node = Node(value * decryption_key)
        all_nodes.append(node)
        if node.value == 0:
            zero_index = i

    all_nodes[0].prev = all_nodes[-1]
    all_nodes[-1].next = all_nodes[0]
    for _ in range(repetitions):
        for i in range(len(all_nodes)):
            node = all_nodes[i]
            if node.value == 0:
                continue
            move_forward(node, node.value, len(all_nodes)) if node.value > 0 else \
                move_backward(node, -node.value, len(all_nodes))

    key_numbers = []
    node = all_nodes[zero_index]
    for i in range(3000):
        node = node.next
        if i in [999, 1999, 2999]:
            key_numbers.append(node.value)
    print(key_numbers)
    return key_numbers


input_lines = common.init_day(20)
if input_lines is None:
    exit(1)

numbers = [int(line) for line in input_lines]

print(f"task1: {sum(decrypt(numbers))}")
print(f"task2: {sum(decrypt(numbers, 811589153, 10))}")
