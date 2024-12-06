import sys
from collections import defaultdict, deque


def parse_input():
    input_data = sys.stdin.read().strip().split("\n")
    rules = []
    updates = []

    # Parse rules until an empty line
    for line in input_data:
        if "|" in line:
            x, y = map(int, line.split("|"))
            rules.append((x, y))
        else:
            break

    # Parse updates (comma-separated lists)
    for line in input_data[len(rules) :]:
        if line.strip():
            updates.append(list(map(int, line.split(","))))

    return rules, updates


def build_graph(rules):
    graph = defaultdict(list)
    in_degree = defaultdict(int)

    for x, y in rules:
        graph[x].append(y)
        in_degree[y] += 1
        if x not in in_degree:
            in_degree[x] = 0

    return graph, in_degree


def is_ordered(update, graph, in_degree):
    order_map = {page: idx for idx, page in enumerate(update)}
    for x in update:
        for y in graph[x]:
            if y in order_map and order_map[x] > order_map[y]:
                return False
    return True


def topological_sort(update, graph, in_degree):
    subgraph = {node: [] for node in update}
    sub_in_degree = {node: 0 for node in update}

    for node in update:
        for neighbor in graph[node]:
            if neighbor in update:
                subgraph[node].append(neighbor)
                sub_in_degree[neighbor] += 1

    queue = deque([node for node in update if sub_in_degree[node] == 0])
    sorted_order = []

    while queue:
        node = queue.popleft()
        sorted_order.append(node)
        for neighbor in subgraph[node]:
            sub_in_degree[neighbor] -= 1
            if sub_in_degree[neighbor] == 0:
                queue.append(neighbor)

    return sorted_order


def find_middle(update):
    return update[len(update) // 2]


def main():
    rules, updates = parse_input()
    graph, in_degree = build_graph(rules)

    corrected_middle_sum = 0

    for update in updates:
        if not is_ordered(update, graph, in_degree):
            # Fix the update using topological sorting
            sorted_update = topological_sort(update, graph, in_degree)
            corrected_middle_sum += find_middle(sorted_update)

    print(corrected_middle_sum)


if __name__ == "__main__":
    main()
