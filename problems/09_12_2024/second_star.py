import sys
from bisect import bisect_left


def read_disk_map() -> list[int]:
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


def identify_files(blocks: list[int]) -> list[tuple[int, int, int]]:
    files = []
    n = len(blocks)
    i = 0
    while i < n:
        if blocks[i] != -1:
            current_id = blocks[i]
            start = i
            length = 1
            i += 1
            while i < n and blocks[i] == current_id:
                length += 1
                i += 1
            files.append((current_id, start, length))
        else:
            i += 1
    return files


def identify_free_spans(blocks: list[int]) -> list[tuple[int, int]]:
    free_spans = []
    n = len(blocks)
    i = 0
    while i < n:
        if blocks[i] == -1:
            start = i
            length = 1
            i += 1
            while i < n and blocks[i] == -1:
                length += 1
                i += 1
            free_spans.append((start, length))
        else:
            i += 1
    return free_spans


def add_free_span(free_spans: list[tuple[int, int]], new_span: tuple[int, int]):
    new_start, new_length = new_span
    new_end = new_start + new_length
    index = bisect_left(free_spans, new_span)

    # Check for merging with previous span
    if index > 0:
        prev_start, prev_length = free_spans[index - 1]
        prev_end = prev_start + prev_length
        if prev_end == new_start:
            new_start = prev_start
            new_length += prev_length
            free_spans.pop(index - 1)
            index -= 1

    # Check for merging with next span
    if index < len(free_spans):
        next_start, next_length = free_spans[index]
        if new_end == next_start:
            new_length += next_length
            free_spans.pop(index)

    # Insert the merged new span
    free_spans.insert(index, (new_start, new_length))


def process_disk_compact_files(blocks: list[int]) -> list[int]:
    files = identify_files(blocks)
    free_spans = identify_free_spans(blocks)

    # Sort free_spans by start index
    free_spans.sort()

    # Sort files in decreasing order of file_id
    files_sorted = sorted(files, key=lambda x: -x[0])

    for file_id, start, length in files_sorted:
        # Binary search to find the first free span that ends <= start and can fit the file
        # Since free_spans are sorted by start, iterate from left to right
        for span_index, (span_start, span_length) in enumerate(free_spans):
            span_end = span_start + span_length
            if span_end > start:
                break  # No spans to the left can fit
            if span_length >= length:
                # Move the file to this span
                # Update the blocks
                for i in range(span_start, span_start + length):
                    blocks[i] = file_id
                for i in range(start, start + length):
                    blocks[i] = -1

                # Update the free_spans list
                if span_length == length:
                    # Exact fit, remove the span
                    free_spans.pop(span_index)
                else:
                    # Adjust the span to remove the used part
                    free_spans[span_index] = (span_start + length, span_length - length)

                # Add the old file location as a new free span
                add_free_span(free_spans, (start, length))
                break  # Move to the next file

    return blocks


def compute_checksum(blocks: list[int]) -> int:
    checksum = 0
    for position, block in enumerate(blocks):
        if block != -1:
            checksum += position * block
    return checksum


def main():
    blocks = read_disk_map()
    compacted_blocks = process_disk_compact_files(blocks)
    checksum = compute_checksum(compacted_blocks)
    print(checksum)


if __name__ == "__main__":
    main()
