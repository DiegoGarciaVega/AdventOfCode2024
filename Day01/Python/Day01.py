f = open("../input.txt",'r')
print(f)
leftList = list()
rightList = list()

# Reading file and adding elements to list
for lines in f:
    line = lines.split()
    leftList.append(int(line[0]))
    rightList.append(int(line[1]))

leftList.sort()
rightList.sort()

totalDistance, similarityScore = 0, 0
for leftElement, rightElement in (zip(leftList, rightList)):
    totalDistance += abs(leftElement - rightElement)
    similarityScore += rightList.count(leftElement) * leftElement

print("#"*50 + f"\nAdvent of Code 2024\n\t- Day 01\n\t\t★  Result: {totalDistance}\n\t\t★★ Result: {similarityScore}\n" + "#"*50)