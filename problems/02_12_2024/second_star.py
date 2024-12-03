import sys
from collections.abc import Generator
from typing import Any


def read_report() -> Generator[list[int], Any, None]:
    for line in sys.stdin:
        yield list(map(int, line.split()))


def check_safe(report: list[int]) -> bool:
    if len(report) < 1:
        return True
    ascending = report[0] < report[1]
    for i in range(0, len(report) - 1):
        diff = report[i] - report[i + 1]
        if not (1 <= abs(diff) <= 3):
            return False

        if (ascending and diff > 0) or (not ascending and diff < 0):
            return False

    return True


def count_safe() -> int:
    count = 0
    for report in read_report():
        if check_safe(report):
            count += 1
        else:
            for i in range(len(report)):
                modified_report = report[:i] + report[i + 1 :]
                if check_safe(modified_report):
                    count += 1
                    break
    return count


if __name__ == "__main__":
    print(count_safe())
