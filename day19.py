import copy
with open('data/day19_input', 'r') as file:
    input = file.read().split("\n\n")

def get_parts(parts_raw): # list of each part as dictionaries
    parts = []
    for r in parts_raw.splitlines():
        current_part = {}
        for attr in r[1:len(r) - 1].split(","):
           current_part[attr.split("=")[0]] = int(attr.split("=")[1])
        parts.append(current_part)
    return parts

def get_workflows(workflows_raw): # dictionary with names as keys, value is list of rules
    '''
    rule = {"attr": "attribute", "cond": lambda, "dest": "destination workflow"}
    '''
    def get_attr_cond(str):
        if ">" in str:
            return str.split(">")[0], lambda a: a > int(str.split(">")[1])
        else:
            return str.split("<")[0], lambda a: a < int(str.split("<")[1])

    def get_valid_range(str): # both inclusive
        if ">" in str:
            return [int(str.split(">")[1]) + 1, 4000]
        else:
            return [1, int(str.split("<")[1]) - 1]

    workflows = {}
    for w in workflows_raw.splitlines():
        name = w.split("{")[0]
        workflows[name] = []
        for r in w.split("{")[1][0: -1].split(","):
            rule = {}
            if len(r.split(":")) == 2:
                attr, cond = get_attr_cond(r.split(":")[0])
                rule["attr"] = attr
                rule["cond"] = cond
                rule["dest"] = r.split(":")[1]
                rule["range"] = get_valid_range(r.split(":")[0])
            else: # last rule
                rule["attr"] = ""
                rule["cond"] = lambda *args, **kwargs: True
                rule["dest"] = r
                rule["range"] = []
            workflows[name].append(rule)
            # print(rule)

    return workflows


workflows = get_workflows(input[0])
parts = get_parts(input[1])

def trace_part(part, workflows):
    cur_trace = []
    current_pos = "in"
    while current_pos != "A" and current_pos != "R":
        cur_trace.append(current_pos)
        for rule in workflows[current_pos]:
            if rule["attr"] == "" or rule["cond"](part[rule["attr"]]):  # condition is fulfilled
                current_pos = rule["dest"]
                break
    cur_trace.append(current_pos)
    return cur_trace

def trace_parts(parts, workflows):
    traces = []
    for part in parts:
        traces.append(trace_part(part, workflows))
    return traces

def calculate_sum(parts, traces):
    sum = 0
    for i in range(len(parts)):
        if traces[i][-1] == "A":
            for attr in parts[i]:
                sum += parts[i][attr]
    return sum

print(f"sum: {calculate_sum(parts, trace_parts(parts, workflows))}")

# --------------------- part 2 ------------------------------

def apply_rule(rule, range):
    attribute = rule["attr"]
    if rule["attr"] == "":
        return rule["dest"], range, {}

    attr_range = range[attribute]
    if range[attribute][1] < range[attribute][0] or rule["range"][0] > attr_range[1] \
            or rule["range"][1] < attr_range[0]:  # no overlap
        return "", {}, range

    dest_range = copy.deepcopy(range)
    if rule["range"][0] != 1 and rule["range"][0] >= attr_range[0]:  # right half of the range fulfills the rule
        #print(f"{attribute}: right half of {rule['range'][0]} is relevant, setting remaining end to be "
        #      f"{rule['range'][0] - 1} and destination_range start to be {rule['range'][0]}")
        range[attribute][1] = rule["range"][0] - 1
        dest_range[attribute][0] = rule["range"][0]
    else:  # left half
        #print(f"{attribute}: left half of {rule['range'][1]} is relevant")
        range[attribute][0] = rule["range"][1] + 1
        dest_range[attribute][1] = rule["range"][1]
    return rule["dest"], dest_range, range

def process(current_pos, positions, workflows): # where will the parts go after one iteration of this workflow
    if current_pos == "A" or current_pos == "R":
        return positions

    for range in positions[current_pos]:
        for rule in workflows[current_pos]:
            dest, dest_range, remaining = apply_rule(rule, range)
            if len(dest_range) > 0:
                invalid_range = False
                for k in dest_range:
                    if dest_range[k][0] > dest_range[k][1]:
                        invalid_range = True
                if not invalid_range:
                    print(f"appending to {dest}: {dest_range}")
                    positions[dest].append(dest_range)
            range = remaining
    positions[current_pos] = []  # remove all parts in this workflow

    return positions

def trace_part_range(positions, workflows):
    '''
    :param positions: dictionary with workflow names as keys, value is list of ranges
    '''
    counter = 0
    while counter < 100:
        for wf in positions:
            #print(f"\nProcessing '{wf}': {positions[wf]}
            positions = process(wf, positions, workflows)
        counter += 1
    return positions

positions = {"in": [{"x": [1, 4000], "m": [1, 4000], "a": [1, 4000], "s": [1, 4000]}]}
for w in workflows:
    if w != "in":
        positions[w] = []
positions["A"] = []
positions["R"] = []

processed = trace_part_range(positions, workflows)
print(processed)
print(f"A: {processed['A']}")
print(f"R: {processed['R']}")

def count_unique_parts(processed_parts):
    cnt = 0
    for r in processed_parts:
        cnt += (r["x"][1] - r["x"][0] + 1) * (r["m"][1] - r["m"][0] + 1) * (r["a"][1] - r["a"][0] + 1) * (r["s"][1] - r["s"][0] + 1)
    return cnt

print(count_unique_parts(processed["A"]))