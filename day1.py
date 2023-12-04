with open('data/day1_input', 'r') as file:
    input = file.read()

def find_digits(line):
    first = -1
    last = -1
    for i in range(len(line)):
        if line[i].isnumeric():
            if first == -1:
                first = i
            last = i
    return first, last, int(line[first]), int(line[last])

'''
sum = 0
for line in input.splitlines():
    first, last, first_num, last_num = find_digits(line)
    sum += first_num*10 + last_num

print("sum: " + str(sum))
'''

# -------------------------- part 2 -----------------------------

def find_digits_str(line):
    digits = ["zero", "one", "two", "three", "four", "five", "six", "seven", "eight", "nine"]
    first = -1
    last = -1
    first_num = 0
    last_num = 0
    for i in range(len(digits)):
        start = 0 # find all occurences of a digit
        while start < len(line):
            if line.find(digits[i], start) >= 0:
                if first == -1:
                    first = line.find(digits[i], start)
                    last = first
                    first_num = i
                    last_num = i
                else:
                    if line.find(digits[i], start) < first:
                        first = line.find(digits[i], start)
                        first_num = i
                    elif line.find(digits[i], start) > last:
                        last = line.find(digits[i], start)
                        last_num = i
                start += len(digits[i])
            else:
                break
    return first, last, first_num, last_num

total = 0
for line in input.splitlines():
    first, last, first_num, last_num = find_digits_str(line)
    if first == -1:
        first, last, first_num, last_num = find_digits(line)
    else:
        first_int, last_int, first_num_int, last_num_int = find_digits(line)
        if first_int != -1 and first_int < first:
            first_num = first_num_int
        if last_int > last:
            last_num = last_num_int
    print(first_num * 10 + last_num)
    total += first_num * 10 + last_num

print("total: " + str(total))