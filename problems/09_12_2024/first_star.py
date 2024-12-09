import sys


def read_disk() -> list[int]:
    disk_map = sys.stdin.read().strip()
    blocks = []
    data_id = 0
    is_data = True

    for c in disk_map:
        digit = int(c)
        if is_data:
            blocks.extend([data_id] * digit)
            data_id += 1
        else:
            blocks.extend([-1] * digit)
        is_data = not is_data

    return blocks


def process_disk(disk: list[int]) -> list[int]:
    empty_blocks = []
    data_blocks = []

    for index, c in enumerate(disk):
        if c == -1:
            empty_blocks.append(index)
        else:
            data_blocks.append(index)

    pointer = len(data_blocks) - 1

    for empty in empty_blocks:
        while pointer >= 0 and data_blocks[pointer] <= empty:
            pointer -= 1
        if pointer >= 0:
            disk[empty] = disk[data_blocks[pointer]]
            disk[data_blocks[pointer]] = -1
            pointer -= 1

    return disk


def compute_checksum(disk: list[int]) -> int:
    checksum = 0
    for i, block in enumerate(disk):
        if block != -1:
            checksum += i * int(block)
    return checksum


def result():
    disk = read_disk()
    blocks = process_disk(disk)
    return compute_checksum(blocks)


if __name__ == "__main__":
    print(result())
