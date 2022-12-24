import re
import typing as t
import dataclasses


@dataclasses.dataclass(frozen=True)
class State:
    ore: int = 0
    clay: int = 0
    obsidian: int = 0
    geode: int = 0
    ore_robots: int = 0
    clay_robots: int = 0
    obsidian_robots: int = 0
    geode_robots: int = 0

    def gather(self) -> "State":
        new_ores = dict(
            ore=self.ore + self.ore_robots,
            clay=self.clay + self.clay_robots,
            obsidian=self.obsidian + self.obsidian_robots,
            geode=self.geode + self.geode_robots,
        )
        new_dict = {**dataclasses.asdict(self), **new_ores}

        return State(**new_dict)

    def add(self, **kwargs) -> "State":
        fields = dataclasses.asdict(self)
        for key, val in kwargs.items():
            fields[key] += val
        return State(**fields)


@dataclasses.dataclass(frozen=True)
class Blueprint:
    # ore -> clay -> obsidian -> geode
    # Ore robots require ore
    ore_robot_cost: int
    # Clay robots require ore
    clay_robot_cost: int
    # Obsidian robots require ore and clay
    obsidian_robot_cost: tuple[int, int]
    # Geode robots require ore and obsidian
    geode_robot_cost: tuple[int, int]


@dataclasses.dataclass(frozen=True)
class Action:
    name: str
    predicate: t.Callable[[State], bool]
    next: t.Callable[[State], State]


def create_actions(blueprint: Blueprint) -> list[Action]:
    
    max_ore_per_robot_required = max(
        blueprint.ore_robot_cost,
        blueprint.clay_robot_cost,
        blueprint.obsidian_robot_cost[0],
        blueprint.geode_robot_cost[0],
    )

    max_clay_per_robot_required = blueprint.obsidian_robot_cost[1]
    max_obsidian_per_robot_required = blueprint.geode_robot_cost[1]

    can_build_ore_robot = lambda state: state.ore >= blueprint.ore_robot_cost
    can_build_clay_robot = lambda state: state.ore >= blueprint.clay_robot_cost
    can_build_obsidian_robot = lambda state: (
        state.ore >= blueprint.obsidian_robot_cost[0] and
        state.clay >= blueprint.obsidian_robot_cost[1]
    )
    can_build_geode_robot = lambda state: (
        state.ore >= blueprint.geode_robot_cost[0] and
        state.obsidian >= blueprint.geode_robot_cost[1]
    )

    should_build_ore_robot = lambda state: can_build_ore_robot(state) and state.ore_robots < max_ore_per_robot_required
    should_build_clay_robot = lambda state: can_build_clay_robot(state) and state.clay_robots < max_clay_per_robot_required
    should_build_obsidian_robot = lambda state: can_build_obsidian_robot(state) and state.obsidian_robots < max_obsidian_per_robot_required
    
    should_wait = lambda state: (
        not can_build_ore_robot(state) and
        not can_build_clay_robot(state) and
        not can_build_obsidian_robot(state) and
        not can_build_geode_robot(state)
    )

    return [
        Action(
            name="wait",
            predicate=lambda _: True,
            next=lambda state: state.gather(),
        ),
        Action(
            name="build_ore_robot",
            predicate=should_build_ore_robot,
            next=lambda state: state.gather().add(
                ore_robots=1,
                ore=-blueprint.ore_robot_cost,
            ),
        ),
        Action(
            name="build_clay_robot",
            predicate=should_build_clay_robot,
            next=lambda state: state.gather().add(
                clay_robots=1,
                ore=-blueprint.clay_robot_cost,
            ),
        ),
        Action(
            name="build_obsidian_robot",
            predicate=should_build_obsidian_robot,
            next=lambda state: state.gather().add(
                obsidian_robots=1,
                ore=-blueprint.obsidian_robot_cost[0],
                clay=-blueprint.obsidian_robot_cost[1],
            ),
        ),
        Action(
            name="build_geode_robot",
            predicate=can_build_geode_robot,
            next=lambda state: state.gather().add(
                geode_robots=1,
                ore=-blueprint.geode_robot_cost[0],
                obsidian=-blueprint.geode_robot_cost[1],
            ),
        ),
    ]




def get_available_actions(state: State, actions: list[Action]):
    # From a given state, what options exist?
    return [action for action in actions if action.predicate(state)]


pattern = re.compile(r"-?\d+")
blueprints = []

with open("input.txt", "r") as f:
    for line in f.readlines():
        numbers = list(map(int, pattern.findall(line)))
        blueprints.append(
            Blueprint(
                ore_robot_cost=numbers[1],
                clay_robot_cost=numbers[2],
                obsidian_robot_cost=tuple(numbers[3:5]),
                geode_robot_cost=tuple(numbers[5:7]),
            )
        )


def part1():

    # The maximum time to run the simulation (depth of tree)
    max_depth = 24
    initial_state = State(ore_robots=1, ore=5)

    blueprint = blueprints[0]
    actions = create_actions(blueprint=blueprint)

    # Perform BFS from initial state until maximum depth reached
    # Tuples of (state, depth)
    queue = [(initial_state, 0)]
    visited = set()

    best_state = initial_state
    last_depth = 0


    while queue:

        state, depth = queue.pop(0)

        if depth != last_depth:
            last_depth = depth
            print(depth)

        if depth > max_depth or state in visited:
            continue

        if state.geode > best_state.geode:
            best_state = state

        visited.add(state)

        available_actions = get_available_actions(state=state, actions=actions)
        next_states = [action.next(state=state) for action in available_actions]

        best_next_state_geode_robots = next_states[0].geode_robots
        best_next_state = None

        for next_state in next_states:
            if next_state.geode_robots > best_next_state_geode_robots:
                best_next_state_geode_robots = next_state.geode_robots
                best_next_state = next_state

        if best_next_state:
            queue.append((best_next_state, depth + 1))
            continue
        
        for next_state in next_states:
            if not next_state in visited:
                queue.append((next_state, depth + 1))

    print(best_state)

part1()

"""
state = State(ore_robots=1)

print(state)

state = state.add(ore=1, clay=1, obsidian=1, geode=1, ore_robots=1, clay_robots=1, obsidian_robots=1, geode_robots=1)

print(state)

state = state.gather()

print(state)
"""
