# Part 1

data = []

with open("day4_input.txt", "r") as f:
    for line in f:
        indices = [int(i) for i in line.strip().replace("-", ",").split(",")]
        data.append(indices)


def is_fully_contained(i0, i1, j0, j1):
    # .., .., i0, .., i1, .., ..
    # .., j0, .., ..,  .., j1 ..
    return (i0 >= j0) and (i1 <= j1) or (j0 >= i0) and (j1 <= i1)


num_fully_contained_pairs = 0

for (i0, i1, j0, j1) in data:
    if is_fully_contained(i0, i1, j0, j1):
        num_fully_contained_pairs += 1

print(num_fully_contained_pairs)


# Part 2

def is_overlapping(i0, i1, j0, j1):
    # It is easiest to check if they are NOT overlapping and invert the result
    return not(i1 < j0 or j1 < i0)


num_overlapping_pairs = 0

for (i0, i1, j0, j1) in data:
    if is_overlapping(i0, i1, j0, j1):
        num_overlapping_pairs += 1