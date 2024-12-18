A = 105875099912602
B = 0
counter = 0 
OUT =[]

while A!=0 or counter == 0:
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
    counter +=1
print(",".join(OUT))

# A = 59590048
# B = 0
# C = 0
# PROGRAM: 2,4,1,5,7,5,0,3,1,6,4,3,5,5,3,0
#   OPCODE   OPERAND   INSTRUCTION
#   2             4     BST(4)
#   1             5     BXL(5)
#   7             5     CDV(5)
#   0             3     ADV(3)
#   1             6     BXL(6)
#   4             3     BXC(3)
#   5             5     OUT(5)
#   3             0     JNZ(0)

# OUT= 6,5,7,4,5,7,3,1,0

