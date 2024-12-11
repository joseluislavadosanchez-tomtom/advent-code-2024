import sys
from collections import deque

DIRECTIONS = [
    (0, 1),  # Up
    (1, 0),  # Right
    (0, -1),  # Down
    (-1, 0),  # Left
]


def read_input() -> list[list[int]]:
    matrix = []
    for line in sys.stdin:
        matrix.append(list(map(int, line.strip())))

    return matrix


def count_trail_heads(matrix: list[list[int]], i: int, j: int) -> int:
    rows = len(matrix)
    cols = len(matrix[0])

    start_height = matrix[i][j]
    visited = set()
    visited.add((i, j))

    queue = deque([(i, j, start_height)])

    found_nines = set()
    while queue:
        x, y, height = queue.popleft()

        if height == 9:
            found_nines.add((x, y))

        for dx, dy in DIRECTIONS:
            new_x = x + dx
            new_y = y + dy

            if (
                0 <= new_x < rows
                and 0 <= new_y < cols
                and (new_x, new_y) not in visited
            ):
                if matrix[new_x][new_y] == height + 1:
                    visited.add((new_x, new_y))
                    queue.append((new_x, new_y, height + 1))

    return len(found_nines)


def result(matrix: list[list[int]]) -> int:
    count = 0
    for i in range(len(matrix)):
        for j in range(len(matrix[i])):
            if matrix[i][j] == 0:
                count += count_trail_heads(matrix, i, j)
    return count


if __name__ == "__main__":
    matrix = read_input()
    print(result(matrix))
