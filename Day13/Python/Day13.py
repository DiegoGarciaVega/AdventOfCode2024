import time
import numpy as np

start = time.time()
# Read input data
f = open("../input.txt", 'r').read().split("\n\n")
COST_A = 3
COST_B = 1

def is_valid_solution(a_val, b_val, tolerance=1e-3,partTwo=False):
    # Check if values are close to integers within a small tolerance
    is_integer_a = abs(a_val - round(a_val)) < tolerance
    is_integer_b = abs(b_val - round(b_val)) < tolerance    
    if partTwo:
        return is_integer_a and is_integer_b

    else:
        # Check range with tolerance
        in_range_a = -tolerance <= a_val <= 100 + tolerance
        in_range_b = -tolerance <= b_val <= 100 + tolerance
        return is_integer_a and is_integer_b and in_range_a and in_range_b

partOne, partTwo = 0,0
valid_solutions = []
for line in f:
    aux = line.split("\n")
    for i in range(len(aux)):
        # print(aux[i])
        if i == 0:
            # A Button parameters
            parsed = [j.split("+") for j in aux[i].split(",")]
            XA = int(parsed[0][1])
            YA = int(parsed[1][1])
        elif i == 1: 
            # B Button parameters
            parsed = [j.split("+") for j in aux[i].split(",")]
            XB = int(parsed[0][1])
            YB = int(parsed[1][1])
        else:
            # Prize parameters
            parsed = [j.split("=") for j in aux[i].split(",")]
            XP = int(parsed[0][1])
            YP = int(parsed[1][1])

            # Create coefficient matrix and constants vector
            A_matrix = np.array([[XA, XB], [YA, YB]])
            b_vector = np.array([XP, YP])
            b2_vector = np.array([XP+10000000000000,YP+10000000000000])
            # Solve the system using least squares
            try:
                # lstsq returns (solution, residuals, rank, singular values)
                solution, residuals, rank, singular_values = np.linalg.lstsq(A_matrix, b_vector, rcond=None)
                
                # Extract A and B values
                a_val, b_val = solution

                if is_valid_solution(a_val, b_val):
                    # Round to handle floating point imprecision
                    a_val = round(a_val, 10)
                    b_val = round(b_val, 10)
                
                    partOne += a_val*COST_A + b_val *COST_B
                
                solution, residuals, rank, singular_values = np.linalg.lstsq(A_matrix, b2_vector, rcond=None)
                a2_val, b2_val = solution
                if is_valid_solution(a2_val, b2_val,partTwo=True):
                
                    # Round to handle floating point imprecision
                    a2_val = round(a2_val, 10)
                    b2_val = round(b2_val, 10)
                    partTwo += a2_val*COST_A + b2_val *COST_B
            
                
            except Exception as e:
                print(f"Error solving system: {e}")

print("#"*50 + f"\nAdvent of Code 2024\n\t- Day 10\n\t\t★  Result: {int(partOne)}\n\t\t★★ Result: {int(partTwo)}\n" + "#"*50)
print(f"Execution Time {time.time()-start} seconds")