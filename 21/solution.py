import re

with open("input.txt", "r") as f:
    lines = [line.strip().split(":") for line in f.readlines()]

print(lines)



is_number = lambda string: re.match(r"^-?\d+$", string) is not None


def parse(content):

    if is_number(content.strip()):
        return (lambda: int(content.strip()), None, None)
    elif "+" in content:
        m1, m2 = content.split("+")
        return (lambda m1, m2: m1 + m2, m1.strip(), m2.strip())
    elif "-" in content:
        m1, m2 = content.split("-")
        return (lambda m1, m2: m1 - m2, m1.strip(), m2.strip())
    elif "*" in content:
        m1, m2 = content.split("*")
        return (lambda m1, m2: m1 * m2, m1.strip(), m2.strip())
    elif "/" in content:
        m1, m2 = content.split("/")
        return (lambda m1, m2: m1 / m2, m1.strip(), m2.strip())

def part1():

    entries = {monkey: parse(content) for monkey, content in lines}

    root_entry = entries["root"]
    lookup = {}

    def _recurse(operation, m1, m2):
        if not (m1 or m2):
            return operation()
        else:
            return operation(_recurse(*entries[m1]), _recurse(*entries[m2])) 

    result = _recurse(*root_entry)

    print(f"The monkey named root yells: {result}")


def part2():

    entries = {monkey: parse(content) for monkey, content in lines}

    # Fix the operation of the human
    entries["humn"] = (lambda: 0, None, None)

    # Fix the operation of the root monkey
    _, m1, m2 = entries["root"]

    left_entry = entries[m1]
    right_entry = entries[m2]


    def _recurse(operation, m1, m2):
        if not (m1 or m2):
            return operation()
        else:
            return operation(_recurse(*entries[m1]), _recurse(*entries[m2])) 

    def _depends_on_human(_, m1, m2):
        if m1 == "humn" or m2 == "humn":
            return True
        elif m1 is None and m2 is None:
            return False
        else:
            return _depends_on_human(*entries[m1]) or _depends_on_human(*entries[m2]) 

    if _depends_on_human(*left_entry):
        desired_value = _recurse(*right_entry)
        search_entry = left_entry
    else:
        desired_value = _recurse(*left_entry)
        search_entry = right_entry
    
    print(desired_value)
    

part1()
part2()
