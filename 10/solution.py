def parse_line(line: str):
    parts = line.split()
    if len(parts) == 1:
        return parts[0], None
    else:
        return parts[0], int(parts[1])


with open("input.txt", "r") as f:
    program = [parse_line(line) for line in f.read().splitlines()]

cycle_lookup = {
    "addx": 2,
    "noop": 1,
}


cycles_to_measure = [20, 60, 100, 140, 180, 220]
i = 0

measurements = {}

x = 1
cycle = 1


for operation, value in program:
    
    required_cycles = cycle_lookup[operation]

    if i < len(cycles_to_measure) and cycle + required_cycles > cycles_to_measure[i]:
        measurements[cycles_to_measure[i]] = x * cycles_to_measure[i]
        i += 1

    if operation == "addx":
        x += value

    cycle += required_cycles

print(f"The measurements are {measurements}")
print(f"The sum of the measured signal strengths is {sum(measurements.values())}")


# Part 2


screen_width = 40
screen_height = 6

screen = ["" for _ in range(screen_height)]


sprite_width = 3

x = 1
cycle = 1

for operation, value in program:

    required_cycles = cycle_lookup[operation]

    for i in range(required_cycles):
        screen_idx = cycle - 1 + i
        screen_row = screen_idx // screen_width
        screen_col = screen_idx % screen_width
        if abs(x - screen_col) <= sprite_width / 2:
            screen[screen_row] += "#"
        else:
            screen[screen_row] += "."

    cycle += required_cycles

    if operation == "addx":
        x += value


print("Screen output:")
print("\n".join(screen))
