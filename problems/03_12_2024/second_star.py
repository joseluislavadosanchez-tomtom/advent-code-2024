import re
import sys
from collections.abc import Generator
from typing import Any


def read_input() -> Generator[str, Any, None]:
    # Read each line of input
    for line in sys.stdin:
        yield line.strip()


def process_line(line: str, enabled: bool) -> tuple[int, bool]:
    # Define patterns for mul, do, and don't
    mul_pattern = r"mul\(([0-9]+),([0-9]+)\)"
    do_pattern = r"do\(\)"
    dont_pattern = r"don't\(\)"

    # Initialize the state to enabled
    line_result = 0

    # Use regex to find all tokens in the line, including mul, do, and don't instructions
    tokens = re.split(f"({do_pattern}|{dont_pattern}|{mul_pattern})", line)

    for token in tokens:
        # Skip empty tokens or non-matching parts
        if not token or token.isspace():
            continue

        # Update the enabled state based on do() or don't()
        if re.fullmatch(do_pattern, token):
            enabled = True
        elif re.fullmatch(dont_pattern, token):
            enabled = False

        # Process mul instructions only if enabled
        elif enabled:
            mul_match = re.fullmatch(mul_pattern, token)
            if mul_match:
                x, y = int(mul_match.group(1)), int(mul_match.group(2))
                line_result += x * y

    return line_result, enabled


def result() -> int:
    total = 0
    enabled = True
    for line in read_input():
        line_total, enabled = process_line(line, enabled)
        total += line_total
    return total


if __name__ == "__main__":
    print(result())
