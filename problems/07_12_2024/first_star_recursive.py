import sys


def read_line():
    # Return a line from the input using a generator
    for line in sys.stdin:
        # parse line first a int then : and then a list of ints
        result, values = line.split(":")
        values = list(map(int, values.split()))
        yield int(result), values


def evaluate_equation(
    target: int, numbers: list[int], index: int = 1, current_value: int | None = None
) -> bool:
    if current_value is None:
        current_value = numbers[0]

    if index == len(numbers):
        return current_value == target

    if evaluate_equation(target, numbers, index + 1, current_value + numbers[index]):
        return True

    return evaluate_equation(target, numbers, index + 1, current_value * numbers[index])


def result() -> int:
    final_sum = 0

    for target, values in read_line():
        if evaluate_equation(target, values):
            final_sum += target

    return final_sum


if __name__ == "__main__":
    print(result())
