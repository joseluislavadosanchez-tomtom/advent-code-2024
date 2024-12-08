import sys
from math import gcd


def read_antennas() -> tuple[dict[str, list[tuple[int, int]]], int, int]:
    # Read all lines from stdin, removing trailing newline characters
    lines = [line.rstrip("\n") for line in sys.stdin]

    # Determine the number of rows and the maximum number of columns in the map
    num_rows = len(lines)
    num_cols = max(len(line) for line in lines) if lines else 0  # Handle empty input

    # Initialize a dictionary to hold antennas grouped by their frequency
    antennas = {}
    for y, line in enumerate(lines):
        for x, char in enumerate(line):
            # Ignore empty spaces denoted by '.'
            if char != ".":
                # If the frequency character is not already a key, add it with an empty list
                if char not in antennas:
                    antennas[char] = []
                # Append the (x, y) position to the corresponding frequency list
                antennas[char].append((x, y))

    return antennas, num_cols, num_rows


def normalize_line(x1: int, y1: int, x2: int, y2: int) -> tuple[int, int, int]:
    # Calculate coefficients a, b, and c based on two points
    a = y2 - y1
    b = x1 - x2
    c = x2 * y1 - x1 * y2

    # Compute the GCD of a, b, and c to reduce the coefficients
    if a or b:
        g = gcd(gcd(abs(a), abs(b)), abs(c))
    else:
        g = 1  # Avoid division by zero if both a and b are zero

    # Divide coefficients by GCD to normalize
    if g != 0:
        a //= g
        b //= g
        c //= g

    # Ensure the first non-zero coefficient is positive for consistency
    if a < 0 or (a == 0 and b < 0):
        a, b, c = -a, -b, -c

    return a, b, c


def enumerate_line_positions(
    a: int, b: int, c: int, num_cols: int, num_rows: int
) -> set[tuple[int, int]]:
    # Initialize an empty set to store unique positions on the line
    positions = set()

    # If both a and b are zero, the line is undefined; return empty set
    if a == 0 and b == 0:
        return positions

    # Handle horizontal lines where a == 0
    if a == 0:
        # Check if y-coordinate is an integer
        if (-c) % b == 0:
            y = (-c) // b  # Calculate the y-coordinate
            # Ensure y is within the map boundaries
            if 0 <= y < num_rows:
                # Add all positions along this horizontal line
                for x in range(num_cols):
                    positions.add((x, y))
    # Handle vertical lines where b == 0
    elif b == 0:
        # Check if x-coordinate is an integer
        if (-c) % a == 0:
            x = (-c) // a  # Calculate the x-coordinate
            # Ensure x is within the map boundaries
            if 0 <= x < num_cols:
                # Add all positions along this vertical line
                for y in range(num_rows):
                    positions.add((x, y))
    else:
        # Handle non-horizontal and non-vertical lines
        # Iterate through all possible x-values to solve for y
        for x in range(num_cols):
            # Check if y is an integer for this x
            if (a * x + c) % b == 0:
                y = (-a * x - c) // b  # Calculate the y-coordinate
                # Ensure y is within the map boundaries
                if 0 <= y < num_rows:
                    positions.add((x, y))

        # Iterate through all possible y-values to solve for x
        for y in range(num_rows):
            # Check if x is an integer for this y
            if (b * y + c) % a == 0:
                x = (-b * y - c) // a  # Calculate the x-coordinate
                # Ensure x is within the map boundaries
                if 0 <= x < num_cols:
                    positions.add((x, y))

    return positions


def result() -> int:
    # Read antennas and map dimensions from input
    antennas, num_cols, num_rows = read_antennas()

    # Initialize a set to store all unique antinode positions
    anti_nodes = set()

    # Iterate over each frequency group
    for _, positions in antennas.items():
        n = len(positions)  # Number of antennas for this frequency
        processed_lines = set()  # To track already processed lines

        # Iterate through all unique pairs of antennas within the same frequency
        for i in range(n):
            x1, y1 = positions[i]  # Coordinates of the first antenna
            for j in range(i + 1, n):
                x2, y2 = positions[j]  # Coordinates of the second antenna

                # Normalize the line defined by the two antennas to ensure uniqueness
                line = normalize_line(x1, y1, x2, y2)

                # Skip if this line has already been processed
                if line in processed_lines:
                    continue

                # Mark this line as processed to avoid duplicate processing
                processed_lines.add(line)

                # Enumerate all positions on this line within the map bounds
                positions_on_line = enumerate_line_positions(*line, num_cols, num_rows)

                # Add all enumerated positions to the set of antinodes
                anti_nodes.update(positions_on_line)

    # Return the total number of unique antinode positions
    return len(anti_nodes)


if __name__ == "__main__":
    # Execute the result function and print the number of unique antinode locations
    print(result())
