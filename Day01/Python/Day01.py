f = open ("../input.txt",'r')

leftList = list()
rightList = list()

# Reading file and adding elements to list
for lines in f:
    line = lines.split()
    leftList.append(int(line[0]))
    rightList.append(int(line[1]))


leftList.sort()
rightList.sort()

totalDistance = 0
for leftElement, rightElement in (zip(leftList, rightList)):
    totalDistance += abs(leftElement - rightElement)

print("#"*50 + f"\nAdvent of Code 2024\n\t⍟ Day 01 Result: {totalDistance}\n" + "#"*50)