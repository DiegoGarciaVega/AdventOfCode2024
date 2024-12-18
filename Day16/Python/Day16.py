import os
import numpy as np
import time
import math
import heapq
start = time.time()

file = open("../test.txt", 'r').read()
grid = np.array([[pos for pos in line] for line in file.split("\n")])

DIRECTIONS = [  [0, 1],     # RIGHT  →
                [-1, 0],    # UP     ↑
                [1, 0],     # DOWN   ↓
                [0, -1]]    # LEFT   ←

DIRECTION_SYMBOLS = {tuple([0, 1]): '⏩', tuple([1, 0]): '🔽', tuple([0, -1]): '⏪', tuple([-1, 0]): '⏫'}

ROW, COL = len(grid), len(grid[0])

# Define the source and destination
src = np.where(grid == "S")
dest = np.where(grid == "E")
src = (int(src[0].item()), int(src[1].item()))
dest = (int(dest[0].item()), int(dest[1].item()))

grid[src[0]][src[1]] = "❎"
grid[dest[0]][dest[1]] = "⬜"

grid[grid=="."] = "⬛"
grid[grid=="#"] = "🟥"

def clear_terminal():
    os.system('cls' if os.name == 'nt' else 'clear')

def print_grid(grid):
    for row in grid:
        print(' '.join(row))

DIRECTIONS = tuple({tuple([0, 1]): '⏩', tuple([1, 0]): '🔽', tuple([0, -1]): '⏪', tuple([-1, 0]): '⏫'})

def dijkstra(grid, src, dest):
    srcX, srcY = src[0], src[1]
    destX, destY = dest[0], dest[1]

    # Modify distances to be a 3D array to track distances with different previous directions
    distances = np.ones((ROW, COL, len(DIRECTIONS)), dtype=float) * math.inf
    
    # Initialize source node distances for all possible starting directions
    for i in range(len(DIRECTIONS)):
        distances[srcX][srcY][i] = 0

    # Priority queue to store (distance, x, y, prev_direction_index)
    queue = [(0, srcX, srcY, -1)]  # -1 indicates no previous direction

    visited = set()
    animated_grid = [row[:] for row in grid]

    while queue:
        current_dist, x, y, prev_dir_idx = heapq.heappop(queue)
        # Create a unique visited key that includes the direction
        visit_key = (x, y, prev_dir_idx)
        if visit_key in visited:
            continue
        visited.add(visit_key)

        # print(f"Visiting node ({x}, {y}) with distance {current_dist} and prev_dir_idx {prev_dir_idx}")

        if (x, y) == (destX, destY):
            animated_grid[x][y] = '🟢'
            clear_terminal()
            print_grid(animated_grid)
            return distances
        
        # Animate the grid (optional visualization)
        if animated_grid[x][y] not in ('S', 'X'):
            if prev_dir_idx != -1:  # Avoid error at the source node
                # Convert direction to a tuple if it's not already
                prev_dir = tuple(DIRECTIONS[prev_dir_idx])
                # Find the corresponding symbol for this direction
                for symbol_key, symbol_value in DIRECTION_SYMBOLS.items():
                    if tuple(symbol_key) == prev_dir:
                        animated_grid[x][y] = symbol_value
                        break
        clear_terminal()
        print_grid(animated_grid)
        time.sleep(1/16/10)

        for curr_dir_idx, dir in enumerate(DIRECTIONS):
            neighbor = tuple(np.array((x, y)) + np.array(dir))
            if (0 <= neighbor[0] < ROW and 0 <= neighbor[1] < COL and 
                grid[neighbor[0]][neighbor[1]] != '🟥'):
                
                # Calculate turn cost more intelligently
                turn_cost = 0
                if prev_dir_idx != -1:
                    # Significant cost for changing direction
                    if not np.array_equal(dir, DIRECTIONS[prev_dir_idx]):
                        turn_cost = 1000  # High cost for turning
                
                # Base movement cost
                movement_cost = 1
                
                # Total new distance
                new_distance = current_dist + turn_cost + movement_cost

                # Check if this path to the neighbor is shorter
                if new_distance < distances[neighbor[0]][neighbor[1]][curr_dir_idx]:
                    distances[neighbor[0]][neighbor[1]][curr_dir_idx] = new_distance
                    
                    # Push to the queue with updated distance and direction index
                    heapq.heappush(queue, (
                        new_distance, 
                        neighbor[0], 
                        neighbor[1], 
                        curr_dir_idx
                    ))

distances = dijkstra(grid, src, dest)

partOne = int(np.min(distances[dest]))

# distances = dijkstra_with_animation(grid, src, dest)
print("#"*50 + f"\nAdvent of Code 2024\n\t- Day 16\n\t\t★  Result: {partOne}\n\t\t★★ Result: {0}\n" + "#"*50)
print(f"Execution Time {time.time() - start} seconds")