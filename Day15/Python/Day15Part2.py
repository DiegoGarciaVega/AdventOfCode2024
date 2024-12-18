import numpy as np
import time

start = time.time()

MOVEMENTS = {"^": [-1, 0],    # UP     ↑
            ">": [0, 1],     # RIGHT  →
            "v": [1, 0],     # DOWN   ↓
            "<": [0, -1]}    # LEFT   ←

file = open("../input.txt", 'r').read().split("\n\n")
grid = np.array([[pos for pos in line] for line in file[0].split("\n")])

# Create a new grid twice as wide
ROWS, COLS = len(grid), len(grid[0])
grid2 = np.full((ROWS, COLS*2), ".", dtype=str)

# Expand the grid
for x in range(ROWS):
    for y in range(0, COLS*2, 2):
        match grid[x][y // 2]:
            case ".":
                grid2[x][y] = "."
                grid2[x][y+1] = "."
            case "#":
                grid2[x][y] = "#"
                grid2[x][y+1] = "#"
            case "O":
                grid2[x][y] = "["
                grid2[x][y+1] = "]"
            case "@":
                grid2[x][y] = "@"
                grid2[x][y+1] = "."

# Update grid to the expanded version
grid = grid2
ROWS, COLS = len(grid), len(grid[0])
moves = ''.join(file[1].split("\n"))

def can_box_move(grid, start_x, start_y, move):
    """
    Check if a box can move in a given direction without being obstructed
    """
    # Determine box coordinates based on move
    match move:
        case "^":
            check_coords = [(start_x-1, start_y), (start_x-1, start_y+1)]
        case "v":
            check_coords = [(start_x+1, start_y), (start_x+1, start_y+1)]
        case "<":
            check_coords = [(start_x, start_y-1), (start_x, start_y-1)]
        case ">":
            check_coords = [(start_x, start_y+2), (start_x, start_y+2)]
    
    # Check if any of these coordinates are blocked
    return all(grid[x][y] == "." for x, y in check_coords)

def move_robot_and_boxes(grid, x, y, move):
    """
    Move robot and potentially push boxes
    """
    moveX, moveY = MOVEMENTS[move]
    nextX, nextY = x + moveX, y + moveY

    # If next position is empty, just move robot
    if grid[nextX][nextY] == ".":
        grid[x][y] = "."
        grid[nextX][nextY] = "@"
        return grid

    # Check if next position is a box
    if grid[nextX][nextY] in ["[", "]"]:
        # Determine full box coordinates
        if grid[nextX][nextY] == "[":
            box_left, box_right = nextY, nextY+1
        else:
            box_left, box_right = nextY-1, nextY

        # Check if box can move
        if can_box_move(grid, nextX, box_left, move):
            # Move robot and box
            grid[x][y] = "."
            grid[nextX][nextY] = "@"
            
            # Move box
            match move:
                case "^":
                    grid[nextX-1][box_left] = "["
                    grid[nextX-1][box_right] = "]"
                    grid[nextX][box_left] = "."
                    grid[nextX][box_right] = "."
                case "v":
                    grid[nextX+1][box_left] = "["
                    grid[nextX+1][box_right] = "]"
                    grid[nextX][box_left] = "."
                    grid[nextX][box_right] = "."
                case "<":
                    grid[nextX][box_left-1] = "["
                    grid[nextX][box_right-1] = "]"
                    grid[nextX][box_left] = "."
                    grid[nextX][box_right] = "."
                case ">":
                    grid[nextX][box_left+1] = "["
                    grid[nextX][box_right+1] = "]"
                    grid[nextX][box_left] = "."
                    grid[nextX][box_right] = "."
    
    return grid

# Execute moves
for move in moves:
    # Find robot position
    x, y = np.where(grid =="@")
    
    # Move robot and potentially boxes
    grid = move_robot_and_boxes(grid, x, y, move)

# Calculate GPS coordinates
partTwo = 0
for x in range(ROWS):
    for y in range(COLS):
        if grid[x][y] == "[":
            partTwo += 100 * x + y

print("#"*50 + f"\nAdvent of Code 2024\n\t- Day 15\n\t\t★★ Part Two Result: {partTwo}\n" + "#"*50)
print(f"Execution Time {time.time() - start} seconds")

# Optional: Print final grid for debugging
print('\n'.join(''.join(row) for row in grid))