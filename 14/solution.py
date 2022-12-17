formations = []

SAND_ENTRY_Y = 0
SAND_ENTRY_X = 500

x_min = 0
y_min = 0
x_max = 0
y_max = 0

with open("input.txt", "r") as f:
    for line in f.read().splitlines():
        formation = []
        for pair in map(str.strip, line.split("->")):
            x, y = pair.split(",")
            x = int(x)
            y = int(y)
            x_max = max(x_max, x)
            y_max = max(y_max, y)
            formation.append((x, y))  
        formations.append(formation)


def print_state(state, x0, y0, x1, y1):
    for row in state[y0:y1]:
        print("".join(map(str, row[x0:x1])))


def create_state(x_min: int, y_min: int, x_max: int, y_max: int, floor: bool = False):
    width = x_max - x_min + 1 
    height = y_max - y_min + 1
    state = [[0] * width for _ in range(height)]

    for formation in formations:
        for (x0, y0), (x1, y1) in zip(formation[:-1], formation[1:]):
            from_x = min(x0, x1)
            from_y = min(y0, y1)
            to_x = max(x0, x1)
            to_y = max(y0, y1)
            for x in range(from_x, to_x + 1):
                for y in range(from_y, to_y + 1):
                    state[y][x] = 1

    # Create floor
    if floor:
        for x in range(width):
            state[-1][x] = 1
        
    return state


def simulate(state):
    
    num_sand_units_at_rest = 0
    sand_is_flowing = True

    y_max = len(state) - 1

    while sand_is_flowing:
        sand_unit_is_at_rest = False
        sand_x, sand_y = SAND_ENTRY_X, SAND_ENTRY_Y

        while not sand_unit_is_at_rest:
            if not state[sand_y + 1][sand_x]:
                sand_y += 1  
            elif not state[sand_y + 1][sand_x - 1]:
                sand_x, sand_y = sand_x - 1, sand_y + 1     
            elif not state[sand_y + 1][sand_x + 1]:
                sand_x, sand_y = sand_x + 1, sand_y + 1
            else:
                sand_unit_is_at_rest = True
                num_sand_units_at_rest += 1
                state[sand_y][sand_x] = 1

                if state[SAND_ENTRY_Y][SAND_ENTRY_X]:
                    # If there is sand at the entry at this stage, it has been blocked
                    sand_is_flowing = False
                    break

            if sand_y >= y_max:
                # Sand fell into the void
                sand_is_flowing = False
                break
    
    print(f"Number of sand units at rest: {num_sand_units_at_rest}")


def part1():
    state = create_state(x_min, y_min, x_max, y_max)
    simulate(state)


def part2():

    new_y_max = y_max + 2
    max_sand_pile_radius = new_y_max - y_min
    sand_pile_x_min = SAND_ENTRY_X - max_sand_pile_radius
    sand_pile_x_max = SAND_ENTRY_X + max_sand_pile_radius

    new_x_min = min(x_min, sand_pile_x_min)
    new_x_max = max(x_max, sand_pile_x_max)
    
    state = create_state(new_x_min, y_min, new_x_max, new_y_max, floor=True)
    simulate(state)


part1()
part2()