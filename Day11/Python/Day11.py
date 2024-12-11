import time
from collections import Counter

start = time.time()
BLINKS_ONE, BLINKS_TWO = 25, 75

# Read input data
f = open("../input.txt", 'r')
stones = Counter([i for i in f.read().split(" ")])

def recursiveBlinkDict(blinks, stones):
    if blinks == 0:
        return sum(stones.values())  # Sum up all counts in the dictionary

    newStones = {}
    for stone, count in stones.items():
        if stone == '0':
            newStones["1"] = newStones.get("1", 0) + count
        elif len(stone) % 2 == 0:
            digits = len(stone) // 2
            first_part, second_part = stone[:digits], stone[digits:]
            newStones[str(int(second_part))] = newStones.get(str(int(second_part)), 0) + count
            newStones[str(first_part)] = newStones.get(str(first_part), 0) + count
        else:
            transformed = str(int(stone) * 2024)
            newStones[transformed] = newStones.get(transformed, 0) + count
    
    stones.clear()  # Clear memory for the previous dictionary
    stones.update(newStones)  # Update stones in-place
    newStones.clear()

    return recursiveBlinkDict(blinks - 1, stones)

print("#"*50 + f"\nAdvent of Code 2024\n\t- Day 10\n\t\t★  Result: {recursiveBlinkDict(BLINKS_ONE, stones)}\n\t\t★★ Result: {recursiveBlinkDict(BLINKS_TWO, stones)}\n" + "#"*50)
print(f"Execution Time {time.time()-start} seconds")