import itertools
import time
from multiprocessing import Pool
import multiprocessing as mp

def evaluate(nums, operators):
    result = int(nums[0])
    for i in range(1, len(nums)):
        op = operators[i-1]
        num = int(nums[i])
        
        # Apply operations more efficiently using conditional checks
        if op == '+':
            result += num
        elif op == '*':
            result *= num
        elif op == '||':
            # Combine numbers as strings when "||" is encountered
            result = int(str(result) + str(num))
    
    return result

def checkCombinations(line, secondPart=False):
    result, values = int(line[0]), line[1].split()
    
    # Determine possible operators based on part of the puzzle
    operator_options = ['+', '*']
    if secondPart:
        operator_options.append('||')
    
    # Determine number of operators needed
    num_operators = len(values) - 1
    
    # If there's only one number, skip operator combinations
    if num_operators == 0:
        return result if int(values[0]) == result else 0

    # Generate all possible operator combinations
    for operators in itertools.product(operator_options, repeat=num_operators):
        # Early exit if the result is found
        if evaluate(values, operators) == result:
            return result
    
    # No valid combination found
    return 0

def process_lines(lines, secondPart=False):
    return [checkCombinations(line, secondPart) for line in lines]

if __name__ == '__main__':
    start = time.time()
    
    # Read input data
    with open("../input.txt", 'r') as f:
        file = f.read()
    lines = [i.split(": ") for i in file.split("\n")]

    # Split lines into chunks for parallel processing
    num_processes = mp.cpu_count() # Adjust based on your machine's core count
    chunk_size = len(lines) // num_processes
    chunks = [lines[i:i + chunk_size] for i in range(0, len(lines), chunk_size)]
    
    # Create a pool of workers and process each chunk in parallel
    with Pool(processes=num_processes) as pool:
        # Solve Part One
        partOne_results = pool.starmap(process_lines, [(chunk, False) for chunk in chunks])
        partOne = sum(sum(result) for result in partOne_results)
        
        # Solve Part Two
        partTwo_results = pool.starmap(process_lines, [(chunk, True) for chunk in chunks])
        partTwo = sum(sum(result) for result in partTwo_results)
    
    # Print results
    print("#"*50 + f"\nAdvent of Code 2024\n\t- Day 07\n\t\t★  Result: {partOne}\n\t\t★★ Result: {partTwo}\n" + "#"*50)
    print(f"Execution Time {time.time()-start} seconds")
