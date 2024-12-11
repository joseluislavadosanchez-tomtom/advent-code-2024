import sys
from functools import lru_cache

MUL_FACTOR = 2024


@lru_cache(None)
def transform(stone_str, steps):
    """
    Returns the number of stones after 'steps' transformations starting from 'stone_str'.
    """
    if steps == 0:
        return 1

    if stone_str == "0":
        # Rule 1: 0 -> 1
        return transform("1", steps - 1)

    length = len(stone_str)
    if length % 2 == 0:
        # Even-length stone
        half = length // 2
        left = stone_str[:half].lstrip("0") or "0"
        right = stone_str[half:].lstrip("0") or "0"
        return transform(left, steps - 1) + transform(right, steps - 1)
    else:
        # Odd-length stone (non-zero)
        val = int(stone_str) * MUL_FACTOR
        return transform(str(val), steps - 1)


def solve(stones, total_steps):
    """
    stones: list of initial stones as strings
    total_steps: number of blinks
    """
    count = 0
    for s in stones:
        count += transform(s, total_steps)
    return count


def result():
    # Read the stones from stdin (one line, space-separated)
    line = sys.stdin.readline().strip()
    initial_stones = line.split()
    # You can set total_steps to 75 as required by the puzzle
    total_steps = 75

    result = solve(initial_stones, total_steps)

    return result


if __name__ == "__main__":
    print(result())
