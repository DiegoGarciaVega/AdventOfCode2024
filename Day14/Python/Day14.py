import time
import numpy as np
from matplotlib import pyplot as plt

start = time.time()

ROWS, COLS = 103, 101
SECONDS = 10000

# Read and parse the input
f = open("../input.txt", 'r')
results = []

robotsX  = np.array([], dtype=int)
robotsY  = np.array([], dtype=int)
robotsVX = np.array([], dtype=int)
robotsVY = np.array([], dtype=int)

SAVE = 7132
# Process each line
for line in f.readlines():
    line = line.strip()  # Remove any leading/trailing whitespace
    if line:  # Ensure the line is not empty
        # Split into position and velocity parts
        parts = line.split()
        position = parts[0].split('=')[1]  # Extract the "0,4" part
        velocity = parts[1].split('=')[1]  # Extract the "3,-3" part

        # Extract x, y, vx, vy as integers
        y, x = map(int, position.split(','))
        vy, vx = map(int, velocity.split(','))

        # Store the results in a dictionary (or any other preferred format)
        robotsX  = np.append(robotsX, x)
        robotsY  = np.append(robotsY, y)
        robotsVX = np.append(robotsVX, vx)
        robotsVY = np.append(robotsVY, vy)

grid = np.zeros((ROWS,COLS), dtype=int)
# Initialize GRID
for robot in range(len(robotsX)):
    grid[robotsX[robot], robotsY[robot]] += 1  

levels = []
entropies = []
for i in range(SECONDS):
    for robot in range(len(robotsX)):
        # Get current robot position
        x, y = robotsX[robot], robotsY[robot]
        newX, newY = x, y

        # Remove robot from current position
        grid[x, y] -= 1
        
        # Calculate new position with WRAP
        newX = (x + robotsVX[robot]) % ROWS
        if newX < 0:
            newX += ROWS
        newY = (y + robotsVY[robot]) % COLS
        if newY < 0:
            newY += COLS
        
        # Add robot to new position and update its position in the array
        grid[newX, newY] += 1
        robotsX[robot], robotsY[robot] = newX, newY
    
    if i == SAVE-1:
        egg = grid.copy()

    midR = ROWS // 2
    midC = COLS // 2

    Q1 = np.sum(grid[:midR, :midC])
    Q2 = np.sum(grid[:midR, midC+1:])
    Q3 = np.sum(grid[midR+1:, :midC])
    Q4 = np.sum(grid[midR+1:, midC+1:])

    danger = Q1 * Q2 * Q3 * Q4
    levels.append(danger)
    
    marg = np.histogramdd(np.ravel(grid), bins = 256)[0]/grid.size
    marg = list(filter(lambda p: p > 0, np.ravel(marg)))
    entropy = -np.sum(np.multiply(marg, np.log2(marg)))
    entropies.append(entropy)


tree = np.argmin(levels)+1
caos = np.argmin(entropies)

plt.imshow(egg)
plt.show()

print("#"*50 + f"\nAdvent of Code 2024\n\t- Day 10\n\t\t★  Result: {danger}\n\t\t★★ Result: {tree}\n" + "#"*50)
print(f"Execution Time {time.time()-start} seconds")