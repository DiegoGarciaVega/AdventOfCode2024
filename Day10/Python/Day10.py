import time
import numpy as np
from queue import LifoQueue 

start = time.time()

# Read input data
f = open("../input.txt", 'r')
grid = np.array([[int(j) for j in i] for i in f.read().split("\n") ])

rows, cols = len(grid), len(grid[0])
zeros = np.where(grid == 0)
# Define movement directions
movements = ([-1, 0],   # Moving UP     ↑
            [0, 1],     # Moving RIGHT  →
            [1, 0],     # Moving DOWN   ↓
            [0, -1])    # Moving LEFT   ←

def pathing(grid, p0, p1,rows,cols, all=False ):
    # Create a copy of the grid to avoid modifying the original
    result = 0
    tempGrid = grid.copy()
    stack = LifoQueue()
    visitedNines = set()
    stack.put((p0,p1))
    while True:
        # Check all possible moves
        if not stack.empty():
            # Pop next move
            x, y = stack.get()
        else:
            break
        for i, j in movements:
            newX, newY = x+i, y+j
            if newX < 0 or newX >= rows or newY < 0 or newY >= cols:
                continue
            # Check if there are possible movements
            if tempGrid[x][y] + 1 == tempGrid[newX][newY]:
                if tempGrid[newX][newY] == 9:
                    pos = (int(newX),int(newY))
                    if pos in visitedNines and not all:
                        continue
                    else:
                        visitedNines.add(pos)
                        result += 1 
                else:
                    stack.put((newX, newY))
    return result

partOne, partTwo = 0, 0
for x, y in zip(zeros[0],zeros[1]):
    partOne += pathing(grid, x, y, rows, cols)
    partTwo += pathing(grid, x, y, rows, cols, all=True)

print("#"*50 + f"\nAdvent of Code 2024\n\t- Day 10\n\t\t★  Result: {partOne}\n\t\t★★ Result: {partTwo}\n" + "#"*50)
print(f"Execution Time {time.time()-start} seconds")