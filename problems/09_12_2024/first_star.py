import sys


def read_input() -> tuple[int, list[int]]:
    line = sys.stdin.readline().strip()

    input = list(map(int, line))

    disk = [-1] * sum(input)
    disk_index = 0
    data_id = 0

    for index, digit in enumerate(input):
        data = index % 2 == 0
        if data:
            for i in range(digit):
                disk[disk_index] = data_id
                disk_index += 1
            data_id += 1
        else:
            disk_index += digit

    return disk_index, disk


def process_disk(disk_size: int, disk: list[int]) -> list[int]:
    final_disk = disk.copy()

    empty_index = final_disk.index(-1)
    data_index = disk_size - 1
    while empty_index != data_index:
        if final_disk[data_index] == -1:
            data_index -= 1
        final_disk[empty_index] = final_disk[data_index]
        final_disk[data_index] = -1
        empty_index = final_disk.index(-1)

    return final_disk


def compute_checksum(disk: list[int]) -> int:
    checksum = 0
    for index, digit in enumerate(disk):
        if digit == -1:
            break
        checksum += digit * index

    return checksum


def result() -> int:
    length, values = read_input()
    return compute_checksum(process_disk(length, values))


if __name__ == "__main__":
    print(result())
