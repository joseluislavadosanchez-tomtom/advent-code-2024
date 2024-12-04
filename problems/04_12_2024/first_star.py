import re
import sys


def read_input() -> list[list[str]]:
    """Read lines from stdin and return a list of character lists."""
    return [list(line.strip()) for line in sys.stdin]


def count_xmas(to_check: list[str], pattern: str) -> int:
    to_check_joined = "".join(to_check)
    return len(re.findall(pattern, to_check_joined))


def result() -> int:
    input = read_input()
    count = 0

    for vertical_line in input:
        count += count_xmas(vertical_line, r"(XMAS)")
        count += count_xmas(vertical_line, r"(SAMX)")

    # Read input by columns
    for i in range(len(input[0])):
        count += count_xmas([input[j][i] for j in range(len(input))], r"(XMAS)")
        count += count_xmas([input[j][i] for j in range(len(input))], r"(SAMX)")
        print("_____")

    diagonals = get_all_diagonals(input)
    for diagonal in diagonals:
        count += count_xmas(diagonal, r"(XMAS)")
        count += count_xmas(diagonal, r"(SAMX)")
    return count


def get_all_diagonals(matrix):
    """Extract all diagonals (main and anti) from a matrix into a single list."""
    n, m = len(matrix), len(matrix[0])
    diagonals = {}

    # Collect main diagonals (row - col) and anti-diagonals (row + col)
    for i in range(n):
        for j in range(m):
            # Main diagonal key (difference of indices)
            d = f"main_{i - j}"
            if d not in diagonals:
                diagonals[d] = []
            diagonals[d].append(matrix[i][j])

            # Anti-diagonal key (sum of indices)
            s = f"anti_{i + j}"
            if s not in diagonals:
                diagonals[s] = []
            diagonals[s].append(matrix[i][j])

    # Return all diagonals as a single list
    return list(diagonals.values())


if __name__ == "__main__":
    print(result())
