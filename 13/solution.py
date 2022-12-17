import functools
from ast import literal_eval


with open("input.txt", "r") as f:
    pairs = [pair.splitlines() for pair in f.read().split("\n\n")]
    data = [tuple(map(literal_eval, pair)) for pair in pairs]


def compare(left: list, right: list) -> bool:
    for x, y in zip(left, right):  
        if isinstance(x, int) and isinstance(y, int):
            if x != y:
                return -1 if x < y else 1
        else:
            x = [x] if not isinstance(x, list) else x
            y = [y] if not isinstance(y, list) else y
            if (result := compare(x, y)) != 0:
                return result
    
    if len(left) != len(right):
        return -1 if len(left) < len(right) else 1

    return 0


def part1():
    indices = [i for i, (d1, d2) in enumerate(data, start=1) if compare(d1, d2) == -1]
    print(f"The sum of the indices is: {sum(indices)}")


def part2():
    divider_packets = [[[2]], [[6]]]
    input_data = [packet for pair in data for packet in pair] + divider_packets
    sorted_data = list(sorted(input_data, key=functools.cmp_to_key(compare)))
    divider_packet_indices = [sorted_data.index(packet) + 1 for packet in divider_packets]
    decoder_key = functools.reduce(lambda x, y: x*y, divider_packet_indices)
    print(f"The decoder key is: {decoder_key}")
    

part1()
part2()
