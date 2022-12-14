# Part 1

with open("input.txt", "r") as f:
    rucksack_lines = f.read().split()

def get_priority(char: str):
    if char.islower():
        return ord(char) - ord("a") + 1
    else:
        return ord(char) - ord("A") + 27

all_compartment_matches = []

for rucksack_line in rucksack_lines:
    partition_size = len(rucksack_line) // 2
    compartment_1_items = rucksack_line[:partition_size]
    compartment_2_items = rucksack_line[partition_size:]
    compartment_matches = set(compartment_1_items).intersection(compartment_2_items)
    all_compartment_matches += compartment_matches

priority_sum = sum(get_priority(char) for char in all_compartment_matches)
print(priority_sum)


# Part 2

group_size = 3
num_groups = len(rucksack_lines) // group_size

all_group_matches = []

for i in range(num_groups):
    group_lines = rucksack_lines[i*group_size: (i+1)*group_size]
    common_items = set.intersection(*map(set, group_lines))
    all_group_matches += common_items

new_priority_sum = sum(get_priority(char) for char in all_group_matches)
print(new_priority_sum)
