#!/usr/bin/env python3
import sys
import heapq
import codecs  # For safe UTF-8 with BOM handling
from collections import deque

# Directions and movement vectors
MOVES = {
    'N': (-1, 0),
    'S': (1, 0),
    'E': (0, 1),
    'W': (0, -1)
}

class State:
    def __init__(self, position, dirty):
        self.position = position        # (row, col)
        self.dirty = frozenset(dirty)   # frozen set of (row, col)

    def __eq__(self, other):
        return self.position == other.position and self.dirty == other.dirty

    def __hash__(self):
        return hash((self.position, self.dirty))


def parse_world(file_path):
    # Handle UTF-8 with BOM
    with codecs.open(file_path, 'r', encoding='utf-8-sig') as f:
        cols = int(f.readline())
        rows = int(f.readline())
        grid = []
        start = None
        dirty = set()
        for r in range(rows):
            line = f.readline().strip()
            row = []
            for c, ch in enumerate(line):
                if ch == '@':
                    start = (r, c)
                    row.append('_')
                elif ch == '*':
                    dirty.add((r, c))
                    row.append('*')
                else:
                    row.append(ch)
            grid.append(row)
    return grid, start, dirty


def get_neighbors(state, grid):
    neighbors = []
    r, c = state.position

    # Move in 4 directions
    for action, (dr, dc) in MOVES.items():
        nr, nc = r + dr, c + dc
        if 0 <= nr < len(grid) and 0 <= nc < len(grid[0]):
            if grid[nr][nc] != '#':
                neighbors.append((action, State((nr, nc), state.dirty)))

    # Vacuum current cell if dirty
    if state.position in state.dirty:
        new_dirty = set(state.dirty)
        new_dirty.remove(state.position)
        neighbors.append(('V', State(state.position, new_dirty)))

    return neighbors


def reconstruct_path(came_from, end_state):
    path = []
    while came_from[end_state][0] is not None:
        action, prev = came_from[end_state]
        path.append(action)
        end_state = prev
    return path[::-1]


def dfs(start_state, grid):
    stack = [(start_state, [])]
    visited = set()
    nodes_generated = 0
    nodes_expanded = 0

    while stack:
        current_state, path = stack.pop()
        if current_state in visited:
            continue
        visited.add(current_state)
        nodes_expanded += 1

        if not current_state.dirty:
            for action in path:
                print(action)
            print(f"{nodes_generated} nodes generated")
            print(f"{nodes_expanded} nodes expanded")
            return

        for action, neighbor in reversed(get_neighbors(current_state, grid)):
            if neighbor not in visited:
                stack.append((neighbor, path + [action]))
                nodes_generated += 1


def ucs(start_state, grid):
    heap = [(0, id(start_state), start_state)]
    came_from = {start_state: (None, None)}
    cost_so_far = {start_state: 0}
    nodes_generated = 0
    nodes_expanded = 0

    while heap:
        cost, _, current_state = heapq.heappop(heap)
        nodes_expanded += 1

        if not current_state.dirty:
            path = reconstruct_path(came_from, current_state)
            for action in path:
                print(action)
            print(f"{nodes_generated} nodes generated")
            print(f"{nodes_expanded} nodes expanded")
            return

        for action, neighbor in get_neighbors(current_state, grid):
            new_cost = cost + 1
            if neighbor not in cost_so_far or new_cost < cost_so_far[neighbor]:
                cost_so_far[neighbor] = new_cost
                heapq.heappush(heap, (new_cost, id(neighbor), neighbor))
                came_from[neighbor] = (action, current_state)
                nodes_generated += 1


def main():
    if len(sys.argv) != 3:
        print("Usage: python3 planner.py [uniform-cost|depth-first] [world-file]")
        sys.exit(1)

    algorithm = sys.argv[1]
    file_path = sys.argv[2]

    grid, start_pos, dirty = parse_world(file_path)
    start_state = State(start_pos, dirty)

    if algorithm == "depth-first":
        dfs(start_state, grid)
    elif algorithm == "uniform-cost":
        ucs(start_state, grid)
    else:
        print("Unknown algorithm:", algorithm)
        sys.exit(1)


if __name__ == "__main__":
    main()
