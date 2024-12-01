import sys
from collections import Counter


def read_input() -> tuple[list[int], list[int]]:
    list1, list2 = [], []
    for line in sys.stdin:
        num1, num2 = map(int, line.split())
        list1.append(num1)
        list2.append(num2)
    return list1, list2


def result(list1: list[int], list2: list[int]) -> int:
    count_list2 = Counter(list2)
    return sum(x * count_list2.get(x, 0) for x in list1)


if __name__ == "__main__":
    list1, list2 = read_input()
    count_list2 = Counter(list2)
    print(result(list1, list2))
