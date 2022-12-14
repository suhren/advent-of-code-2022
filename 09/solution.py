with open("input.txt", "r") as f:
    moves = [line.split() for line in f.read().splitlines()]


current_head_x = 0
current_head_y = 0

last_head_x = current_head_x
last_head_y = current_head_y

tail_x = 0
tail_y = 0

visited = {}


for direction, steps in moves:

    for _ in range(int(steps)):
        
        last_head_x = current_head_x
        last_head_y = current_head_y

        match direction:
            case "L":
                current_head_x -= 1
            case "R":
                current_head_x += 1
            case "U":
                current_head_y -= 1
            case "D":
                current_head_y += 1

        # Move the tail if it is more than 1 position away from the head
        if abs(current_head_x - tail_x) > 1 or abs(current_head_y - tail_y) > 1:
            tail_x, tail_y = last_head_x, last_head_y
        
        visited[(tail_x, tail_y)] = True


print(f"Number of visited positions in part 1: {len(visited)}")



# Part 2

visited = {}

rope_length = 10

def sign(val):
    if val < 0:
        return -1
    elif val > 0:
        return 1
    return 0
    
def resolve_tail(tail_x, tail_y, head_x, head_y):
    
    
    dx = head_x - tail_x
    dy = head_y - tail_y

    # Don't move the tail if it is 1 position or closer from the head
    if abs(dx) <= 1 and abs(dy) <= 1:
        return (tail_x, tail_y)
    
    # Find the sign of the delta (-1, 0, 1)
    sx = sign(dx)
    sy = sign(dy)
    
    return (tail_x + sx, tail_y + sy)
    


# Tail of the rope on index 0, and head of the rope at index -1
rope_positions = [(0, 0)] * rope_length


for direction, steps in moves:

    for _ in range(int(steps)):
        
        head_x, head_y = rope_positions[-1]
        
        match direction:
            case "L":
                head_x -= 1
            case "R":
                head_x += 1
            case "U":
                head_y -= 1
            case "D":
                head_y += 1

        rope_positions[-1] = head_x, head_y

        for i in reversed(range(0, rope_length - 1)):
            
            head_x, head_y = rope_positions[i + 1]
            tail_x, tail_y = rope_positions[i]
            
            tail_x, tail_y = resolve_tail(tail_x, tail_y, head_x, head_y)
            rope_positions[i] = tail_x, tail_y
        

        visited[rope_positions[0]] = True


print(f"Number of visited positions in part 2: {len(visited)}")
