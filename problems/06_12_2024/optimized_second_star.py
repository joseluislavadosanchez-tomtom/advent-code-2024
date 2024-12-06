import sys

# Directions: Up=0, Right=1, Down=2, Left=3
DIRS = [(-1, 0), (0, 1), (1, 0), (0, -1)]
DIRECTION_MAP = {'^':0, '>':1, 'v':2, '<':3}

def turn_right(d):
    return (d+1) % 4

def read_matrix():
    lines = [l.rstrip('\n') for l in sys.stdin]
    n = len(lines)
    m = len(lines[0])
    grid = [[False]*m for _ in range(n)]
    start = (-1, -1)
    start_dir = -1

    for r, line in enumerate(lines):
        for c, ch in enumerate(line):
            if ch == '#':
                grid[r][c] = True
            elif ch in DIRECTION_MAP:
                start = (r, c)
                start_dir = DIRECTION_MAP[ch]

    return grid, start, start_dir, n, m

def in_bounds(r, c, n, m):
    return 0 <= r < n and 0 <= c < m

def build_state_machine(grid, n, m, start, start_dir):
    def state_index(r, c, d):
        return ((r*m) + c)*4 + d

    total_states = n*m*4
    next_state = [-1]*(total_states)
    affected_states = [[[] for _ in range(m)] for __ in range(n)]

    # Precompute transitions
    for r in range(n):
        for c in range(m):
            if grid[r][c]:
                continue
            for d in range(4):
                st = state_index(r,c,d)

                def try_move(r0, c0, d0):
                    # Attempt up to 4 turns (0 to 3 rights)
                    for _ in range(4):
                        fr0, fc0 = r0 + DIRS[d0][0], c0 + DIRS[d0][1]
                        if not in_bounds(fr0, fc0, n, m) or grid[fr0][fc0]:
                            d0 = turn_right(d0)
                            continue
                        return (fr0, fc0, d0)
                    return None

                res = try_move(r, c, d)
                if res is None:
                    next_state[st] = -1
                else:
                    nr, nc, nd = res
                    nst = ((nr*m)+nc)*4+nd
                    next_state[st] = nst
                    affected_states[nr][nc].append(st)

    start_state = ((start[0]*m)+start[1])*4 + start_dir
    return next_state, affected_states, start_state

def get_patrol_path(next_state, start_state, n, m):
    # Follow path and record visited positions until out-of-map or cycle
    visited_positions = []
    visited_states = [False]*len(next_state)
    visited_cells = [False]*(n*m)

    s = start_state
    while s != -1:
        if visited_states[s]:
            # We've hit a state we've seen before: cycle detected
            break
        visited_states[s] = True

        pos = s // 4
        if not visited_cells[pos]:
            visited_cells[pos] = True
            visited_positions.append(pos)

        s = next_state[s]

    return visited_positions

def follow_path_check_loop(next_state, start_state):
    # Check loop by following from start_state
    visited = [False]*len(next_state)
    s = start_state
    while s != -1:
        if visited[s]:
            return True
        visited[s] = True
        s = next_state[s]
    return False

def place_obstruction_and_check_loop(
    next_state,
    affected_states,
    grid,
    n, m,
    start_state,
    obstruct_r,
    obstruct_c
):
    original = grid[obstruct_r][obstruct_c]
    grid[obstruct_r][obstruct_c] = True

    def state_index_to_rcd(st):
        pos = st // 4
        d = st % 4
        r = pos // m
        c = pos % m
        return r, c, d

    def try_move(r0, c0, d0):
        for _ in range(4):
            fr0, fc0 = r0 + DIRS[d0][0], c0 + DIRS[d0][1]
            if not in_bounds(fr0, fc0, n, m) or grid[fr0][fc0]:
                d0 = turn_right(d0)
                continue
            return (fr0, fc0, d0)
        return None

    changed = affected_states[obstruct_r][obstruct_c]
    old_vals = []
    for st in changed:
        old_n = next_state[st]
        r, c, d = state_index_to_rcd(st)
        res = try_move(r, c, d)
        if res is None:
            next_state[st] = -1
        else:
            nr, nc, nd = res
            next_state[st] = ((nr*m)+nc)*4+nd
        old_vals.append((st, old_n))

    loop_found = follow_path_check_loop(next_state, start_state)

    # Revert
    for st, ov in old_vals:
        next_state[st] = ov
    grid[obstruct_r][obstruct_c] = original

    return loop_found

def main():
    grid, start, start_dir, n, m = read_matrix()
    next_state, affected_states, start_state = build_state_machine(grid, n, m, start, start_dir)
    patrol_path_positions = get_patrol_path(next_state, start_state, n, m)

    start_pos = (start[0]*m)+start[1]

    count = 0
    for pos in patrol_path_positions:
        if pos == start_pos:
            continue
        r = pos // m
        c = pos % m
        if grid[r][c]:
            continue
        if place_obstruction_and_check_loop(next_state, affected_states, grid, n, m, start_state, r, c):
            count += 1

    print(count)

if __name__ == "__main__":
    main()
