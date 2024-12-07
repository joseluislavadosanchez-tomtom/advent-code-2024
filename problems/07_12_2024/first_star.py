import sys


def read_line():
    # Return a line from the input using a generator
    for line in sys.stdin:
        # parse line first a int then : and then a list of ints
        result, values = line.split(":")
        values = list(map(int, values.split()))
        yield int(result), values


def generate_all_combinations(length: int) -> list[list[str]]:
    # Generate all combinations of 0 and 1 for a given length
    combinations = []
    for i in range(2 ** (length - 1)):
        combination = bin(i)[2:]
        combination = "0" * ((length - 1) - len(combination)) + combination
        combinations.append(list(combination))

    return combinations


def result() -> int:
    final_sum = 0

    for result, values in read_line():
        combinations = generate_all_combinations(len(values))
        for combination in combinations:
            current_sum = values[0]
            for i in range(len(combination)):
                if combination[i] == "1":
                    current_sum += values[i + 1]
                else:
                    current_sum *= values[i + 1]

            if current_sum == result:
                final_sum += result
                break

    return final_sum


if __name__ == "__main__":
    print(result())
