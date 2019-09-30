
# A simplified poker hand evaluation system and a simplified simulation of one-on-one Texas Hold'Em

import random
import time

randomCards = []

# ---------------------------------------------------------------------------------|
# TEXAS_HOLDEM: simulates simplified version of a one-on-one game of texas hold'em |
# ---------------------------------------------------------------------------------|
def texas_holdem():
    totalbets = 0
    get_hand()  # randomly deals cards

    # begins game
    print("\nStarting game of Texas Hold'em!\n--------------------------------\n")
    pause()
    print("Dealing cards", end="")
    pause()

    # reveals first two cards of starting hand
    print("\n\nYour starting hand is a {} of {} and a {} of {}.".format(randomCards[0][0], randomCards[0][1],
                                                                        randomCards[1][0], randomCards[1][1]))
    time.sleep(0.5)

    # asks for bets
    if ask_bet():
        totalbets += get_bet()
    printbets(totalbets)

    pause()
    print("Dealing cards", end="")
    pause()

    # reveals first three community cards
    print("\n\nThe first three community cards are: {}-{}, {}-{}, {}-{}.".format(randomCards[2][0], randomCards[2][1],
                                                                                 randomCards[3][0], randomCards[3][1],
                                                                                 randomCards[4][0], randomCards[4][1]))

    # asks for bets
    if ask_bet():
        totalbets += get_bet()
    printbets(totalbets)

    pause()
    print("Dealing cards", end="")
    pause()

    # reveals fourth community cards
    print("\n\nThe fourth community card is: {}-{}.".format(randomCards[5][0], randomCards[5][1]))

    # asks for bets
    if ask_bet():
        totalbets += get_bet()
    printbets(totalbets)

    pause()
    print("Dealing cards", end="")
    pause()

    # reveals final community card
    print("\n\nThe final community card is: {}-{}.".format(randomCards[6][0], randomCards[6][1]))

    # asks for bets
    if ask_bet():
        totalbets += get_bet()
    printbets(totalbets)

    # assigns hands to new separate lists
    pause()
    yourHand = [randomCards[i] for i in range(7)]
    opponentHand = [randomCards[i] for i in range(2, 9)]

    # reveals your hand and your opponents hand
    print("\nYou have: ", end="")
    evaluate(yourHand)
    pause()
    print("\nYour opponent has: ", end="")
    evaluate(opponentHand)

    # evaluates winner and prints results
    if evaluate_score(yourHand) > evaluate_score(opponentHand):
        print("\nCongratulations! You won and doubled your money. You now have ${:.2f}.\n".format(totalbets))
    elif evaluate_score(yourHand) < evaluate_score(opponentHand):
        print("\nOh, no! You lost! You now owe your opponent ${:.2f}.\n".format(totalbets))
    else:
        print("\nYou tied! You don't win or owe any money.\n")

    pause()
    print("End of Game", end="")
    pause()


# evaluates score:
def evaluate_score(poker_hand):
    poker_hand.sort()
    poker_hand_ranks = get_all_ranks(poker_hand)
    if royal_flush(poker_hand):
        return 8
    elif straight_flush(poker_hand):
        return 7
    elif four_of_a_kind(poker_hand_ranks):
        return 6
    elif full_house(poker_hand_ranks):
        return 5
    elif straight(poker_hand):
        return 4
    elif three_of_a_kind(poker_hand_ranks):
        return 3
    elif two_pair(poker_hand_ranks):
        return 2
    elif one_pair(poker_hand_ranks):
        return 1
    else:
        return 0


# generates a random hand of poker
def get_hand():
    randomCards.clear()
    suits = ["spades", "clubs", "diamonds", "hearts"]

    while len(randomCards) != 9:
        suit = random.choice(suits)
        rank = random.randint(2, 14)
        temp = [rank, suit]
        if temp not in randomCards:
            randomCards.append(temp)
    return randomCards[:5]


# UX pause
def pause():
    print(".", end="")
    time.sleep(0.5)
    print(".", end="")
    time.sleep(0.5)
    print(".", end="")
    time.sleep(0.5)

# prints total bets
def printbets(totalbets):
    print("\nYour total bets are: ${:.2f}\n".format(totalbets))

# asks user if they want to bet
def ask_bet():
    while True:
        betYes_No = input("\nDo you want to make a bet? (Y/N) ")
        if betYes_No.upper() == "Y" or betYes_No.upper() == "N":
            break
    if betYes_No.upper() == "Y":
        return True
    else:
        return False


# gets bet amount
def get_bet():
    while True:
        betInput = input("How much do you want to bet? $")
        try:
            bet = float(betInput)
            break
        except ValueError:
            print("\nERROR: You must enter a number.\n")
    return bet


# ----------------------------------------------|
# FLUSH:                                        |
# used for both royal flush and straight flush  |
# takes in hand and lowest rank possible        |
# ----------------------------------------------|

def flush(hand, rank):
    suit = hand[0][1]  # sets suit to variable
    index = 0  # sets index
    flushcount = 0

    # iterates over every card in hand
    for card in hand:

        # checks to see if flush
        if hand[index][0] == rank and hand[index][1] == suit:
            flushcount += 1

        # updates counters
        rank += 1
        index += 1

    return flushcount >= 5


# ----------------------------------------------|
# ROYAL FLUSH:                                  |
# uses flush function and passes 10 as lowest   |
# possible rank                                 |
# ----------------------------------------------|
def royal_flush(hand):
    return flush(hand, 10)


