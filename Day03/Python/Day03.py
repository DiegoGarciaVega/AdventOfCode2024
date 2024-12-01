import re
f = open("../input.txt",'r')
file = f.read()

partOne = lambda file: sum([int(a)*int(b) for a,b in re.findall(r"mul\(([0-9]+),([0-9]+)\)",file)])
patternMatch = lambda file : [x.group() for x in re.finditer(r"mul\(([0-9]+),([0-9]+)\)|don't\(\)|do\(\)",file)]

def ignoreDont(found):
    do, new = True, []
    for i in found:
        if i == "do()":
            do = True
            continue
        if i == "don't()":
            do = False
            continue
        if "mul" in i and do:
            new.append(i)
    return ''.join(new)

print("#"*50 + f"\nAdvent of Code 2024\n\t- Day 03\n\t\t★  Result: {partOne(file)}\n\t\t★★ Result: {partOne(ignoreDont(patternMatch(file)))}\n" + "#"*50)   