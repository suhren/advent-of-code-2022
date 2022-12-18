# Define the given rock shapes
ROCK_SHAPES = [
    # Horizontal bar
    [[1, 1, 1, 1]],
    # Plus sign
    [[0, 1, 0], [1, 1, 1], [0, 1, 0]],
    # Reversed L
    [[0, 0, 1], [0, 0, 1], [1, 1, 1]],
    # Vertical bar
    [[1], [1], [1], [1]],
    # Square
    [[1, 1], [1, 1]],
]

# Utility type for a matrix
Matrix = list[list[int]]


class Rock:
    def __init__(self, x: int, y: int, shape: Matrix):
        self.x = x
        self.y = y
        self.shape = shape
        self.w = len(shape[0])
        self.h = len(shape)

    def move_and_check_collision(self, dx: int, dy: int, state: list[list]):
        state_h = len(state)
        state_w = len(state[0])
        new_x = self.x + dx
        new_y = self.y + dy

        # Check if intersecting with left wall, right wall, or floor
        if new_x < 0 or new_x + self.w > state_w or new_y + self.h > state_h:
            return True

        # Check if intersecting with another rock in the state matrix
        for y in range(self.h):
            for x in range(self.w):
                if state[new_y + y][new_x + x] == 1 and self.shape[y][x] == 1:
                    return True

        self.x = new_x
        self.y = new_y
        return False


# The tall, vertical chamber is exactly seven units wide
CHAMBER_WIDTH = 7

# The initial state must have enough vertical space for the tallest shape to
# spawn three units above the floor
TALLEST_SHAPE = max(len(shape) for shape in ROCK_SHAPES)
INITIAL_CHAMBER_HEIGHT = TALLEST_SHAPE + 3

# Read input data for the gas jets specifying the movements of the rocks
with open("input.txt", "r") as f:
    #chars = set(f.read().strip())
    MOVEMENTS = [-1 if char == "<" else 1 for char in f.read().strip()]


def print_state(state: list[list]):
    mapping = {0: ".", 1: "#"}
    for line in state:
        print("".join(mapping[val] for val in line))
    print()


def settle_rock(rock: Rock, state: list[list]):
    full_line = False
    for y in range(rock.h):
        for x in range(rock.w):
            if rock.shape[y][x] == 1:
                state[rock.y + y][rock.x + x] = 1
        if all(state[y]):
            print("Full line!")
            full_line = True


