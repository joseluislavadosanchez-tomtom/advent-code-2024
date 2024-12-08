import sys


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


def result() -> int:
    antennas, num_cols, num_rows = read_antennas()

    # Set to store unique antinode positions
    anti_nodes = set()

    # Process each frequency group
    for _, positions in antennas.items():
        n = len(positions)
        # Iterate over all unique pairs
        for i in range(n):
            x1, y1 = positions[i]
            for j in range(i + 1, n):
                x2, y2 = positions[j]

                # Compute P1: 2*x2 - x1, 2*y2 - y1
                p1_x = 2 * x2 - x1
                p1_y = 2 * y2 - y1

                # Compute P2: 2*x1 - x2, 2*y1 - y2
                p2_x = 2 * x1 - x2
                p2_y = 2 * y1 - y2

                # Check if P1 is within bounds
                if 0 <= p1_x < num_cols and 0 <= p1_y < num_rows:
                    anti_nodes.add((p1_x, p1_y))
                # Check if P2 is within bounds
                if 0 <= p2_x < num_cols and 0 <= p2_y < num_rows:
                    anti_nodes.add((p2_x, p2_y))

    # Output the number of unique antinode locations
    return len(anti_nodes)


if __name__ == "__main__":
    print(result())