# ----------------------------------------------|
# STRAIGHT FLUSH:                               |
# uses flush function and passes lowest rank    |
# in hand as rank                               |
# ----------------------------------------------|
def straight_flush(hand):
    return flush(hand, hand[0][0])


# ----------------------------------------------|
# STRAIGHT:                                     |
# ----------------------------------------------|
def straight(hand):
    index = 0  # sets index
    rank = hand[0][0]
    straightcount = 0

    # iterates over every card in hand
    for card in hand:

        # checks to see if straight
        if hand[index][0] == rank:
            straightcount += 1

        # updates counters
        rank += 1
        index += 1

    return straightcount >= 5


# ----------------------------------------------|
# N OF A KIND:                                  |
# takes in list of ranks and an integer n       |
# calculates number of ocurrences of size n     |
# within the list of ranks                      |
# ----------------------------------------------|
def n_of_a_kind(ranks, n):
    count = 0  # counter for n-sized occurences

    # copies list of ranks to temp list
    tempList = [ranks[i] for i in range(len(ranks))]

    # iterates over templist, checking if n-sized groups found, if so, deletes those ranks from tempList
    while len(tempList) > 1:
        if tempList.count(tempList[0]) == n:
            count += 1
        for i in range(tempList.count(tempList[0])):
            tempList.pop(0)

    return count


# ----------------------------------------------|
# FOUR OF A KIND:                               |
# ----------------------------------------------|
def four_of_a_kind(ranks):
    if n_of_a_kind(ranks, 4) > 0:
        return True
    else:
        return False


# ----------------------------------------------|
# FULL HOUSE:                                   |
# ----------------------------------------------|
def full_house(ranks):
    if n_of_a_kind(ranks, 2) >= 1 and three_of_a_kind(ranks):
        return True
    else:
        return False


# ----------------------------------------------|
# THREE OF A KIND:                              |
# ----------------------------------------------|
def three_of_a_kind(ranks):
    if n_of_a_kind(ranks, 3) > 0:
        return True
    else:
        return False


# ----------------------------------------------|
# TWO PAIRS:                                    |
# uses count_pairs function to check if 2 pairs |
# ----------------------------------------------|
def two_pair(ranks):
    if n_of_a_kind(ranks, 2) == 2:
        return True
    else:
        return False


# ----------------------------------------------|
# ONE PAIR:                                     |
# uses count_pairs function to check if 1 pair  |
# ----------------------------------------------|
def one_pair(ranks):
    if n_of_a_kind(ranks, 2) == 1:
        return True
    else:
        return False


# ----------------------------------------------+
# Function provided by professor John Paxton.   |
# get_all_ranks(hand) was not written by me.    |
# ----------------------------------------------+
def get_all_ranks(hand):
    result = []
    for card in hand:
        result.append(card[0])
    return result


# ----------------------------------------------+
# Function provided by professor John Paxton.   |
# evaluate(poker_hand) was not written by me.   |
# ----------------------------------------------+
def evaluate(poker_hand):
    poker_hand.sort()
    poker_hand_ranks = get_all_ranks(poker_hand)
    print(poker_hand, "--> ", end="")
    if royal_flush(poker_hand):
        print("Royal Flush")
    elif straight_flush(poker_hand):
        print("Straight Flush")
    elif four_of_a_kind(poker_hand_ranks):
        print("Four of a Kind")
    elif full_house(poker_hand_ranks):
        print("Full House")
    elif straight(poker_hand):
        print("Straight")
    elif three_of_a_kind(poker_hand_ranks):
        print("Three of a Kind")
    elif two_pair(poker_hand_ranks):
        print("Two Pair")
    elif one_pair(poker_hand_ranks):
        print("One Pair")
    else:
        print("Nothing")


# -----------------------------------------+

def main():
    print("Poker Hand Evaluation Program")
    print("---------------------------------------")
    evaluate([[10, "spades"], [14, "spades"], [12, "spades"], [13, "spades"], [11, "spades"]])  # royal flush
    evaluate([[10, "clubs"], [9, "clubs"], [6, "clubs"], [7, "clubs"], [8, "clubs"]])  # straight flush
    evaluate([[2, "diamonds"], [7, "clubs"], [2, "hearts"], [2, "clubs"], [2, "spades"]])  # 4 of a kind
    evaluate([[8, "diamonds"], [7, "clubs"], [8, "hearts"], [8, "clubs"], [7, "spades"]])  # full house
    evaluate([[13, "diamonds"], [7, "clubs"], [7, "hearts"], [8, "clubs"], [7, "spades"]])  # 3 of a kind
    evaluate([[10, "clubs"], [9, "clubs"], [6, "clubs"], [7, "clubs"], [8, "spades"]])  # straight
    evaluate([[10, "spades"], [9, "clubs"], [6, "diamonds"], [9, "diamonds"], [6, "hearts"]])  # 2 pair
    evaluate([[10, "spades"], [12, "clubs"], [6, "diamonds"], [9, "diamonds"], [12, "hearts"]])  # 1 pair
    evaluate([[2, "spades"], [7, "clubs"], [8, "diamonds"], [13, "diamonds"], [11, "hearts"]])  # nothing
    print()
    print("Randomly generated poker hand:")
    evaluate(get_hand())
    texas_holdem()


# -----------------------------------------+

main()
