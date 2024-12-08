import time
import math
start = time.time()

checkBounds =  lambda x,y,rows, cols: (0 <= x < rows) and (0 <= y < cols)

def antinodes(A, B, rows, cols,distances=[2]):
    xA, yA = A
    xB, yB = B    
    result = []

    ABx, ABy = xB - xA, yB - yA
    BAx, BAy = ABx*-1, ABy*-1
    
    for distance in distances:
        xZ = xA + distance * ABx
        yZ = yA + distance * ABy

        xW = xB + distance * BAx
        yW = yB + distance * BAy

        # Check if the antinodes are within the map bounds
        if checkBounds(xZ,yZ,rows,cols):
            result.append((xZ, yZ))
        if checkBounds(xW,yW,rows,cols):    
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
            resultOne += antinodes(antennas[key][i], antennas[key][j], rows, cols)
            resultTwo += antinodes(antennas[key][i], antennas[key][j], rows, cols, distances=list(range(cols)))
            
resultOne = set(resultOne)
resultTwo = set(resultTwo)

# Print results
print("#"*50 + f"\nAdvent of Code 2024\n\t- Day 07\n\t\t★  Result: {len(resultOne)}\n\t\t★★ Result: {len(resultTwo)}\n" + "#"*50)
print(f"Execution Time {time.time()-start} seconds")
