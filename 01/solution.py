# Part 1

with open("input.txt", "r") as f:
    chunks = f.read().split("\n\n")

lists = [[int(line) for line in chunk.split()] for chunk in chunks]
sums = [sum(lst) for lst in lists]

# Elf with most calories
print(max(sums))


# Part 2

# Top three elves calories
print(sum(sorted(sums)[-3:]))
