import re
import copy
import typing as t

init_pattern = re.compile(r"\[(\S)\]")
move_pattern = re.compile(r"move (\d+) from (\d+) to (\d+)")

num_stacks = 9

stack_states = [[] for _ in range(num_stacks)]
move_operations = []

with open("input.txt", "r") as f:

    lines = f.readlines()

    for i, line in enumerate(lines):
        if not (matches := list(init_pattern.finditer(line))):
            break
        for match in matches:
            stack_entry = match.group(1)
            stack_index = match.start() // 4
            stack_states[stack_index].insert(0, stack_entry)

    for line in lines[i:]:
        if (matches := move_pattern.findall(line)):
            move_operations.append((int(matches[0][0]), int(matches[0][1]) - 1, int(matches[0][2]) - 1))


stack_states_1 = copy.deepcopy(stack_states)
stack_states_2 = copy.deepcopy(stack_states)


# Part 1
for (num_items, from_index, to_index) in move_operations:
    stack_states_1[to_index] += stack_states_1[from_index][-num_items:][::-1]
    stack_states_1[from_index] = stack_states_1[from_index][:-num_items]

print(stack_states_1)
print("".join(state[-1] for state in stack_states_1))

# Part 2
for (num_items, from_index, to_index) in move_operations:
    stack_states_2[to_index] += stack_states_2[from_index][-num_items:]
    stack_states_2[from_index] = stack_states_2[from_index][:-num_items]

print(stack_states_2)
print("".join(state[-1] for state in stack_states_2))
