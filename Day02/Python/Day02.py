def checkSafe(list, dampener = False):
    if not dampener:
        difs = [int(list[i-1]) - int(list[i]) for i in range(1,len(list))]
        positive, negative, cont  = sum(x > 0 for x in difs), sum(x < 0 for x in difs), 0
        cont = abs(abs(positive - negative) - len(difs)) + sum([i==0 for i in difs]) + sum([abs(i) > 3 for i in difs])
        return (cont == 0)
    else:
        return any(checkSafe(sub_list) for sub_list in ([list[:i] + list[i+1:] for i in range(len(list))]))

f = open("../input.txt",'r')
file = f.read().strip().split("\n")
safe = sum([checkSafe(i.split(" ")) for i in file])
dampened = sum([checkSafe(i.split(" "),dampener=True) for i in file])
print("#"*50 + f"\nAdvent of Code 2024\n\t- Day 02\n\t\t★  Result: {safe}\n\t\t★★ Result: {dampened} \n" + "#"*50)   