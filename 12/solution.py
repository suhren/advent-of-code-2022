def get_elevation(char: str) -> int:
    return ord(char) - ord("a")

data = []

with open("input.txt", "r") as f:
    for y, line in enumerate(f.readlines()):
        data_line = []
        for x, char in enumerate(line.strip()):
            if char == "S":
                source_position = (x, y)
                data_line.append(get_elevation("a"))
            elif char == "E":
                target_position = (x, y)
                data_line.append(get_elevation("z"))
            else:
                data_line.append(get_elevation(char))
        data.append(data_line)


def get_neighbours(data, x, y):
    height = len(data)
    width = len(data[0])
    can_walk = lambda e1, e2: e2 <= e1 + 1 
    result = []

    # Walk left
    if x > 0 and can_walk(data[y][x], data[y][x - 1]):
        result.append((x - 1, y))
    # Walk right
    if x < width - 1 and can_walk(data[y][x], data[y][x + 1]):
        result.append((x + 1, y))
    # Walk up
    if y > 0 and can_walk(data[y][x], data[y - 1][x]):
        result.append((x, y - 1))   
    # Walk down
    if y < height - 1 and can_walk(data[y][x], data[y + 1][x]):
        result.append((x, y + 1))

    return result


def get_shortest_path_bfs(data, source_position, target_position):
    explored = set()
    queue = [[source_position]]

    while queue:
        path = queue.pop(0)
        node = path[-1]

        if node in explored:
            continue

        neighbours = get_neighbours(data, *node)
        
        for neighbour in neighbours:
            new_path = path.copy() + [neighbour]
            queue.append(new_path)

            if neighbour == target_position:
                return new_path

            explored.add(node)


def part1():

    shortest_path = get_shortest_path_bfs(data, source_position, target_position)
    print(f"Steps from {source_position} to {target_position}: {len(shortest_path) - 1}")


def part2():

    height = len(data)
    width = len(data[0])

    fewest_steps = float("inf") 

    for y in range(height):
        for x in range(width):
            if data[y][x] == 0:
                shortest_path = get_shortest_path_bfs(data, (x, y), target_position)
                if shortest_path is not None:
                    fewest_steps = min(fewest_steps, len(shortest_path) - 1)
    
    print(f"Number of steps in shortest path: {fewest_steps}")


part1()
part2()