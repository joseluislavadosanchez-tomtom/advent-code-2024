import random
import timeit


def result(list1: list[int], list2: list[int]) -> int:
    list1.sort()
    list2.sort()
    return sum(abs(x - y) for x, y in zip(list1, list2))


def generate_random_input(size: int, max_value: int) -> tuple[list, list]:
    list1 = [random.randint(0, max_value) for _ in range(size)]
    list2 = [random.randint(0, max_value) for _ in range(size)]
    return list1, list2


if __name__ == "__main__":
    sizes = [10, 100, 1_000, 10_000, 100_000, 1_000_000]
    max_value = 99999
    for size in sizes:
        list1, list2 = generate_random_input(size, max_value)
        times = timeit.repeat(lambda: result(list1, list2), repeat=10, number=1)
        mean_time = sum(times) / len(times)
        std_time = (sum((x - mean_time) ** 2 for x in times) / len(times)) ** 0.5
        print(
            f"Size: {size}, Mean Time: {mean_time:.6f} seconds, Std Dev: {std_time:.6f} seconds"
        )
