import time
import itertools
start = time.time()

# Read input data
f = open("../input.txt", 'r')
file = f.read() 

memory = []
ID = 0
for i in range(len(file)):
    if i % 2 == 0:
        memory += itertools.repeat(ID,int(file[i]))
        ID += 1
    else:   
        memory += itertools.repeat(".",int(file[i]))

memoryPartTwo = memory.copy()
memoryPartOne = memory.copy()

def diskCompacting(memoryPartOne):
    lastFree, exit = 0, False
    for bckInd in range(len(memoryPartOne)-1,0,-1):
        if exit:
            break
        if memoryPartOne[bckInd] != ".":
            for fwdInd in range(lastFree,len(memoryPartOne)):
                if bckInd < fwdInd:
                    exit = True
                    break
                if memoryPartOne[fwdInd] == ".":
                    lastFree = fwdInd+1
                    memoryPartOne[fwdInd] = memoryPartOne[bckInd]
                    memoryPartOne[bckInd] = "."
                    # print(memoryPartOne)
                    break
    return sum([int(memoryPartOne[i])*i if memoryPartOne[i] != "." else 0  for i in range(len(memoryPartOne[:]))])

def fileCompacting(memory):
    # File blocks dictionary {ID: [i,...i+1] ]}
    files = dict()
    
    for i in range(len(memory)):
        if memory[i] != ".":
            if memory[i] not in files:
                files[memory[i]] = [i]
            else:
                aux = files[memory[i]]
                files[memory[i]] = aux + [i]
        

    maxFiles = max(files.keys()) if files else 0

    # Free blocks dictionary {ID: [i,...i+1]}
    free = dict()
    for i in range(maxFiles):
        endA = files[i][-1]
        startB = files[i+1][0]
        if startB - endA > 1:
            free[i] = [i for i in range(endA+1,startB)]


    maxFree = max(free.keys())

    for i in range(maxFiles,0,-1):
        if i not in files:
            continue  # Skip invalid file IDs
        for j in free.keys():
            if len(free[j]) >= len(files[i]):
                if free[j][0] < files[i][0]:
                    num = len(files[i])
                    files[i] = free[j][:len(files[i])]
                    free[j] = free[j][num:]
                    break
                    
                    
    result = 0
    for k, v in files.items():
        result+= sum([k * value for value in v])

    return result

print("#"*50 + f"\nAdvent of Code 2024\n\t- Day 09\n\t\t★  Result: {diskCompacting(memoryPartOne)}\n\t\t★★ Result: {fileCompacting(memory)}\n" + "#"*50)
print(f"Execution Time {time.time()-start} seconds")