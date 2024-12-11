import sys

DIRECTIONS = [
    (-1, 0),  # Up
    (0, 1),  # Right
    (1, 0),  # Down
    (0, -1),  # Left
]


def read_input() -> list[list[int]]:
    matrix = []
    for line in sys.stdin:
        line = line.strip()
        if not line:
            continue
        matrix.append(list(map(int, line)))
    return matrix


def sum_trailhead_ratings(matrix: list[list[int]]) -> int:
    rows = len(matrix)
    cols = len(matrix[0]) if rows > 0 else 0

    # ways[i][j] will hold the count of distinct trails starting at cell (i,j)
    ways = [[0] * (cols) for _ in range(rows)]

    # Group cells by their height
    height_cells = {}
    for i in range(rows):
        for j in range(cols):
            h = matrix[i][j]
            height_cells.setdefault(h, []).append((i, j))

    # Initialize: height 9 cells each have exactly 1 trail (the trivial trail of just themselves)
    for i, j in height_cells[9]:
        ways[i][j] = 1

    # Process from height 8 down to 0
    for h in range(8, -1, -1):
        for i, j in height_cells[h]:
            # Sum the ways of all neighbors that are h+1
            total_ways = 0
            for dx, dy in DIRECTIONS:
                nx, ny = i + dx, j + dy
                if 0 <= nx < rows and 0 <= ny < cols:
                    if matrix[nx][ny] == h + 1:
                        total_ways += ways[nx][ny]
            ways[i][j] = total_ways

    # Now sum the ways of all trailheads (cells with height 0)
    rating_sum = 0
    for i, j in height_cells[0]:
        rating_sum += ways[i][j]

    return rating_sum


if __name__ == "__main__":
    matrix = read_input()
    print(matrix)
    print(sum_trailhead_ratings(matrix))
