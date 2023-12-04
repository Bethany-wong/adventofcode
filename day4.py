with open('data/day4_input', 'r') as file:
    input = file.read()
input_lines = input.splitlines()

def count_winning_cards(winning_nums, card_nums): # count the number of matching cards
    cnt = 0
    for num in card_nums:
        if num in winning_nums:
            cnt += 1
    return cnt

def calculate_score(winning_nums, card_nums):
    cnt = count_winning_cards(winning_nums, card_nums)
    return 0 if cnt == 0 else 2**(cnt-1)

def get_winning_and_current_cards(line): # find a list of winning cards and a list of cards i have
    line_list = line.split(" ")
    # find start of winning numbers
    pointer = 0
    while not line_list[pointer].isnumeric() and pointer < len(line_list):
        pointer += 1
    # store them
    winning_nums = []
    while line_list[pointer] != "|" and pointer < len(line_list):
        if line_list[pointer].isnumeric():
            winning_nums.append(int(line_list[pointer]))
        pointer += 1
    # store numbers I have
    nums_on_card = []
    while pointer < len(line_list):
        if line_list[pointer].isnumeric():
            nums_on_card.append(int(line_list[pointer]))
        pointer += 1
    return winning_nums, nums_on_card


total_score = 0
for line in input_lines:
    winning_nums, nums_on_card = get_winning_and_current_cards(line)
    total_score += calculate_score(winning_nums, nums_on_card)

print(total_score)


# ---------------------- part 2 ---------------------------------------

matching_num = [] # winning number of each card: 0th element is matching number of card 1
for line in input_lines:
    winning_nums, nums_on_card = get_winning_and_current_cards(line)
    matching_num.append(count_winning_cards(winning_nums, nums_on_card))
#print("matching_num: " + str(matching_num))

cards = [1 for i in range(len(input_lines))]
for i in range(len(cards)):
    #print(cards)
    for j in range(1, matching_num[i] + 1):
        if j >= len(input_lines):
            break
        cards[i + j] += cards[i]
        j += 1

print(sum(cards))