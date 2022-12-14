#!/usr/bin/env python3.10

import common

input_lines = common.init_day(7)
if input_lines is None:
    exit(1)

class Dir:
    def __init__(self, name, parent="", level=0):
        self.name = name
        self.content = []
        self.parent = parent
        self.level = level

    def get_size(self):
        size = 0
        for element in self.content:
            size += element.get_size()
        return size

    def __repr__(self) -> str:
        return self.to_string()

    def to_string(self):
        indent = ' ' * (2 * self.level)
        if isinstance(self.parent, Dir):
            result = f"{indent}- {self.name} (dir [{self.parent.name}], size={self.get_size()})\n"
        else:
            result = f"{indent}- {self.name} (dir [], size={self.get_size()})\n"
        for child in self.content:
            result += child.to_string()
        return result

    def get_all_directories_not_bigger(self, limit):
        result = []
        for child in self.content:
            if isinstance(child, Dir):
                if child.get_size() <= limit:
                    result.append((child.name, child.get_size()))
                result += child.get_all_directories_not_bigger(limit)
        return result

    def get_all_directiories_sizes(self):
        result = [self.get_size()]
        for child in self.content:
            if isinstance(child, Dir):
                result += child.get_all_directiories_sizes()
        return result


class File:
    def __init__(self, name, size, level):
        self.name = name
        self.size = size
        self.level = level

    def get_size(self):
        return self.size

    def __repr__(self) -> str:
        indent = ''.join([' ' for i in range(2*self.level)])
        return f"{indent}- {self.name} (file, size={self.size})\n"

    def to_string(self):
        indent = ''.join([' ' for i in range(2*self.level)])
        return f"{indent}- {self.name} (file, size={self.size})\n"


root_dir = Dir("/")
current_dir = root_dir
iscommand = lambda c: c[0] == '$'
isdirectory = lambda c: c.split()[0] == "dir"

for line in input_lines:
    if iscommand(line):
        command = line.split()[1]
        match command:
            case "cd":
                dest = line.split()[2]
                if dest == '..':
                    current_dir = current_dir.parent
                else:
                    for child in current_dir.content:
                        if isinstance(child, Dir):
                            if child.name == dest:
                                current_dir = child
                                break
            case "ls":
                continue
    else:
        size, name = line.split()
        if isdirectory(line):
            current_dir.content.append(Dir(name, current_dir, current_dir.level + 1))
        else:
            current_dir.content.append(File(name, int(size), current_dir.level + 1))

result1 = sum([d[1] for d in root_dir.get_all_directories_not_bigger(100000)])

space_needed = 30000000 - (70000000 - root_dir.get_size())
all_directories_sizes = sorted(root_dir.get_all_directiories_sizes())

for size in all_directories_sizes:
    if size >= space_needed:
        result2 = size
        break

print(f"task1: {result1}")
print(f"task2: {result2}")