def simulate(
    num_rocks_to_simulate: int = None,
    state: Matrix = None,
    shape_index: int = 0,
    movement_index: int = 0,
    rock_stack_height: int = None,
    break_on_known_state: bool = False,
    smart: bool = False,
):
    state = state or []
    rock_is_moving = False
    initial_movement_index = shape_index
    rock_stack_height = rock_stack_height or 0
    num_movements = len(MOVEMENTS)
    num_settled_rocks = 0
    simulation_index = 0
    state_hash_lookup = {}
    fast_forwarded = False

    while num_settled_rocks < num_rocks_to_simulate:
        
        if not rock_is_moving:
            
            # Get the rock to spawn
            shape = ROCK_SHAPES[shape_index]

            # Check if the state matrix is tall enough to spawn a rock
            required_state_height = rock_stack_height + 3 + len(shape)
            if len(state) < required_state_height:
                num_rows_to_add = required_state_height - len(state)
                state = [[0] * CHAMBER_WIDTH for _ in range(num_rows_to_add)] + state

            start_x = 2
            start_y = len(state) - (rock_stack_height + 3 + len(shape))

            # Spawn rock two units from left wall and three units above highest rock
            rock = Rock(x=start_x, y=start_y, shape=shape)
            rock_is_moving = True
            initial_movement_index = movement_index
            
            slice_y_from = start_y + rock.h + 3
            #initial_state_hash = str(hash(str()))
            initial_state_hash = str(hash(str((initial_movement_index, shape_index, state[slice_y_from:slice_y_from + 300]))))

            
        # First, push the rock by the jets
        jet_dx = MOVEMENTS[movement_index % len(MOVEMENTS)]
        rock.move_and_check_collision(dx=jet_dx, dy=0, state=state)

        movement_index  = (movement_index + 1) % num_movements

        # Then check if the fall caused the rock to collide with another rock
        if rock.move_and_check_collision(dx=0, dy=1, state=state):
            rock_is_moving = False
            settle_rock(rock, state)
            rock_stack_height = max(rock_stack_height, len(state) - rock.y)
            num_settled_rocks += 1
            shape_index = num_settled_rocks % len(ROCK_SHAPES)

            if smart and initial_state_hash in state_hash_lookup and not fast_forwarded:
                
                print(f"Encountered known state at {simulation_index=}")

                s1_simulation_index, s1_num_settled_rocks, s1_rock_stack_height = state_hash_lookup[initial_state_hash]

                print(f"Previous state at {s1_simulation_index=}")

                index_diff = simulation_index - s1_simulation_index

                print(f"{index_diff=}")

                num_rocks_settled_per_cycle = num_settled_rocks - s1_num_settled_rocks
                rock_stack_height_per_cycle = rock_stack_height - s1_rock_stack_height

                print(f"{num_rocks_settled_per_cycle=}, {rock_stack_height_per_cycle=}")

                num_rocks_between_states = num_settled_rocks - s1_num_settled_rocks
                num_rocks_remaining = num_rocks_to_simulate - num_settled_rocks

                num_cycles = num_rocks_remaining // num_rocks_between_states
                added_height = num_cycles * rock_stack_height_per_cycle
                added_num_rocks = num_cycles * num_rocks_settled_per_cycle

                # "Fast-forward"
                num_settled_rocks += added_num_rocks
                print(f"{num_settled_rocks=}")

                fast_forwarded = True
                
            else:
                state_hash_lookup[initial_state_hash] = (simulation_index, num_settled_rocks, rock_stack_height)

        simulation_index += 1


    if smart:
        rock_stack_height += added_height
        s1_height_added = s1_rock_stack_height
        cycle_height_added = added_height
        remaining_height_added = rock_stack_height - cycle_height_added - s1_height_added
        print(f"{s1_height_added=}, {cycle_height_added=}, {remaining_height_added=}")
    
    return rock_stack_height


def part1():
    num_rocks_to_simulate = 2022
    height = simulate(num_rocks_to_simulate=num_rocks_to_simulate)
    print(f"Height of rocks after {num_rocks_to_simulate} rocks: {height}")


def part2_old():

    num_rocks_to_simulate = 1000000000000

    state, shape_index, movement_index, s1_num_settled_rocks, s1_rock_stack_height, s2_num_settled_rocks, s2_rock_stack_height = simulate(break_on_known_state=True)
    
    num_rocks_settled_per_cycle = s2_num_settled_rocks - s1_num_settled_rocks
    rock_stack_height_per_cycle = s2_rock_stack_height - s1_rock_stack_height

    print(f"{num_rocks_settled_per_cycle=}, {rock_stack_height_per_cycle=}")

    num_rocks_to_simulate_at_cycle_start = num_rocks_to_simulate  - s1_num_settled_rocks
    num_cycles = num_rocks_to_simulate_at_cycle_start // num_rocks_settled_per_cycle
    cyclic_height = num_cycles * rock_stack_height_per_cycle

    num_remaining_rocks = num_rocks_to_simulate_at_cycle_start % rock_stack_height_per_cycle
    
    print(shape_index, movement_index)
    remaining_height = simulate(
        num_rocks_to_simulate=num_remaining_rocks,
        state=state,
        shape_index=shape_index,
        movement_index=movement_index,
        rock_stack_height=s2_rock_stack_height,
    )

    remaining_height_to_add = remaining_height - s2_rock_stack_height

    height = cyclic_height + remaining_height_to_add
    
    print(f"Height of rocks after {num_rocks_to_simulate} rocks: {height}")


def part2():

    num_rocks_to_simulate = 1000000000000

    height = simulate(num_rocks_to_simulate=num_rocks_to_simulate, smart=True)
    
    print(f"Height of rocks after {num_rocks_to_simulate} rocks: {height}")

    
part1()
part2()
