import sys


def read_data() -> list[str]:
    return [line.strip() for line in sys.stdin.read().strip().split("\n")]


def find_start(rows: list[str]) -> tuple[int, int]:
    return next(
        (x, y) for y, row in enumerate(rows) for x, c in enumerate(row) if c in "<>v^"
    )


def create_jump_map(
    rows: list[str], width: int, height: int, directions: list[tuple[int, int]]
) -> dict[tuple[int, int, int], tuple[int, int, int] | None]:
    def get_jump_location(x: int, y: int, dindex: int) -> tuple[int, int, int] | None:
        if rows[y][x] == "#":
            return None

        dx, dy = directions[dindex]
        while 0 <= x < width and 0 <= y < height and rows[y][x] != "#":
            x += dx
            y += dy

        if x < 0 or y < 0 or x >= width or y >= height:
            return (x, y, -1)  # Changed dindex from None to -1 to match expected type

        x -= dx
        y -= dy
        dindex = (dindex + 1) % 4
        return (x, y, dindex)

    return {
        (x, y, di): get_jump_location(x, y, di)
        for x in range(width)
        for y in range(height)
        for di in range(len(directions))
    }


def jump_into_block(
    directions: list[tuple[int, int]], dindex: int, block_patch: tuple[int, int]
) -> tuple[int, int, int]:
    dx, dy = directions[dindex]
    bx, by = block_patch
    return (bx - dx, by - dy, (dindex + 1) % 4)


def jump(
    jump_map: dict[tuple[int, int, int], tuple[int, int, int] | None],
    directions: list[tuple[int, int]],
    x: int,
    y: int,
    dindex: int,
    block_patch: tuple[int, int] | None,
) -> tuple[int, int, int] | None:
    dest = jump_map.get((x, y, dindex))
    if dest is None:
        return None

    if block_patch is not None:
        fx, fy, fdindex = dest
        bx, by = block_patch
        if fx == bx and min(y, fy) <= by <= max(y, fy):
            return jump_into_block(directions, dindex, block_patch)
        elif min(x, fx) <= bx <= max(x, fx) and fy == by:
            return jump_into_block(directions, dindex, block_patch)
    return dest


def get_full_path(
    rows: list[str],
    directions: list[tuple[int, int]],
    direction_map: dict[str, tuple[int, int]],
    sx: int,
    sy: int,
    width: int,
    height: int,
) -> set[tuple[int, int]]:
    x, y = sx, sy

    visited = set()
    dindex = directions.index(direction_map[rows[y][x]])

    while True:
        visited.add((x, y))

        dx, dy = directions[dindex]
        x, y = x + dx, y + dy
        if x < 0 or y < 0 or x >= width or y >= height:
            break
        elif rows[y][x] == "#":
            x -= dx
            y -= dy
            dindex = (dindex + 1) % len(directions)

    return visited


def path_loops_with_patch(
    rows: list[str],
    directions: list[tuple[int, int]],
    direction_map: dict[str, tuple[int, int]],
    jump_map: dict[tuple[int, int, int], tuple[int, int, int] | None],
    sx: int,
    sy: int,
    block_patch: tuple[int, int],
) -> bool:
    x, y = sx, sy
    dindex = directions.index(direction_map[rows[y][x]])

    visited = set()

    while True:
        result = jump(jump_map, directions, x, y, dindex, block_patch)
        if result is None:
            return False

        x, y, dindex = result

        if (x, y, dindex) in visited:
            return True

        visited.add((x, y, dindex))


def main() -> None:
    rows = read_data()

    width, height = len(rows[0]), len(rows)
    sx, sy = find_start(rows)

    directions = [(1, 0), (0, 1), (-1, 0), (0, -1)]
    direction_map = {">": (1, 0), "<": (-1, 0), "^": (0, -1), "v": (0, 1)}

    jump_map = create_jump_map(rows, width, height, directions)

    path = get_full_path(rows, directions, direction_map, sx, sy, width, height)
    print(len(path))

    loop_positions = 0
    for block in path:
        if block != (sx, sy) and path_loops_with_patch(
            rows, directions, direction_map, jump_map, sx, sy, block
        ):
            loop_positions += 1

    print(loop_positions)


if __name__ == "__main__":
    main()
