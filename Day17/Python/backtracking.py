def reconstruct_A(target_out):
    def backtrack(ip=-1, A=0, B=0, C=0):
        # Check if we've successfully reconstructed the entire output
        if abs(ip) > len(target_out):
            return A
        
        # Try all possible values for the current digit and previous states
        for a in range(8**6):  # Explore a broader range of A values
            curr_A = a
            curr_B = B
            curr_C = C
            
            # Temporary list to track outputs
            test_out = []
            matched = True
            temp_A = curr_A
            temp_B = curr_B
            
            # Simulate forward for the current sequence length
            for curr_ip in range(len(target_out)):
                # BST(4) & BXL(5)
                temp_B = (temp_A % 8) ^ 5
                
                # CDV(5)
                temp_C = temp_A // (2 ** temp_B)
                
                # ADV(3)
                temp_A = temp_A // 8
                
                # BXL(6)
                temp_B = temp_B ^ 6
                
                # BXC(3)
                temp_B = temp_B ^ temp_C
                
                # OUT(5)
                curr_out = temp_B % 8
                test_out.append(curr_out)
                
                # Check if current output matches target
                if curr_out != int(target_out[-(curr_ip+1)]):
                    matched = False
                    break
            
            # If we found a match and reached the correct length
            if matched and len(test_out) == len(target_out):
                return curr_A
        
        # No solution found
        return None

    # Find the initial A
    result = backtrack()
    return result

# Target output from the original problem
target_out = [2,4,1,5,7,5,0,3,1,6,4,3,5,5,3,0]

# Find the initial A
initial_A = reconstruct_A(target_out)
print(f"Reconstructed Initial A: {initial_A}")

# Verification function
def verify_solution(A):
    B = 0
    counter = 0
    OUT = []
    orig_A = A
    while A != 0 or counter == 0:
        # BST(4) & BXL(5)
        B = (A % 8) ^ 5
        # CDV(5)
        C = A // (2 ** B)
        # ADV(3)
        A = A // 8
        # BXL(6)
        B = B ^ 6
        # BXC(3)
        B = B ^ C
        # OUT(5)
        OUT.append(str(B%8))
        # JNZ(3)
        counter += 1
        if counter > 20:  # Prevent infinite loop
            break
    
    print("Reconstructed output:", OUT)
    print("Matches target output:", OUT == [str(x) for x in target_out])
    print("Original A used:", orig_A)

if initial_A is not None:
    verify_solution(initial_A)
else:
    print("No solution found")