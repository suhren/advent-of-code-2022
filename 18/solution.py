parse_line = lambda line: tuple(map(int, line.split(",")))

with open("input.txt", "r") as f:
    data = list(map(parse_line, f.readlines()))


def part1():

    width = 0
    height = 0
    depth = 0

    for (x, y, z) in data:
        width = max(width, x + 1)
        height = max(height, y + 1)
        depth = max(depth, z + 1)

    space = [[[0] * depth for _ in range(height)] for _ in range(width)]

    for (x, y, z) in data:
        space[x][y][z] = 1
    
    def _num_neighbours(x, y, z):
        return (
            int(x > 0 and space[x - 1][y][z]) + 
            int(x < width - 1 and space[x + 1][y][z]) +
            int(y > 0 and space[x][y - 1][z]) +
            int(y < height - 1 and space[x][y + 1][z]) +
            int(z > 0 and space[x][y][z - 1]) +
            int(z < depth - 1 and space[x][y][z + 1])
        )

    area = sum(6 - _num_neighbours(*point) for point in data)
    print(f"Total surface area of scanned lava droplet: {area}")


def part2():
    
    # Create a space with padded zeros around the sides
    new_data = [(x + 1, y + 1, z + 1) for (x, y, z) in data]

    width = 0
    height = 0
    depth = 0
    
    for (x, y, z) in new_data:
        width = max(width, x + 2)
        height = max(height, y + 2)
        depth = max(depth, z + 2)

    space = [[[0] * depth for _ in range(height)] for _ in range(width)]

    for (x, y, z) in new_data:
        space[x][y][z] = 1
    
    area = 0
    visited = set()
    queue = [(0, 0, 0)]

    while queue:

        (x, y, z) = queue.pop(0)

        if (x, y, z) in visited:
            continue
            
        visited.add((x, y, z))
        
        if x > 0 and (x - 1, y, z) not in visited:
            if space[x - 1][y][z] == 1:
                area += 1
            else:
                queue.append((x - 1, y, z))

        if x < width - 1 and (x + 1, y, z) not in visited:
            if space[x + 1][y][z] == 1:
                area += 1
            else:
                queue.append((x + 1, y, z))
        
        if y > 0 and (x, y - 1, z) not in visited:
            if space[x][y - 1][z] == 1:
                area += 1
            else:
                queue.append((x, y - 1, z))

        if y < height - 1 and (x, y + 1, z) not in visited:
            if space[x][y + 1][z] == 1:
                area += 1
            else:
                queue.append((x, y + 1, z))

        if z > 0 and (x, y, z - 1) not in visited:
            if space[x][y][z - 1] == 1:
                area += 1
            else:
                queue.append((x, y, z - 1))

        if z < depth - 1 and (x, y, z + 1) not in visited:
            if space[x][y][z + 1] == 1:
                area += 1
            else:
                queue.append((x, y, z + 1))

    print(f"Outside surface area of scanned lava droplet: {area}")


part1()
part2()
