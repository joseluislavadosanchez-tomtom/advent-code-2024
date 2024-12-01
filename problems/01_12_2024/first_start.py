import sys


def read_input() -> tuple[list, list]:
    list1, list2 = [], []
    for line in sys.stdin:
        num1, num2 = map(int, line.split())
        list1.append(num1)
        list2.append(num2)
    return list1, list2


if __name__ == "__main__":
    list1, list2 = read_input()
    result = sum((abs(x - y) for x, y in zip(sorted(list1), sorted(list2))))
    print(result)
