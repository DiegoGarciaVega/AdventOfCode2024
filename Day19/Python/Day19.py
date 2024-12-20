import time

def count(target: str, patterns: set[str], memo: dict = None) -> int:
    if memo is None:
        memo = {}
    
    # Base cases
    if not target:  # Empty string can be formed in exactly one way
        return 1
    if target in memo:  # Return memoized result if available
        return memo[target]
    
    total_combinations = 0
    # Try each pattern as a potential prefix
    for pattern in patterns:
        if target.startswith(pattern):
            # Recursively count combinations for remaining substring
            remaining = target[len(pattern):]
            total_combinations += count(remaining, patterns, memo)
    
    # Memoize the total number of combinations for this target
    memo[target] = total_combinations
    return total_combinations

def solve(file_path: str):
    content = open(file_path, 'r').read()
    available_towels, wanted_towels = content.split("\n\n")
    
    # Process patterns and designs
    patterns = {p.strip() for p in available_towels.replace(" ", "").split(",")}
    designs = [d.strip() for d in wanted_towels.splitlines()]
    
    possible_count = 0  # Part 1 result
    total_combinations = 0  # Part 2 result
    
    for design in designs:
        combinations = count(design, patterns)
        if combinations > 0:
            possible_count += 1
        total_combinations += combinations
    
    return possible_count, total_combinations

start = time.time()
partOne, partTwo = solve("../input.txt")
print("#"*50 + f"\nAdvent of Code 2024\n\t- Day 19\n\t\t★  Result: {partOne}\n\t\t★★ Result: {partTwo}\n" + "#"*50)
print(f"Execution Time {time.time() - start} seconds")