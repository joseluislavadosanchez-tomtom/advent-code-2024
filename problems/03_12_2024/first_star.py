import re
import sys
from collections.abc import Generator
from typing import Any


def read_input() -> Generator[str, Any, None]:
    # Read each line of input
    for line in sys.stdin:
        yield line.strip()


def process_line(line: str) -> int:
    pattern = r"mul\(([0-9]+),([0-9]+)\)"
    groups = re.findall(pattern, line)
    line_result = 0
    for group in groups:
        line_result += int(group[0]) * int(group[1])
    return line_result


def result() -> int:
    total = 0
    for line in read_input():
        total += process_line(line)
    return total


if __name__ == "__main__":
    print(result())
