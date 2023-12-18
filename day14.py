import numpy as np

with open('data/day14_input_s', 'r') as file:
    input = file.read()

map = np.array([list(l) for l in input.splitlines()])

def find_landing_north(row, column):
    # tilted to the north, where will the rock land, returns the row
    next = row - 1
    while next >= 0:
        if map[next][column] == ".":
            next -= 1
        else:
            return next + 1
    return 0

def tilt_to_north():
    mask = map == "O"
    rows, col = np.where(mask)
    for r, c in zip(rows, col):
        landing_row = find_landing_north(r, c)
        if landing_row != r:
            map[landing_row][c] = "O"
            map[r][c] = "."

def calculate_load(map):
    sum = 0
    for i in range(len(map)):
        weight = len(map) - i
        for ele in map[i]:
            if ele == "O":
                sum += weight
    return sum

#tilt_to_north()
#print(f"load: {calculate_load(map)}")


# --------------- part 2 --------------------------------

def find_landing_south(row, column, rows_cnt):
    # tilted to the south, where will the rock land, returns the row
    next = row + 1
    while next < rows_cnt:
        if map[next][column] == ".":
            next += 1
        else:
            return next - 1
    return rows_cnt - 1

def tilt_to_south():
    mask = map == "O"
    rows, col = np.where(mask)
    for r, c in sorted(zip(rows, col), key=lambda x: x[0], reverse=True):
        landing_row = find_landing_south(r, c, len(map))
        if landing_row != r:
            map[landing_row][c] = "O"
            map[r][c] = "."

def find_landing_east(row, column, col_cnt):
    # tilted to the east, where will the rock land, returns the column
    next = column + 1
    while next < col_cnt:
        if map[row][next] == ".":
            next += 1
        else:
            return next - 1
    return col_cnt - 1

def tilt_to_east():
    mask = map == "O"
    rows, col = np.where(mask)
    for r, c in sorted(zip(rows, col), key=lambda x: x[1], reverse=True):
        landing_column = find_landing_east(r, c, len(map[0]))
        if landing_column != c:
            map[r][landing_column] = "O"
            map[r][c] = "."

def find_landing_west(row, column):
    # tilted to the west, where will the rock land, returns the column
    next = column - 1
    while next >= 0:
        if map[row][next] == ".":
            next -= 1
        else:
            return next + 1
    return 0

def tilt_to_west():
    mask = map == "O"
    rows, col = np.where(mask)
    for r, c in sorted(zip(rows, col), key=lambda x: x[1]):
        landing_column = find_landing_west(r, c)
        if landing_column != c:
            map[r][landing_column] = "O"
            map[r][c] = "."

def do_a_cycle():
    tilt_to_north()
    tilt_to_west()
    tilt_to_south()
    tilt_to_east()
def do_cycles(count):
    for i in range(count):
        if i % 10000000 == 0:
            print(i%1000000)
        do_a_cycle()

do_cycles(1000000000)
print(f"total load: {calculate_load(map)}")
for l in map:
    print(l)