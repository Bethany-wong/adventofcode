loaded = {"red": 12, "green": 13, "blue": 14}
with open('data/day2_input', 'r') as file:
    input = file.read()
input_lines = input.splitlines()

def extract_set(set_list):
    output = {}
    for item in set_list:
        for ele in item.split(" "):
            if ele.isnumeric():
                num = int(ele)
            elif ele != " ":
                color = ele
        output[color] = num
    return output

def find_sets(line): # return sets in a game as list of dictionaries
    sets = []
    for set_str in line.split(";"):
        sets.append(extract_set(set_str.split(",")))
    return sets

def check_feasibility(sets):
    for s in sets:
        for color in s:
            if s[color] > loaded[color]:
                return False
    return True

total = 0
for i in range(len(input_lines)):
    if check_feasibility(find_sets(input_lines[i].split(":")[1])):
        total += i + 1  # 0th row is game 1
print(total)

# ------------------ part 2 ------------------------
def find_fewest_possible_cubes(sets):
    lowest_possible = {"red": 0, "green": 0, "blue": 0}
    for s in sets:
        for color in s:
            if s[color] > lowest_possible[color]:
                lowest_possible[color] = s[color]
    return lowest_possible

def compute_power(lowest_possible):
    output = 1
    for color in lowest_possible:
        output *= lowest_possible[color]
    return output

power_sum = 0
for i in range(len(input_lines)):
    sets = find_sets(input_lines[i].split(":")[1])
    power_sum += compute_power(find_fewest_possible_cubes(sets))

print(power_sum)