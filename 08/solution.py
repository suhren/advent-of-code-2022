with open("input.txt", "r") as f:
    # Add an extra 1 since trees use height 0 as the shortest height
    data = [[int(x) + 1 for x in line] for line in f.read().split()]


rows = len(data)
cols = len(data[0])

visibility = [[0] * cols for _ in range(rows)]

# Left visibility
for i in range(rows):
    max_height = -1
    for j in range(cols):
        if data[i][j] > max_height:
            max_height = data[i][j]
            visibility[i][j] = 1

# Right visibility
for i in range(rows):
    max_height = -1
    for j in reversed(range(cols)):
        if data[i][j] > max_height:
            max_height = data[i][j]
            visibility[i][j] = 1

# Top visibility
for j in range(cols):
    max_height = -1
    for i in range(rows):
        if data[i][j] > max_height:
            max_height = data[i][j]
            visibility[i][j] = 1

# Bottom visibility
for j in range(cols):
    max_height = -1
    for i in reversed(range(rows)):
        if data[i][j] > max_height:
            max_height = data[i][j]
            visibility[i][j] = 1


num_visible = sum(map(sum, visibility))
print(f"Number of visible trees: {num_visible}")


## Part 2


def scenic_score(i_start: int, j_start: int):

    height = data[i_start][j_start]
    score = 0

    # Score to the right
    right_score = 0
    for j in range(j_start, cols - 1, 1):
        right_score += 1
        if data[i_start][j + 1] >= height:
            break

    # Score to the left
    left_score = 0
    for j in range(j_start, 0, -1):
        left_score += 1
        if data[i_start][j - 1] >= height:
            break

    # Score to the bottom
    bottom_score = 0
    for i in range(i_start, rows - 1, 1):
        bottom_score += 1
        if data[i + 1][j_start] >= height:
            break

    # Score to the top
    top_score = 0
    for i in range(i_start, 0, -1):
        top_score += 1
        if data[i - 1][j_start] >= height:
            break

    return right_score * left_score * bottom_score * top_score


best_score = 0

for i in range(rows):
    for j in range(cols):
        best_score = max(best_score, scenic_score(i, j))

print(f"Best scenic score: {best_score}")

