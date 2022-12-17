import re
import math
import functools
import typing as t

class Monkey:

    def __init__(
        self,
        items: list[int],
        operation: t.Callable[[int], int],
        test_denominator: int,
        test_true_monkey: int,
        test_false_monkey: int,
    ):
        self.items = items.copy()
        self.operation = operation
        self.test_denominator = test_denominator
        self.test_true_monkey = test_true_monkey
        self.test_false_monkey = test_false_monkey
        self.num_inspected = 0

    def simulate_round(
        self,
        monkeys: dict[int, "Monkey"],
        worry_level_divider: int = 3,
        modulo_denominator: int = None,
    ):
        while self.items:

            worry_level = self.items.pop(0)
            new_worry_level = self.operation(worry_level)

            if worry_level_divider:
                new_worry_level = math.floor(new_worry_level / worry_level_divider)

            if modulo_denominator:
                new_worry_level %= modulo_denominator
                
            if new_worry_level % self.test_denominator == 0:
                monkeys[self.test_true_monkey].items.append(new_worry_level)
            else:
                monkeys[self.test_false_monkey].items.append(new_worry_level)
            
            self.num_inspected += 1


pattern = re.compile(
    r"Monkey (\d):\s+"
    r"Starting items: (.+)$\s+"
    r"Operation: (.+)$\s+"
    r"Test: divisible by (.+)$\s+"
    r"If true: throw to monkey (.+)$\s+"
    r"If false: throw to monkey (.+)$",
    re.MULTILINE
)


with open("input.txt", "r") as f:
    regex_matches = re.findall(pattern, f.read())


def get_operation(operation: str) -> t.Callable[[int], int]:
    operator, val = operation.split()[-2:]
    if operator == "+":
        return (lambda x: x + int(val)) if val != "old" else (lambda x: x + x)
    elif operator == "*":
        return (lambda x: x * int(val)) if val != "old" else (lambda x: x * x)
    

def get_monkeys():
    monkeys = {}
    for monkey_index, items, operation, test, true_monkey, false_monkey in regex_matches:
        monkeys[int(monkey_index)] = Monkey(
            items=list(map(int, items.split(","))),
            operation=get_operation(operation),
            test_denominator=int(test),
            test_true_monkey=int(true_monkey),
            test_false_monkey=int(false_monkey),
        )   
    return monkeys


def simulate_rounds(monkeys: dict[int, Monkey], num_rounds: int, worry_level_divider: int = None, modulo_denominator: int = None):
    for _ in range(num_rounds):    
        for monkey in monkeys.values():
            monkey.simulate_round(
                monkeys=monkeys,
                worry_level_divider=worry_level_divider,
                modulo_denominator=modulo_denominator,
            )
    inspect_counts = sorted(monkey.num_inspected for monkey in monkeys.values())
    monkey_business = inspect_counts[-1] * inspect_counts[-2]
    print(f"The level of monkey business is {monkey_business}")



def part1():
    monkeys = get_monkeys()
    simulate_rounds(monkeys, num_rounds=20, worry_level_divider=3)


def part2():
    monkeys = get_monkeys()
    test_denominators = [monkey.test_denominator for monkey in monkeys.values()]
    modulo_denominator = functools.reduce(lambda x, y: x * y, test_denominators)
    simulate_rounds(monkeys, num_rounds=10000, worry_level_divider=None, modulo_denominator=modulo_denominator)


part1()
part2()
