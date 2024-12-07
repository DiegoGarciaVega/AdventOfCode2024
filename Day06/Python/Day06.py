import os
import time
import numpy as np
import multiprocessing as mp

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

def traverse(grid, x, y, obsX, obsY, rotationID):
    # Create a copy of the grid to avoid modifying the original
    temp_grid = grid.copy()
    
    # Current position and rotation
    curr_x, curr_y, curr_rotationID = x, y, rotationID
    
    # Mark obstacle
    temp_grid[obsX, obsY] = "#"
    
    # Keep track of visited states
    seen = set()
    
    while True:
        # Current state includes position and rotation
        state = (curr_x, curr_y, curr_rotationID)
        
        # Check if we've been in this state before
        if state in seen:
            return True  # Loop detected
        
        # Add current state to seen
        seen.add(state)
        
        # Calculate next position based on current rotation
        nextX = curr_x + rotations[curr_rotationID][0]
        nextY = curr_y + rotations[curr_rotationID][1]
        
        # Check if next position is out of bounds
        if nextX < 0 or nextX >= rows or nextY < 0 or nextY >= cols:
            return False  # Out of bounds
        
        # If next position is an obstacle, rotate
        if temp_grid[nextX, nextY] == "#":
            curr_rotationID = (curr_rotationID + 1) % 4
        else:
            # Move to the next position
            curr_x, curr_y = nextX, nextY

def main():
    # Part One: Guard Route
    obstacles = []
    visited_positions = set()
    
    # Reset starting position
    x, y = startingPoint[0][0], startingPoint[1][0]
    rotationID = 0
    
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

    # Part Two: Finding Valid Obstruction Positions with Multiprocessing
    # Prepare arguments for multiprocessing
    start_x, start_y = startingPoint[0][0], startingPoint[1][0]
    
    # Filter out starting point and existing walls
    check_positions = [pos for pos in visited_positions 
                        if pos != (start_x, start_y) and grid[pos[0], pos[1]] != "#"]
    
    # Prepare arguments for multiprocessing: [(grid, start_x, start_y, obsX, obsY, initial_rot)]
    mp_args = [(grid, start_x, start_y, obsX, obsY, 0) 
                for obsX, obsY in check_positions]
    
    # Use all available CPU cores
    with mp.Pool(processes=mp.cpu_count()) as pool:
        loop_results = pool.starmap(traverse, mp_args)
    
    # Count valid positions (those that create a loop)
    valid_positions = sum(loop_results)

    # Final results
    print("#" * 50)
    print(f"Advent of Code 2024\n\t- Day 06\n\t\t★  Result: {np.count_nonzero(grid == 'X')}")
    print(f"\t\t★★ Result: {valid_positions}")
    print("#" * 50)

if __name__ == "__main__":
    start_time = time.time()
    main()
    end_time = time.time()
    print(f"\nTotal Execution Time: {end_time - start_time:.2f} seconds")