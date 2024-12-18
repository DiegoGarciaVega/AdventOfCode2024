import time
start = time.time()

# Reading program and registers
file = open("../test2.txt", 'r').read()

registers, program =  file.split("\n\n")

initA, initB, initC = [int(i.split(":")[1]) for i in registers.split("\n")]

program = list(map(int,program.split(":")[1].split(",")))

# Global variables
PROGRAM_LIMIT = len(program)
INSTRUCTION_POINTER = 0
FLAG_INCREASE_POINTER = True
OUTPUT = []

# Class register
class Register:
    value = None
    def __init__(self, init):
        self.value = init

    def getRegister(self):
        return self.value
    
    def setRegister(self, new):
        self.value = new

# Initializing registers
A = Register(initA)
B = Register(initB)
C = Register(initC)

# Dictionary of combo operands
COMBO = {
            0: lambda: 0,
            1: lambda: 1,
            2: lambda: 2,
            3: lambda: 3, 
            4: lambda: A.getRegister(),
            5: lambda: B.getRegister(),
            6: lambda: C.getRegister(),
            7: lambda: None
        }

# Initializing possible operations
def adv(operand: int):
    A.setRegister(A.getRegister() // (2 ** COMBO[operand]()))
    print(f"Executing ADV\t Changed Register A to {A.getRegister()}")

def bxl(operand: int):
    B.setRegister(B.getRegister() ^ operand)
    print(f"Executing BXL\t Changed Register B to {B.getRegister()}")

def bst(operand: int):
    B.setRegister(COMBO[operand]() % 8)
    print(f"Executing BST\t Changed Register B to {B.getRegister()}")

def jnz(operand: int):
    global INSTRUCTION_POINTER, FLAG_INCREASE_POINTER
    if A.getRegister():
        INSTRUCTION_POINTER = operand
        FLAG_INCREASE_POINTER = False
    print(f"Executing JNZ\t Changed POINTER {INSTRUCTION_POINTER}\t FLAG {FLAG_INCREASE_POINTER}")

def bxc(operand: int):
    B.setRegister(B.getRegister() ^ C.getRegister())
    print(f"Executing BXL\t Changed Register B to {B.getRegister()}")
    
def out(operand: int):
    OUTPUT.append(str(COMBO[operand]() % 8))
    print(f"Executing OUT\t Current OUTPUT {OUTPUT}")

def bdv(operand: int):
    B.setRegister(A.getRegister() // (2 ** COMBO[operand]()))
    print(f"Executing BDV\t Changed Register B to {B.getRegister()}")

def cdv(operand: int):
    C.setRegister(A.getRegister() // (2 ** COMBO[operand]()))
    print(f"Executing CDV\t Changed Register C to {C.getRegister()}")
    
# Dictionary of literal operands
OPCODE = {
            0: adv,
            1: bxl,
            2: bst,
            3: jnz, 
            4: bxc,
            5: out,
            6: bdv,
            7: cdv
        }

print(f"Register A: {A.getRegister()}")
print(f"Register B: {B.getRegister()}")
print(f"Register C: {C.getRegister()}")
print()
print(f"Program {program}")
print()
print("INSTRUCTION\t OPERATION")

while True:
    try:
        code = program[INSTRUCTION_POINTER]
        operand = program[INSTRUCTION_POINTER + 1]

        
        OPCODE[code](operand)
        
        if FLAG_INCREASE_POINTER:
            INSTRUCTION_POINTER += 2
        else:
            FLAG_INCREASE_POINTER = True
            
    except Exception as error:
        print("🛑 Halting execution❗")
        break

print("OUTPUT")
print(",".join(OUTPUT))


print("#"*50 + f"\nAdvent of Code 2024\n\t- Day 17\n\t\t★  Result: {0}\n\t\t★★ Result: {0}\n" + "#"*50)
print(f"Execution Time {time.time() - start} seconds")