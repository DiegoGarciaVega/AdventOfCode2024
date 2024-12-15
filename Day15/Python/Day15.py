import numpy as np
import time

start = time.time()

MOVEMENTS = {"^": [-1, 0],    # UP     ↑
            ">": [0, 1],     # RIGHT  →
            "v": [1, 0],     # DOWN   ↓
            "<": [0, -1]}    # LEFT   ←

file = open("../input.txt", 'r').read().split("\n\n")
grid  = np.array([[pos for pos in line] for line in file[0].split("\n")])
moves = ''.join(file[1].split("\n"))

ROWS, COLS = len(grid), len(grid[0])

for move in moves:
    # os.system('cls' if os.name == 'nt' else 'clear')
    # print(f"Move {move}:")
    x, y = np.where(grid =="@")
    x, y = x[0], y[0]
    moveX, moveY = MOVEMENTS[move]
    nextX, nextY = x + moveX, y + moveY
    nextPos = grid[nextX][nextY]
    
    if nextPos == ".":
        grid[x][y] = "."
        grid[nextX][nextY] = "@"
    elif nextPos == "O": 
        match move:
            case "^":
                check = [(i, y) for i in range(x-1, -1, -1)]
            case "v":
                check = [(i, y) for i in range(x+1, ROWS)]
            case "<":
                check = [(x, i) for i in range(y-1, -1, -1)]
            case ">":
                check = [(x, i) for i in range(y+1, COLS)]
        values = list(map(lambda coord: grid[coord[0]][coord[1]] , check))
        
        if "." in values[:values.index("#")]:
            previous = None
            # Can move the boxes
            for position in check:
                nextX, nextY = position
                if previous is None:
                    previous = grid[nextX][nextY]
                    grid[nextX][nextY] = "@"
                    grid[x][y] = "."
                    continue
                elif grid[nextX][nextY] == ".":
                    grid[nextX][nextY] = previous
                    break
                
    # print('\n'.join(''.join(row) for row in grid))
    
partOne = 0
for i in range(ROWS*COLS):
    x, y = i // COLS, i % COLS
    if grid[x][y] == "O":
        partOne += 100 * x + y


print("#"*50 + f"\nAdvent of Code 2024\n\t- Day 15\n\t\t★  Result: {partOne}\n\t\t★★ Result: {0}\n" + "#"*50)
print(f"Execution Time {time.time() - start} seconds")