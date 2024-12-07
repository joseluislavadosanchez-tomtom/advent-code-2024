import sys
from itertools import product


def read_line():
    # Return a line from the input using a generator
    for line in sys.stdin:
        # parse line first a int then : and then a list of ints
        result, values = line.split(":")
        values = list(map(int, values.split()))
        yield int(result), values


def generate_all_combinations(length: int):
    # Use a generator instead of creating a full list
    return product([0, 1, 2], repeat=length)


def result() -> int:
    final_sum = 0

    for target, values in read_line():
        combinations = generate_all_combinations(len(values) - 1)

        for combination in combinations:
            current_sum = values[0]
            valid = True  # Flag to track if the calculation is valid

            for i, op in enumerate(combination):
                if op == 0:  # Addition
                    current_sum += values[i + 1]
                elif op == 1:  # Multiplication
                    current_sum *= values[i + 1]
                elif op == 2:  # Concatenation
                    current_sum = (
                        current_sum * (10 ** len(str(values[i + 1]))) + values[i + 1]
                    )

                # Early exit if current_sum exceeds target
                if current_sum > target:
                    valid = False
                    break

            if valid and current_sum == target:
                final_sum += target
                break  # No need to check further combinations

    return final_sum


if __name__ == "__main__":
    print(result())
