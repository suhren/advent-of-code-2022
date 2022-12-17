import re
import typing as t

data = []
x_min = 0
x_max = 0
y_min = 0
y_max = 0

pattern = re.compile(r"Sensor at x=(\S+), y=(\S+): closest beacon is at x=(\S+), y=(\S+)")

with open("input.txt", "r") as f:
    for line in f.read().splitlines():
        if match := pattern.search(line):
            sx, sy, bx, by = tuple(map(int, match.groups()))
            coverage_distance = abs(sx - bx) + abs(sy - by)
            x_min = min(x_min, sx - coverage_distance)
            x_max = max(x_max, sx + coverage_distance)
            y_min = min(y_min, sy - coverage_distance)
            y_max = max(y_max, sy + coverage_distance)
            data.append((sx, sy, bx, by, coverage_distance))


def get_interval(y: int, sx: int, sy: int, d: int, x_min: int = None, x_max: int = None):
    
    dy = abs(sy - y)

    if dy > d:
        return None

    diff = d - dy
    x0, x1 = (sx - diff, sx + diff)
    
    if x_min is not None:
        if x1 < x_min:
            return None
        x0 = max(x0, x_min)
        
    if x_max is not None:
        if x0 > x_max:
            return None
        x1 = min(x1, x_max)

    return (x0, x1)


def merge_intervals(intervals: t.List[t.Tuple[int, int]]) -> t.List[t.Tuple[int, int]]:
    
    if not intervals:
        return []
    
    # Sort intervals by their left edge
    intervals = list(sorted(intervals))

    result = [intervals[0]]

    for (i, j) in intervals[1:]:
        
        i_last, j_last = result[-1]

        # If the next interval has a left edge intersecting the last interval
        if i <= j_last:
            # If the next interval has a right edge outside of the last interval
            if j > j_last:
                # Update the last interval by extending it to the right
                result[-1] = (i_last, j)
        # If it is not overlappinf with the last interval, create a new one
        else:
            result.append((i, j))

    return result


def part1(y_row_target: int = 2000000):
    
    beacon_x_locations = set()
    coverage_intervals = []
    
    for sx, sy, bx, by, d in data:
        if coverage_interval := get_interval(y=y_row_target, sx=sx, sy=sy, d=d): 
            coverage_intervals.append(coverage_interval)
        if by == y_row_target:
            beacon_x_locations.add(bx)
    
    coverage_intervals = merge_intervals(coverage_intervals)
    
    no_beacon_positions = 0

    for (x0, x1) in coverage_intervals:
        no_beacon_positions += (x1 - x0) + 1
        for x in beacon_x_locations:
            if x0 <= x <= x1:
                no_beacon_positions -= 1

    print(f"Number of positions at y={y_row_target} with no beacon: {no_beacon_positions}")


def part2():

    found_pos = None
    
    search_x_min = 0
    search_y_min = 0
    search_x_max = 4000000
    search_y_max = 4000000
    
    for y in range(search_y_min, search_y_max + 1):
        
        coverage_intervals = []
        
        for sx, sy, bx, by, d in data:
            if coverage_interval := get_interval(y=y, sx=sx, sy=sy, d=d, x_min=search_x_min, x_max=search_x_max): 
                coverage_intervals.append(coverage_interval)
                
        coverage_intervals = merge_intervals(coverage_intervals)

        if len(coverage_intervals) > 1:
            # If there are more than one merged interval, there is a spot between them
            found_pos = (coverage_intervals[0][1] + 1, y)
            break
        
        elif coverage_intervals[0][0] > search_x_min:
            found_pos = (search_x_min, y)
            break

        elif coverage_intervals[0][1] < search_x_max:
            found_pos = (search_x_max, y)
            break
    
    tuning_frequency = found_pos[0] * search_x_max + found_pos[1]
    print(f"Found position at {found_pos} with tuning frequency {tuning_frequency}")


part1()
part2()
