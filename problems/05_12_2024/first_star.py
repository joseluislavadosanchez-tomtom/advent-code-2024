import sys


def read_rules(lines: list[str]) -> dict[int, list[int]]:
    # Parse the rules from the input lines
    rules = {}
    for line in lines:
        if line == "":
            break
        key, after = map(int, line.split("|"))
        rules.setdefault(key, []).append(after)
    return rules


def read_updates(lines: list[str]) -> list[list[int]]:
    # Parse updates from the input lines
    return [list(map(int, line.split(","))) for line in lines if line]


def result() -> int:
    # Read all input at once
    input_lines = sys.stdin.read().strip().splitlines()

    # Separate rules and updates
    empty_line_index = input_lines.index("")
    rules_lines = input_lines[:empty_line_index]
    updates_lines = input_lines[empty_line_index + 1 :]

    # Parse rules and updates
    rules = read_rules(rules_lines)
    updates = read_updates(updates_lines)

    result = 0
    for update in updates:
        update_set = set(update)  # Use a set for fast membership checking
        update_ok = True

        for index_page, page in enumerate(update):
            page_rules = rules.get(page, [])
            if not page_rules:
                continue

            # Check if all "after" rules are satisfied
            for after in page_rules:
                if after in update_set and after in update[:index_page]:
                    update_ok = False
                    break
            if not update_ok:
                break

        if update_ok:
            # Add the mid element of the update to the result
            result += update[len(update) // 2]

    return result


if __name__ == "__main__":
    print(result())
