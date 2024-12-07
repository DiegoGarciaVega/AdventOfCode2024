f = open("../input.txt",'r')
file = f.read()
sectionOne, sectionTwo = file.split("\n\n")
sectionOne = [list(map(int,i.split("|"))) for i in sectionOne.split("\n")]
sectionTwo = [list(map(int,i.split(","))) for i in sectionTwo.split("\n")]
rules = {key: [value for _, value in filter(lambda x: x[0] == key, sectionOne)] for key in {k for k, _ in sectionOne}}

def check(updates,rules):
    for i in range(1, len(updates)):
        if updates[i] in rules:
            for page in (rules[updates[i]]):
                if page in updates[:i]:
                    return False
    return True

# Bubble sort
def sort(update, rules):
    for n in range(len(update) - 1, 0, -1):
        swapped = False  
        for i in range(n):
            if update[i+1] in rules:
                if update[i] in rules[update[i+1]]:          
                    update[i], update[i + 1] = update[i + 1], update[i]
                    swapped = True
        if not swapped:
            break
    return update

resultOne = sum([i[len(i)//2] for i in filter(lambda item: check(item,rules=rules), sectionTwo)])
resultTwo = sum([(lambda list: list[len(list)//2])(sort(i,rules)) for i in filter(lambda item: not check(item,rules=rules), sectionTwo)])

print("#"*50 + f"\nAdvent of Code 2024\n\t- Day 05\n\t\t★  Result: {resultOne}\n\t\t★★ Result: {resultTwo}\n" + "#"*50)  