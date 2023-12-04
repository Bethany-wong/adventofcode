with open('data/day3_input', 'r') as file:
    input = file.read()
input_lines = input.splitlines()
input_matrix = []
for line in input_lines:
    input_matrix.append(list(line))

n = len(input_matrix)
m = len(input_matrix[0])

influence = [[False for _ in range(m)] for _ in range(n)]

def influence_cell(i, j):
    if i >= 0 and j >= 0 and i < n and j < m:
        influence[i][j] = True

def flow(i, j): # input should be valid
    # print(f"flowing from {i}, {j}: {input_matrix[i][j]}")
    for plus_i in range(-1, 2):
        for plus_j in range(-1, 2):
            influence_cell(i + plus_i, j + plus_j)


for i in range(n): # row
    for j in range(m): # column
        if not input_matrix[i][j].isnumeric() and input_matrix[i][j] != ".":
            # this is a symbol, mark adjacent cells as influenced
            flow(i, j)

sum = 0
for i in range(n):
    current_number = ""
    is_part_number = False

    for j in range(m):
        if input_matrix[i][j].isnumeric():
            is_part_number = is_part_number or influence[i][j]
            current_number += input_matrix[i][j]
            if j == m - 1 and is_part_number: # end of line, save the number
                sum += int(current_number)
        else:
            if current_number != "":
                if is_part_number:
                    sum += int(current_number)
                    is_part_number = False
                current_number = ""

print(sum)


# ------------------------------ part 2 ------------------------------------------

def in_range(i, j):
    return i >= 0 and j >= 0 and i < n and j < m

def find_number(i, j):
    j_start = j
    while j_start >= 0 and input_matrix[i][j_start].isnumeric():
        j_start = j_start - 1
    j_start = j_start + 1
    num = ""
    while j_start < m and input_matrix[i][j_start].isnumeric():
        num += input_matrix[i][j_start]
        j_start += 1
    return int(num)

total = 0
for i in range(n): # row
    for j in range(m): # column
        cnt = 0
        positions = []
        if input_matrix[i][j] != "*":
            continue
        for plus in [-1, 1]:
            # up and down
            if input_matrix[i+plus][j].isnumeric(): # number in the middle -> at most one number
                positions.append([i+plus, j])
                cnt += 1
            else:
                if in_range(i+plus, j - 1) and input_matrix[i+plus][j-1].isnumeric():
                    positions.append([i+plus, j - 1])
                    cnt += 1
                if in_range(i+plus, j + 1) and input_matrix[i+plus][j + 1].isnumeric():
                    positions.append([i+plus, j + 1])
                    cnt += 1
            # left and right
            if in_range(i, j+plus) and input_matrix[i][j+plus].isnumeric():
                positions.append([i, j+plus])
                cnt += 1

        if cnt == 2:
            total += find_number(positions[0][0], positions[0][1]) * find_number(positions[1][0], positions[1][1])

print(total)