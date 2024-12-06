import sys


def read_matrix() -> tuple[list[list[str]], tuple[int, int], tuple[int, int]]:
    matrix = []
    start = (-1, -1)
    direction = (-1, -1)
    directions = {"^": (-1, 0), "v": (1, 0), "<": (0, -1), ">": (0, 1)}
    for row, line in enumerate(sys.stdin):
        matrix_row = list(line.strip())
        for col, char in enumerate(matrix_row):
            if char in directions:
                start = (row, col)
                direction = directions[char]
        matrix.append(matrix_row)

    return matrix, start, direction


def print_matrix(matrix: list[list[str]]):
    for row in matrix:
        print("".join(row))


def count_movements(
    matrix: list[list[str]], start: tuple[int, int], start_direction: tuple[int, int]
) -> int:
    row, col = start
    direction = start_direction

    n, m = len(matrix), len(matrix[0])

    cange_direction = {
        (-1, 0): (0, 1),  # Up to Right
        (0, 1): (1, 0),  # Right to Down
        (1, 0): (0, -1),  # Down to Left
        (0, -1): (-1, 0),  # Left to Up
    }
    visited = set()
    while True:
        if row < 0 or row >= n or col < 0 or col >= m:
            break
        visited.add((row, col))

        next_row, next_col = row + direction[0], col + direction[1]
        if (
            0 <= next_row < n
            and 0 <= next_col < m
            and matrix[next_row][next_col] == "#"
        ):
            direction = cange_direction[direction]
            continue

        row, col = next_row, next_col

    return len(visited)


if __name__ == "__main__":
    matrix, start, direction = read_matrix()
    print(count_movements(matrix, start, direction))
