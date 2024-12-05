import sys


def read_input() -> list[list[str]]:
    """Read lines from stdin and return a list of character lists."""
    return [list(line.strip()) for line in sys.stdin]


def result() -> int:
    input_matrix = read_input()
    n, m = len(input_matrix), len(input_matrix[0])
    count = 0

    up_right_diagonal_directions = [(-1, 1), (1, -1)]
    up_left_diagonal_directions = [(-1, -1), (1, 1)]

    for i in range(n):
        for j in range(m):
            letter = input_matrix[i][j]

            if letter != "A":
                continue

            up_right_diagonal = []

            for di, dj in up_right_diagonal_directions:
                x, y = i + di, j + dj
                if 0 <= x < n and 0 <= y < m:
                    up_right_diagonal.append(input_matrix[x][y])

            if len(up_right_diagonal) < 2:
                continue

            up_left_diagonal = []

            for di, dj in up_left_diagonal_directions:
                x, y = i + di, j + dj
                if 0 <= x < n and 0 <= y < m:
                    up_left_diagonal.append(input_matrix[x][y])

            if len(up_left_diagonal) < 2:
                continue

            if up_right_diagonal == ["S", "M"] and up_left_diagonal == ["M", "S"]:
                count += 1

            if up_right_diagonal == ["M", "S"] and up_left_diagonal == ["M", "S"]:
                count += 1

            if up_right_diagonal == ["M", "S"] and up_left_diagonal == ["S", "M"]:
                count += 1

            if up_right_diagonal == ["S", "M"] and up_left_diagonal == ["S", "M"]:
                count += 1
    return count


if __name__ == "__main__":
    print(result())
