cards = ["A", "K", "Q", "J", "T", "9", "8", "7", "6", "5", "4", "3", "2"]
hands_rank = ["Five of a kind", "Four of a kind", "Full house", "Three of a kind", "Two pair", "One pair", "High card"]

with open('data/day7_input', 'r') as file:
    input = file.read()

hands = []
bids = []
for line in input.splitlines():
    hands.append(line.split(" ")[0])
    bids.append(int(line.split(" ")[1]))

def count_occurence(char, str):
    cnt = 0
    for c in str:
        cnt += (c == char)
    return cnt

def determine_type(hand): # input must be a hand of five
    unique_cards = set(hand)
    if len(unique_cards) == 1:
        return "Five of a kind"
    elif len(unique_cards) == 2:
        occur_cnt = count_occurence(list(unique_cards)[0], hand)
        return "Four of a kind" if (occur_cnt == 1 or occur_cnt == 4) else "Full house"
    elif len(unique_cards) == 3:
        for card in unique_cards:
            cnt = count_occurence(card, hand)
            if cnt == 3:
                return "Three of a kind"
            elif cnt == 2:
                return "Two pair"
    elif len(unique_cards) == 4:
        return "One pair"
    else:
        return "High card"

types = []
for i in range(len(hands)):
    types.append(determine_type(hands[i]))

type_ranking = {}
for i in range(len(hands_rank)):
    type_ranking[i] = []
for j in range(len(types)):
    type_ranking[hands_rank.index(types[j])].append(j)
print(type_ranking)

def custom_sort(strings):
    priorities = {char: index for index, char in enumerate(cards)}
    def sort_key(string):
        return tuple(priorities.get(char, float('inf')) for char in string)

    return sorted(strings, key=sort_key)

def rank_cards_same_type(cards):
    return custom_sort([hands[i] for i in cards])

hand_num_to_rank = {}
rank = len(hands)
for type_r in range(len(type_ranking)):
    if len(type_ranking[type_r]) > 0:
        for c in rank_cards_same_type(type_ranking[type_r]):
            hand_num_to_rank[c] = rank
            rank -= 1
print(f"rank: {rank}")
print(hand_num_to_rank)

def calculate_winning(rankings):
    sum = 0
    for c in rankings:
        sum += bids[hands.index(c)] * rankings[c]
    return sum

print(f"winning: {calculate_winning(hand_num_to_rank)}")