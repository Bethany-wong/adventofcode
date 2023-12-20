from collections import deque
with open('data/day20_input', 'r') as file:
    input = file.read()
def initialize(modules):
    for name in modules:
        if modules[name]["type"] == "%":
            modules[name]["flip"] = False
        elif modules[name]["type"] == "&":
            modules[name]["flip"] = {}
            for other_module in modules:
                if name in modules[other_module]["dest"]:
                    modules[name]["flip"][other_module] = False

modules = {}
for line in input.splitlines():
    type_and_name = line.split(" -> ")[0]
    module_name = type_and_name if type_and_name == "broadcaster" else type_and_name[1:]
    modules[module_name] = {"type": type_and_name[0], "dest": line.split(" -> ")[1].split(", ")}

initialize(modules)
for m in modules:
    print(m, modules[m])

def push_button(modules, push_count=0, init_pulse=False): # sends low pulse to broadcaster
    cnt = {False: 0, True: 0}
    cnt[init_pulse] += 1
    queue = deque()
    for destination in modules["broadcaster"]["dest"]:
        queue.append(("broadcaster", destination, init_pulse))
        cnt[init_pulse] += 1

    while len(queue) > 0:
        sender, destination, pulse = queue.popleft()
        #print(f"{sender} - {pulse} -> {destination}")
        '''
        if not destination in modules:
            continue
        '''
        #------------ part 2 -----------------
        if not destination in modules:
            if destination == "rx":
                if not pulse:
                    print(f"found rx at push {push_count}")
                    return
            continue
        #if destination == "th":
        #    if modules["cn"]["flip"]["th"]:
        #        print(f"th is flipped at push {push_count + 1}")

        # ----------- part 2 -----------------


        if modules[destination]["type"] == "%":
            if not pulse: # if received low pulse, flip the switch and send pulse
                modules[destination]["flip"] = not modules[destination]["flip"]
                for dest in modules[destination]["dest"]:
                    queue.append((destination, dest, modules[destination]["flip"]))
                    cnt[modules[destination]["flip"]] += 1
        else: # Conjunction modules
            modules[destination]["flip"][sender] = pulse
            conj = True
            for connected in modules[destination]["flip"]:
                conj = conj and modules[destination]["flip"][connected]
            for dest in modules[destination]["dest"]:
                queue.append((destination, dest, not conj))
                cnt[not conj] += 1

    return cnt

def check_restored(modules):
    for name in modules:
        if modules[name]["type"] == "%":
            if modules[name]["flip"]:
                return False
        if modules[name]["type"] == "&":
            for connected in modules[name]["flip"]:
                if modules[name]["flip"][connected]:
                    return False
    return True

def calculate_pulses_product(modules, press_cnt):
    restored = False
    pulses_record = []
    while not restored and len(pulses_record) < press_cnt:
        pulses_record.append(push_button(modules, len(pulses_record))) # part 1
        restored = check_restored(modules)

    low_cnt = 0
    high_cnt = 0
    for record in pulses_record:
        high_cnt += record[True]*int(press_cnt/len(pulses_record))
        low_cnt += record[False]*int(press_cnt/len(pulses_record))

    for i in range(press_cnt%len(pulses_record)):
        high_cnt += pulses_record[i][True]
        low_cnt += pulses_record[i][False]

    # return low_cnt*high_cnt


calculate_pulses_product(modules, 100000)

'''
th: 3947
sv: 4001
gh: 3943
ch: 3917
'''

print(3947*4001*3943*3917)