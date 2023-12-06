with open('data/day6_input', 'r') as file:
    input = file.read()

times = [t for t in input.splitlines()[0].split(":")[1].split(" ") if t.isnumeric()]
records = [r for r in input.splitlines()[1].split(":")[1].split(" ") if r.isnumeric()]

def count_winnings(time, record_dist): # naive way
    cnt = 0
    for i in range(time + 1): # press the button for i seconds
        if (time - i)*i > record_dist:
            cnt += 1
    return cnt

product = 1
for race_num in range(len(times)):
    product *= count_winnings(int(times[race_num]), int(records[race_num]))
print(f"result: {product}")

# ----------------------- part 2 -------------------------------------
def find_first_record_beater(time, record_dist):
    for i in range(time + 1):
        if (time - i)*i > record_dist:
            return i
    return -1

time = "".join(times)
record = "".join(records)
start = find_first_record_beater(int(time), int(record))
end = int(time) - start
print(f"part 2: {end - start + 1}")