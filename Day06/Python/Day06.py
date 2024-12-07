import os
import time
import numpy as np

# Read and parse the input
f = open("../input.txt", 'r')
file = f.read().strip()
grid = np.array([[j for j in i] for i in file.split("\n")])
rows, cols = len(grid), len(grid[0])
startingPoint = np.where(grid == '^')

x, y = startingPoint[0][0], startingPoint[1][0]

# Define movement directions
rotations = ([-1, 0],   # Moving UP     ↑
            [0, 1],     # Moving RIGHT  →
            [1, 0],     # Moving DOWN   ↓
            [0, -1])    # Moving LEFT   ←
rotationID = 0
loops = 0  # Accumulator for Part Two

def prettyPrint(grid):
    """Display the grid with 'X' highlighted."""
    RESET = '\033[0m'
    BLUE = '\033[34m'
    colored_result = '\n'.join(
        ''.join(BLUE + 'X' + RESET if char == 'X' else char for char in row)
        for row in grid)
    time.sleep(.1)
    os.system('clear')
    print(colored_result)

def traverse(grid, x, y, obsX, obsY, rotationID):
    """Traverse the grid and detect loops, incrementing the global loops counter."""
    startX, startY, startRot = x, y, rotationID
    seen = set()  # Keep track of visited (x, y, rotationID)
    TTL = 130**2  # Arbitrary limit to prevent infinite loops
    
    # Mark obstacle
    grid[obsX, obsY] = "#"
    while TTL > 0:
        TTL -= 1
        state = (x, y, rotationID)
        if state in seen:
            return True  # Loop detected
        seen.add(state)
        
        nextX, nextY = x + rotations[rotationID][0], y + rotations[rotationID][1]
        if nextX < 0 or nextX >= rows or nextY < 0 or nextY >= cols:
            return False  # Out of bounds
        
        if grid[nextX, nextY] == "#":
            rotationID = (rotationID + 1) % 4
        else:
            x, y = nextX, nextY

    return False  # Exceeded time-to-live

# Part One: Guard Route
obstacles = []
visited_positions = set()
while True:
    grid[x, y] = 'X'
    visited_positions.add((x, y))
    nextX, nextY = x + rotations[rotationID][0], y + rotations[rotationID][1]
    
    if (nextX < 0 or nextX >= rows) or (nextY < 0 or nextY >= cols):
        break  # Out of bounds
    
    if grid[nextX, nextY] == "#":
        rotationID = (rotationID + 1) % 4
        obstacles.append((int(nextX), int(nextY)))
        x, y = x + rotations[rotationID][0], y + rotations[rotationID][1]
    else:
        x, y = nextX, nextY

# Part Two: Finding Valid Obstruction Positions
valid_positions = 0
for obsX, obsY in visited_positions:
    if (obsX, obsY) == (startingPoint[0][0], startingPoint[1][0]) or grid[obsX, obsY] == "#":
        continue  # Skip guard's starting position or existing walls
    temp_grid = grid.copy()
    if traverse(temp_grid, startingPoint[0][0], startingPoint[1][0], obsX, obsY, 0):
        valid_positions += 1

# Final results
print("#" * 50)
print(f"Advent of Code 2024\n\t- Day 06\n\t\t★  Result: {np.count_nonzero(grid == 'X')}")
print(f"\t\t★★ Result: {valid_positions}")
print("#" * 50)
