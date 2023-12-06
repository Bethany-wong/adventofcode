categories = ["seed", "soil", "fertilizer", "water", "light", "temperature", "humidity", "location"]

with open('data/day5_input', 'r') as file:
    input = file.read()

paragraphs = input.split("\n\n")
entries = {}
for para in paragraphs:
    entries[para.split(":")[0]] = para.split(":")[1]

seeds = [int(s) for s in entries["seeds"].split(" ") if s.isnumeric()]

def create_ranges(source, destination, ranges):
    ranges_dict = {}
    ranges_dict["source"] = source
    ranges_dict["destination"] = destination
    ranges_dict["intervals"] = []
    for line in ranges.splitlines():
        if len(line) == 0:
            continue
        nums = [n for n in line.split(" ") if n.isnumeric()]
        tmp = {}
        tmp["destination_start"] = int(nums[0])
        tmp["source_start"] = int(nums[1])
        tmp["range_len"] = int(nums[2])
        ranges_dict["intervals"].append(tmp)
    return ranges_dict

def map_to_destination(source, map):
    for range in map:
        if source >= range["source_start"] and source < range["source_start"] + range["range_len"]:
            return source -  range["source_start"] + range["destination_start"]
    return source

maps = {}
for i in range(len(categories) - 1):
    entry_key = f"{categories[i]}-to-{categories[i+1]} map"
    maps[f"{categories[i]}-to-{categories[i+1]}"] = create_ranges(categories[i], categories[i + 1], entries[entry_key])

seed_to_location = []
for seed in seeds:
    converted_val = {}
    converted_val["seed"] = seed
    for i in range(len(categories) - 1):
        converted_val[categories[i + 1]] = map_to_destination(converted_val[categories[i]],
                                                              maps[f"{categories[i]}-to-{categories[i + 1]}"]["intervals"])
    seed_to_location.append((seed, converted_val["location"]))

def find_min_location(seed_to_location):
    min_location = seed_to_location[0][1]
    for s in seed_to_location:
        if s[1] < min_location:
            min_location = s[1]
    return min_location

print(f"lowest location number: {find_min_location(seed_to_location)}")

# ---------------------------------- part 2 ----------------------------------------
def map_to_source(destination, map):
    for range in map:
        if destination >= range["destination_start"] and destination < range["destination_start"] + range["range_len"]:
            return destination + range["source_start"] - range["destination_start"]
    return destination


def is_initial_seed(seed):
    for i in range(int(len(seeds) / 2)):
        if seed >= seeds[i * 2] and seed < seeds[i * 2] + seeds[i * 2 + 1]:
            return True
    return False


# backtrack
for i in range(20358600):
    if i % 100000 == 0:
        print(i)
    converted_val = {}
    converted_val["location"] = i
    for j in range(len(categories) - 1, 0, -1):
        converted_val[categories[j - 1]] = map_to_source(converted_val[categories[j]],
                                                              maps[f"{categories[j - 1]}-to-{categories[j]}"][
                                                                  "intervals"])
    if is_initial_seed(converted_val["seed"]):
        print(f"found: {i}")
        break