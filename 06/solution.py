with open("input.txt", "r") as f:
    string = f.read().strip()


def find_consecutive_unique_characters(string: str, num_chars) -> int:
    state = list(string[:num_chars])
    for i in range(num_chars, len(string)):
        if len(set(state)) == num_chars:
            return i
        state.pop(0)
        state.append(string[i])


print(find_consecutive_unique_characters(string=string, num_chars=4))
print(find_consecutive_unique_characters(string=string, num_chars=14))
