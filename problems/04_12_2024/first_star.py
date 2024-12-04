import sys


def read_input() -> list[list[str]]:
    """Read lines from stdin and return a list of character lists."""
    return [list(line.strip()) for line in sys.stdin]


def count_substring(s: str, patterns: set[str]) -> int:
    count = 0
    sub_len = len(next(iter(patterns)))
    for i in range(len(s) - sub_len + 1):
        if s[i : i + sub_len] in patterns:
            count += 1
    return count


def count_patterns(to_check: list[str], patterns: set[str]) -> int:
    if len(to_check) < len(next(iter(patterns))):
        return 0
    to_check_joined = "".join(to_check)
    return count_substring(to_check_joined, patterns)


def result() -> int:
    input_matrix = read_input()
    count = 0
    patterns = {"XMAS", "SAMX"}
    n = len(input_matrix)
    m = len(input_matrix[0])

    # Rows
    for row in input_matrix:
        count += count_patterns(row, patterns)

    # Columns
    for i in range(m):
        column = [input_matrix[j][i] for j in range(n)]
        count += count_patterns(column, patterns)

    # Diagonals
    diagonals = get_all_diagonals(input_matrix)
    for diagonal in diagonals:
        count += count_patterns(diagonal, patterns)

    return count


def get_all_diagonals(matrix: list[list[str]]) -> list[list[str]]:
    n, m = len(matrix), len(matrix[0])
    diagonals = []

    # Main diagonals
    for p in range(-n + 1, m):
        diagonals.append([matrix[i][i - p] for i in range(max(0, p), min(n, n + p))])

    # Anti-diagonals
    for p in range(n + m - 1):
        diagonals.append(
            [
                matrix[i][p - i]
                for i in range(max(0, p - m + 1), min(n, p + 1))
                if 0 <= p - i < m
            ]
        )

    return diagonals


if __name__ == "__main__":
    print(result())
