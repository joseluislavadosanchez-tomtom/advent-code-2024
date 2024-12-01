import sys
from collections import Counter


def read_input() -> tuple[list, list]:
    list1, list2 = [], []
    for line in sys.stdin:
        num1, num2 = map(int, line.split())
        list1.append(num1)
        list2.append(num2)
    return list1, list2


if __name__ == "__main__":
    list1, list2 = read_input()
    count_list2 = Counter(list2)
    result = sum(x * count_list2.get(x, 0) for x in list1)
    print(result)
