# Part 1

# rock (A/X) defeats scissors
# paper (B/Y) defeats rock
# scissors (C/Z) defeats paper
# same ends in a draw

# Total tournament score is sum of scores each round
# shape (1 for rock, 2 for paper, 3 for scissors) +
# outcome (0 if lost, 3 if draw, 6 if win)

# (opponent_shape, my_shape)
shapes = []

with open("day2_input.txt", "r") as f:
    for line in f:
        shapes.append(line.split())


shape_score = {"X": 1, "Y": 2, "Z": 3}

outcome_score = {
    # Opponent plays rock (A)
    "A": {"X": 3, "Y": 6, "Z": 0},
    # Opponent plays paper (B)
    "B": {"X": 0, "Y": 3, "Z": 6},
    # Opponent plays scissors (C)
    "C": {"X": 6, "Y": 0, "Z": 3},
}

total_score = 0

for (opponent_shape, my_shape) in shapes:

    total_score += shape_score[my_shape] + outcome_score[opponent_shape][my_shape]

print(total_score)


# Part 2

# X means you need to lose
# Y means you need to draw
# Z means you need to win

new_shape_score = {"A": 1, "B": 2, "C": 3}

outcome_to_shape_mapping = {
    # Opponent plays rock (A)
    "A": {"X": "C", "Y": "A", "Z": "B"},
    # Opponent plays paper (B)
    "B": {"X": "A", "Y": "B", "Z": "C"},
    # Opponent plays scissors (C)
    "C": {"X": "B", "Y": "C", "Z": "A"},
}

new_outcome_score = {"X": 0, "Y": 3, "Z": 6}

new_total_score = 0

for (opponent_shape, my_outcome) in shapes:

    my_shape = outcome_to_shape_mapping[opponent_shape][my_outcome]
    new_total_score += new_shape_score[my_shape] + new_outcome_score[my_outcome]

print(new_total_score)
