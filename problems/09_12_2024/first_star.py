import sys


def read_disk() -> list[str]:
    disk_map = sys.stdin.read().strip()
    blocks = []
    data_id = 0
    is_data = True

    for c in disk_map:
        digit = int(c)
        if is_data:
            blocks.extend([str(data_id)] * digit)
            data_id += 1
        else:
            blocks.extend(["."] * digit)
        is_data = not is_data

    return blocks


def process_disk(disk: list[str]) -> list[str]:
    empty_blocks = []
    data_blocks = []

    for index, c in enumerate(disk):
        if c == ".":
            empty_blocks.append(index)
        else:
            data_blocks.append(index)

    data_sorted = sorted(data_blocks)
    empty_sorted = sorted(empty_blocks)

    pointer = len(data_sorted) - 1

    for empty in empty_sorted:
        while pointer >= 0 and data_sorted[pointer] <= empty:
            pointer -= 1
        if pointer >= 0:
            disk[empty] = disk[data_sorted[pointer]]
            disk[data_sorted[pointer]] = "."
            pointer -= 1

    return disk


def compute_checksum(disk: list[str]) -> int:
    checksum = 0
    for i, block in enumerate(disk):
        if block != ".":
            checksum += i * int(block)
    return checksum


def result():
    disk = read_disk()
    blocks = process_disk(disk)
    return compute_checksum(blocks)


if __name__ == "__main__":
    print(result())
