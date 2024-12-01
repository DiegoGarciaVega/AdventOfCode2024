f = open("../input.txt",'r')
file = f.read()

"""
Auxiliary Functions to search for:
    - Horizontal     -> H
    - Vertical       -> V
    - Right Diagonal -> RD
    - Left Diagonal  -> LD
"""
def find_word_in_matrix(matrix, word, row, column, row_step, col_step):
    try:
        for ch in word:
            if matrix[row][column] != ch or column < 0 or row < 0:
                return False
            row += row_step
            column += col_step
        return True
    except IndexError:
        return False
    
search_directions = {
    "H":  lambda matrix, word, row, col: find_word_in_matrix(matrix, word, row, col, 0, 1),
    "V":  lambda matrix, word, row, col: find_word_in_matrix(matrix, word, row, col, 1, 0),
    "RD": lambda matrix, word, row, col: find_word_in_matrix(matrix, word, row, col, 1, 1),
    "LD": lambda matrix, word, row, col: find_word_in_matrix(matrix, word, row, col, 1, -1),
}
cont, cont2 = 0, 0

word = "XMAS"
drow = word[::-1]

word2 = "MAS"
drow2 = word2[::-1]

matrix = [[j for j in i] for i in file.split("\n")]
rows, columns = len(matrix), len(matrix[0])

# Search for words
for i in range(rows):
    for j in range(columns):
        # First Part: Search for "XMAS" and its reverse in all directions
        for direction in search_directions.values():
            cont += direction(matrix, word, i, j)
            cont += direction(matrix, drow, i, j)

        # Second Part: Special condition involving "MAS" and its reverse
        if (search_directions["RD"](matrix, word2, i, j) and search_directions["LD"](matrix, word2, i, j + 2)):
            cont2 += 1
        if (search_directions["RD"](matrix, word2, i, j) and search_directions["LD"](matrix, drow2, i, j + 2)):
            cont2 += 1
        if (search_directions["RD"](matrix, drow2, i, j) and search_directions["LD"](matrix, word2, i, j + 2)):
            cont2 += 1
        if (search_directions["RD"](matrix, drow2, i, j) and search_directions["LD"](matrix, drow2, i, j + 2)):
            cont2 += 1

print("#"*50 + f"\nAdvent of Code 2024\n\t- Day 04\n\t\t★  Result: {cont}\n\t\t★★ Result: {cont2}\n" + "#"*50)   