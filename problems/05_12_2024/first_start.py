import sys


def read_rules() -> dict[int, list[int]]:
    # Read line by line till we found a empty line
    rules = dict()
    for line in sys.stdin:
        if line == "\n":
            break
        key, after = list(map(int, line.strip().split("|")))
        if key not in rules:
            rules[key] = [after]
        else:
            rules[key].append(after)

    return rules


def read_update() -> list[int]:
    line = sys.stdin.readline().strip("")
    if not line:
        return []
    return list(map(int, line.split(",")))


def result() -> int:
    rules = read_rules()

    result = 0
    while True:
        update = read_update()
        if len(update) == 0:
            break

        update_ok = True
        for index_page, page in enumerate(update):
            page_rules = rules.get(page, [])
            if len(page_rules) == 0:
                continue

            all_ok = True
            for after in page_rules:
                # all_ok if all after are after page in update
                if after not in update:
                    continue
                if after in update[:index_page]:
                    all_ok = False
                    break
            if not all_ok:
                update_ok = False
                break

        if update_ok:
            # add to result the mid number of the update
            result += update[len(update) // 2]

    return result


if __name__ == "__main__":
    print(result())
