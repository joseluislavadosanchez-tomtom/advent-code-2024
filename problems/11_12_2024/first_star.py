import sys


def read_values() -> list[int]:
    return list(map(int, sys.stdin.readline().split()))


def blink(values: list[int]) -> list[int]:
    new_values = []
    for value in values:
        if value == 0:
            # If the stone is engraved with 0, it becomes 1
            new_values.append(1)
        else:
            s = str(value)
            if len(s) % 2 == 0:
                # Even number of digits: split into two stones
                half = len(s) // 2
                left_str, right_str = s[:half], s[half:]
                left_num = int(left_str)  # Convert to int to remove leading zeros
                right_num = int(right_str)
                new_values.append(left_num)
                new_values.append(right_num)
            else:
                # Otherwise, multiply by 2024
                new_values.append(value * 2024)
    return new_values


def result() -> int:
    values = read_values()
    for _ in range(25):
        values = blink(values)

    return len(values)


if __name__ == "__main__":
    print(result())
