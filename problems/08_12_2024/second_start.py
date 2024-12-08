import sys
from math import gcd


def read_antennas() -> tuple[dict[str, list[tuple[int, int]]], int, int]:
    # Read all lines from stdin and strip newline characters
    lines = [line.rstrip("\n") for line in sys.stdin]

    num_rows = len(lines)
    num_cols = max(len(line) for line in lines)

    # Collect antennas grouped by frequency
    antennas = {}
    for y, line in enumerate(lines):
        for x, char in enumerate(line):
            if char != ".":
                if char not in antennas:
                    antennas[char] = []
                antennas[char].append((x, y))

    return antennas, num_cols, num_rows


def normalize_line(x1: int, y1: int, x2: int, y2: int) -> tuple[int, int, int]:
    a = y2 - y1
    b = x1 - x2
    c = x2 * y1 - x1 * y2

    g = gcd(gcd(abs(a), abs(b)), abs(c)) if a or b else 1

    if g != 0:
        a //= g
        b //= g
        c //= g

    if a < 0 or (a == 0 and b < 0):
        a, b, c = -a, -b, -c

    return a, b, c


def enumerate_line_positions(
    a: int, b: int, c: int, num_cols: int, num_rows: int
) -> set[tuple[int, int]]:
    positions = set()

    if a == 0 and b == 0:
        return positions

    if a == 0:
        if b != 0 and (-c) % b == 0:
            y = (-c) // b
            if 0 <= y < num_rows:
                for x in range(num_cols):
                    positions.add((x, y))
    elif b == 0:
        if a != 0 and (-c) % a == 0:
            x = (-c) // a
            if 0 <= x < num_cols:
                for y in range(num_rows):
                    positions.add((x, y))
    else:
        for x in range(num_cols):
            if (a * x + c) % b == 0:
                y = (-a * x - c) // b
                if 0 <= y < num_rows:
                    positions.add((x, y))

        for y in range(num_rows):
            if (b * y + c) % a == 0:
                x = (-b * y - c) // a
                if 0 <= x < num_cols:
                    positions.add((x, y))

    return positions


def result() -> int:
    antennas, num_cols, num_rows = read_antennas()

    anti_nodes = set()

    for _, positions in antennas.items():
        n = len(positions)
        processed_lines = set()

        for i in range(n):
            x1, y1 = positions[i]
            for j in range(i + 1, n):
                x2, y2 = positions[j]

                line = normalize_line(x1, y1, x2, y2)

                if line in processed_lines:
                    continue

                processed_lines.add(line)

                positions_on_line = enumerate_line_positions(*line, num_cols, num_rows)

                anti_nodes.update(positions_on_line)

    return len(anti_nodes)


if __name__ == "__main__":
    print(result())
