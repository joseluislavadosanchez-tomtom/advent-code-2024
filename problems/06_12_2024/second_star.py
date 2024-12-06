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


def is_there_loop(
    matrix: list[list[str]], start: tuple[int, int], start_direction: tuple[int, int]
) -> bool:
    row, col = start
    direction = start_direction

    n, m = len(matrix), len(matrix[0])

    change_direction = {
        (-1, 0): (0, 1),  # Up to Right
        (0, 1): (1, 0),  # Right to Down
        (1, 0): (0, -1),  # Down to Left
        (0, -1): (-1, 0),  # Left to Up
    }
    visited = set()

    while True:
        if row < 0 or row >= n or col < 0 or col >= m:
            break

        state = (row, col, direction)
        if state in visited:
            return True
        visited.add(state)

        next_row, next_col = row + direction[0], col + direction[1]
        if (
            0 <= next_row < n
            and 0 <= next_col < m
            and matrix[next_row][next_col] == "#"
        ):
            direction = change_direction[direction]
            continue
        row, col = next_row, next_col

    return False


def get_patrol_path(
    matrix: list[list[str]], start: tuple[int, int], start_direction: tuple[int, int]
) -> set[tuple[int, int]]:
    row, col = start
    direction = start_direction

    n, m = len(matrix), len(matrix[0])
    visited_positions = set()

    change_direction = {
        (-1, 0): (0, 1),
        (0, 1): (1, 0),
        (1, 0): (0, -1),
        (0, -1): (-1, 0),
    }

    while True:
        if row < 0 or row >= n or col < 0 or col >= m:
            break

        visited_positions.add((row, col))

        next_row, next_col = row + direction[0], col + direction[1]
        if (
            0 <= next_row < n
            and 0 <= next_col < m
            and matrix[next_row][next_col] == "#"
        ):
            direction = change_direction[direction]
        else:
            row, col = next_row, next_col

    return visited_positions


def count_loops(
    matrix: list[list[str]], start: tuple[int, int], start_direction: tuple[int, int]
) -> int:
    count = 0

    patrol_path = get_patrol_path(matrix, start, start_direction)

    for row, col in patrol_path:
        if (row, col) == start or matrix[row][col] == "#":
            continue

        original = matrix[row][col]
        matrix[row][col] = "#"
        if is_there_loop(matrix, start, start_direction):
            count += 1
        matrix[row][col] = original

    return count


def result() -> int:
    matrix, start, direction = read_matrix()
    return count_loops(matrix, start, direction)


if __name__ == "__main__":
    print(result())
