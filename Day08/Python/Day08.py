import time
import math
start = time.time()

def antinodesA(A, B, rows, cols):
    xA, yA = A
    xB, yB = B    
    result = []
    
    ABx, ABy = xB - xA, yB - yA
    BAx, BAy = xA - xB, yA - yB

    xZ = xA + 2* ABx
    yZ = yA + 2* ABy

    xW = xB + 2* BAx
    yW = yB + 2* BAy
        
    # Check if the antinodes are within the map bounds
    if (0 <= xZ < rows) and (0 <= yZ < cols):
        result.append((xZ, yZ))
    if (0 <= xW < rows) and (0 <= yW < cols):    
        result.append((xW, yW))
    return result

def antinodesB(A, B, rows, cols):
    xA, yA = A
    xB, yB = B    
    result = []

    ABx, ABy = xB - xA, yB - yA
    BAx, BAy = xA - xB, yA - yB
    
    for distance in range(cols):
    
        xZ = xA + distance * ABx
        yZ = yA + distance * ABy

        xW = xB + distance * BAx
        yW = yB + distance * BAy

        # Check if the antinodes are within the map bounds
        if (0 <= xZ < rows) and (0 <= yZ < cols):
            result.append((xZ, yZ))
        if (0 <= xW < rows) and (0 <= yW < cols):    
            result.append((xW, yW))

    return result

# Read input data
f = open("../input.txt", 'r')
file = f.read()
lines = [i for i in file.split("\n")]

rows, cols = len(lines), len(lines[0])

antennas = dict()

for i in range(rows*cols):
    x,y = i//cols, i%cols
    if lines[x][y] != ".":
        if lines[x][y] in antennas:
            antennas[lines[x][y]].append((x,y))
        else:
            antennas[lines[x][y]] = [(x,y)]

resultOne, resultTwo = [],[]
for key in antennas.keys():
    for i in range(len(antennas[key])):
        for j in range(i,len(antennas[key])):
            if i == j:
                continue
            if len(antennas[key]) <= 1:
                break
            resultOne += antinodesA(antennas[key][i], antennas[key][j], rows, cols)
            resultTwo += antinodesB(antennas[key][i], antennas[key][j], rows, cols)
            
resultOne = set(resultOne)
resultTwo = set(resultTwo)

# Print results
print("#"*50 + f"\nAdvent of Code 2024\n\t- Day 07\n\t\t★  Result: {len(resultOne)}\n\t\t★★ Result: {len(resultTwo)}\n" + "#"*50)
print(f"Execution Time {time.time()-start} seconds")
