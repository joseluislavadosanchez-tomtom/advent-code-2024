import sys


def read_input() -> tuple[list[int], list[int]]:
    list1, list2 = [], []
    for line in sys.stdin:
        num1, num2 = map(int, line.split())
        list1.append(num1)
        list2.append(num2)
    return list1, list2


def result(list1: list[int], list2: list[int]) -> int:
    list1.sort()
    list2.sort()
    return sum([abs(x - y) for x, y in zip(list1, list2)])


if __name__ == "__main__":
    list1, list2 = read_input()
    print(result(list1, list2))
