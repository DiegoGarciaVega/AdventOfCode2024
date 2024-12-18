import numpy as np
import time
import heapq
import os

start = time.time()
# Global Vars
BYTES = 1024
ROWS, COLS, = 71, 71
SRC  = [0, 0]
DEST = [70, 70]
filepath = "../input.txt"

def printGrid(grid):
    for row in grid:
        print(''.join(row))

def clear_terminal():
    os.system('cls' if os.name == 'nt' else 'clear')
"""
A* algorithm
"""
# Define the Cell class
class Cell:
    def __init__(self):
        # Parent cell's row index
        self.parent_i = 0
        # Parent cell's column index
        self.parent_j = 0
        # Total cost of the cell (g + h)
        self.f = float('inf')
        # Cost from start to this cell
        self.g = float('inf')
        # Heuristic cost from this cell to destination
        self.h = 0

def is_valid(row, col):
    return (row >= 0) and (row < ROWS) and (col >= 0) and (col < COLS)

def is_unblocked(grid, row, col):
    return grid[row][col] == "🟩"

def is_destination(row, col, dest):
    return row == dest[0] and col == dest[1]

def calculate_h_value(row, col, dest):
    return abs(row - dest[0]) + abs(col - dest[1])

def trace_path(cell_details, dest, animation=False):
    path = []
    row = dest[0]
    col = dest[1]

    # Trace the path from destination to source using parent cells
    while not (cell_details[row][col].parent_i == row and cell_details[row][col].parent_j == col):
        path.append((row, col))
        temp_row = cell_details[row][col].parent_i
        temp_col = cell_details[row][col].parent_j
        row = temp_row
        col = temp_col

    # Add the source cell to the path
    path.append((row, col))
    # Reverse the path to get the path from source to destination
    path.reverse()
    if animation:
        # Print the path
        for i in path:
            # print("->", i, end=" ")
            printGrid(grid)
            grid[i[0]][i[1]] = "🟦"
            time.sleep(1/16)
            clear_terminal()
    
    return path

def a_star_search(grid, src, dest, animation=False):
    # Check if the source and destination are valid
    if not is_valid(src[0], src[1]) or not is_valid(dest[0], dest[1]):
        return False, []

    # Check if the source and destination are unblocked
    if not is_unblocked(grid, src[0], src[1]) or not is_unblocked(grid, dest[0], dest[1]):
        return False, []

    # Check if we are already at the destination
    if is_destination(src[0], src[1], dest):
        return True, []

    # Initialize the closed list (visited cells)
    closed_list = [[False for _ in range(COLS)] for _ in range(ROWS)]
    # Initialize the details of each cell
    cell_details = [[Cell() for _ in range(COLS)] for _ in range(ROWS)]

    # Initialize the start cell details
    i = src[0]
    j = src[1]
    cell_details[i][j].f = 0
    cell_details[i][j].g = 0
    cell_details[i][j].h = 0
    cell_details[i][j].parent_i = i
    cell_details[i][j].parent_j = j

    # Initialize the open list (cells to be visited) with the start cell
    open_list = []
    heapq.heappush(open_list, (0.0, i, j))

    # Initialize the flag for whether destination is found
    found_dest = False

    # Main loop of A* search algorithm
    while len(open_list) > 0:
        # Pop the cell with the smallest f value from the open list
        p = heapq.heappop(open_list)

        # Mark the cell as visited
        i = p[1]
        j = p[2]
        closed_list[i][j] = True

        # For each direction, check the successors
        directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]
        for dir in directions:
            new_i = i + dir[0]
            new_j = j + dir[1]

            # If the successor is valid, unblocked, and not visited
            if is_valid(new_i, new_j) and is_unblocked(grid, new_i, new_j) and not closed_list[new_i][new_j]:
                # If the successor is the destination
                if is_destination(new_i, new_j, dest):
                    # Set the parent of the destination cell
                    cell_details[new_i][new_j].parent_i = i
                    cell_details[new_i][new_j].parent_j = j
                    
                    # Trace and print the path from source to destination
                    path = trace_path(cell_details, dest)
                    found_dest = True
                    return found_dest, path
                else:
                    # Calculate the new f, g, and h values
                    g_new = cell_details[i][j].g + 1.0
                    h_new = calculate_h_value(new_i, new_j, dest)
                    f_new = g_new + h_new

                    # If the cell is not in the open list or the new f value is smaller
                    if cell_details[new_i][new_j].f == float('inf') or cell_details[new_i][new_j].f > f_new:
                        # Add the cell to the open list
                        heapq.heappush(open_list, (f_new, new_i, new_j))
                        # Update the cell details
                        cell_details[new_i][new_j].f = f_new
                        cell_details[new_i][new_j].g = g_new
                        cell_details[new_i][new_j].h = h_new
                        cell_details[new_i][new_j].parent_i = i
                        cell_details[new_i][new_j].parent_j = j

    # If the destination is not found after visiting all cells
    if not found_dest:
        return False, []

if __name__ == "__main__":
    file = open(filepath, 'r').read()
    bytes = np.array([list(map(int,line.split(","))) for line in file.split("\n")])
    grid = np.ones(shape=(ROWS,COLS),dtype=str)
    grid[grid == "1"] = "🟩"
    counter = 0

    for i in range(len(bytes)):
        col, row = bytes[i]
        previousGrid = grid.copy() 
        grid[row][col] = "🟥"
        reachable, path = a_star_search(grid, SRC, DEST)
        if counter == BYTES:
            partOne = len(path)-1
        if not reachable:
            difference = grid != previousGrid
            index = np.where(difference)
            partTwo = (int(index[1]), int(index[0]))
            break
        counter +=1

    print("#"*50 + f"\nAdvent of Code 2024\n\t- Day 18\n\t\t★  Result: {partOne}\n\t\t★★ Result: {partTwo}\n" + "#"*50)
    print(f"Execution Time {time.time() - start} seconds")