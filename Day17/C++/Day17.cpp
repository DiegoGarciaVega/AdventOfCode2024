#include <iostream>
#include <fstream>
#include <vector>
#include <string>
#include <functional>
#include <map>
#include <cmath>
#include <sstream>
#include <stdexcept>
#include <cctype>

using namespace std;

// Class to represent a register
class Register {
public:
    int value;
    Register(int init) : value(init) {}

    int getRegister() const {
        return value;
    }

    void setRegister(int newValue) {
        value = newValue;
    }
};

// Global variables
int PROGRAM_LIMIT;
int INSTRUCTION_POINTER = 0;
bool FLAG_INCREASE_POINTER = true;
vector<int> program;
vector<string> OUTPUT;

Register A(0), B(0), C(0);

// Combo operands
map<int, function<int()>> COMBO = {
    {0, [](){ return 0; }},
    {1, [](){ return 1; }},
    {2, [](){ return 2; }},
    {3, [](){ return 3; }},
    {4, [](){ return A.getRegister(); }},
    {5, [](){ return B.getRegister(); }},
    {6, [](){ return C.getRegister(); }},
    {7, [](){ return 0; }} // None equivalent
};

// Operations
void adv(int operand) {
    A.setRegister(A.getRegister() / (int)pow(2, COMBO[operand]()));
    cout << "Executing ADV\t Changed Register A to " << A.getRegister() << endl;
}

void bxl(int operand) {
    B.setRegister(B.getRegister() ^ operand);
    cout << "Executing BXL\t Changed Register B to " << B.getRegister() << endl;
}

void bst(int operand) {
    B.setRegister(COMBO[operand]() % 8);
    cout << "Executing BST\t Changed Register B to " << B.getRegister() << endl;
}

void jnz(int operand) {
    if (A.getRegister()) {
        INSTRUCTION_POINTER = operand;
        FLAG_INCREASE_POINTER = false;
    }
    cout << "Executing JNZ\t Changed POINTER " << INSTRUCTION_POINTER << "\t FLAG " << FLAG_INCREASE_POINTER << endl;
}

void bxc(int operand) {
    B.setRegister(B.getRegister() ^ C.getRegister());
    cout << "Executing BXL\t Changed Register B to " << B.getRegister() << endl;
}

void out(int operand) {
    OUTPUT.push_back(to_string(COMBO[operand]() % 8));
    cout << "Executing OUT\t Current OUTPUT " << OUTPUT.back() << endl;
}

void bdv(int operand) {
    B.setRegister(A.getRegister() / (int)pow(2, COMBO[operand]()));
    cout << "Executing BDV\t Changed Register B to " << B.getRegister() << endl;
}

void cdv(int operand) {
    C.setRegister(A.getRegister() / (int)pow(2, COMBO[operand]()));
    cout << "Executing CDV\t Changed Register C to " << C.getRegister() << endl;
}

// Operation code map
map<int, function<void(int)>> OPCODE = {
    {0, adv},
    {1, bxl},
    {2, bst},
    {3, jnz},
    {4, bxc},
    {5, out},
    {6, bdv},
    {7, cdv}
};

// Utility function to safely convert strings to integers
int safe_stoi(const string& str) {
    string clean_str;
    
    // Remove any non-numeric characters from the string
    for (char ch : str) {
        if (isdigit(ch) || ch == '-') {
            clean_str += ch;
        }
    }

    // Check if the cleaned string is empty or contains invalid characters
    if (clean_str.empty()) {
        cerr << "Error: Invalid integer format for string: " << str << endl;
        throw invalid_argument("Invalid integer format.");
    }

    try {
        return stoi(clean_str);  // Convert cleaned string to integer
    } catch (const invalid_argument& e) {
        cerr << "Invalid integer: " << str << endl;
        throw;
    } catch (const out_of_range& e) {
        cerr << "Integer out of range: " << str << endl;
        throw;
    }
}

int main() {
    // Start time
    clock_t start = clock();

    // Read file
    ifstream file("../test2.txt");
    if (!file.is_open()) {
        cerr << "Error opening file" << endl;
        return 1;
    }

    string content((istreambuf_iterator<char>(file)), istreambuf_iterator<char>());
    
    // Split registers and program
    size_t splitIndex = content.find("\n\n");
    if (splitIndex == string::npos) {
        cerr << "Invalid file format: Could not split registers and program" << endl;
        return 1;
    }
    
    string registers = content.substr(0, splitIndex);
    string programString = content.substr(splitIndex + 2);
    
    // Initialize registers
    stringstream registersStream(registers);
    string line;
    while (getline(registersStream, line)) {
        if (line.find("A:") != string::npos) {
            try {
                A = Register(safe_stoi(line.substr(2)));
            } catch (...) {
                cerr << "Error while parsing register A: " << line << endl;
                return 1;
            }
        }
        if (line.find("B:") != string::npos) {
            try {
                B = Register(safe_stoi(line.substr(2)));
            } catch (...) {
                cerr << "Error while parsing register B: " << line << endl;
                return 1;
            }
        }
        if (line.find("C:") != string::npos) {
            try {
                C = Register(safe_stoi(line.substr(2)));
            } catch (...) {
                cerr << "Error while parsing register C: " << line << endl;
                return 1;
            }
        }
    }

    // Initialize program
    stringstream programStream(programString);
    string programLine;
    while (getline(programStream, programLine, ',')) {
        try {
            program.push_back(safe_stoi(programLine.substr(programLine.find(":") + 1)));
        } catch (...) {
            cerr << "Error while parsing program: " << programLine << endl;
            return 1;
        }
    }

    PROGRAM_LIMIT = program.size();

    // Print initial values
    cout << "Register A: " << A.getRegister() << endl;
    cout << "Register B: " << B.getRegister() << endl;
    cout << "Register C: " << C.getRegister() << endl;
    cout << endl << "Program: ";
    for (const int& p : program) {
        cout << p << " ";
    }
    cout << endl << "INSTRUCTION\t OPERATION" << endl;

    // Execution loop
    while (true) {
        try {
            int code = program[INSTRUCTION_POINTER];
            int operand = program[INSTRUCTION_POINTER + 1];

            OPCODE[code](operand);

            if (FLAG_INCREASE_POINTER) {
                INSTRUCTION_POINTER += 2;
            } else {
                FLAG_INCREASE_POINTER = true;
            }
        } catch (...) {
            cout << "🛑 Halting execution❗" << endl;
            break;
        }
    }

    // Output
    cout << "OUTPUT" << endl;
    for (const string& out : OUTPUT) {
        cout << out << ",";
    }
    cout << endl;

    // Execution time
    cout << string(50, '#') << endl;
    cout << "Advent of Code 2024\n\t- Day 17\n\t\t★ Result: 0\n\t\t★★ Result: 0\n";
    cout << string(50, '#') << endl;
    cout << "Execution Time " << (float)(clock() - start) / CLOCKS_PER_SEC << " seconds" << endl;

    return 0;
}
