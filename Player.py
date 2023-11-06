import cards
import random
from enum import Enum
from collections import Counter


class HandStrength(Enum):
    DEFAULT = 0
    HIGH_CARD = 1
    ONE_PAIR = 2
    TWO_PAIR = 3
    THREE_OF_A_KIND = 4
    STRAIGHT = 5
    FLUSH = 6
    FULL_HOUSE = 7
    FOUR_OF_A_KIND = 8
    STRAIGHT_FLUSH = 9
    ROYAL_FLUSH = 10


class Player:
    def __init__(self):
        self.name = None
        self.hand = []
        self.stack = 0
        self.is_computer_player = True  # defaults to computer player
        self.showdown = []
        self.handStrength = HandStrength.DEFAULT

    def get_name(self):
        return self.name

    def get_hand(self):
        return self.hand

    def get_stack(self):
        return self.stack

    def get_player_type(self):
        return self.is_computer_player

    def set_stack(self, stack):
        self.stack = stack

    def set_name(self, name):
        self.name = name

    def set_hand(self, hand):
        self.hand = hand

    def set_computer_player(self, boolean_value):
        self.is_computer_player = boolean_value

    def turn(self, community_cards):
        # return decision (bet, check, fold)
        decision = self.make_decision(community_cards)
        return decision

    def evaluate_strength(self, community_cards):
        # takes community_cards, combines with self.hand, returns strength
        combined_cards = self.hand + community_cards
        hand_strength = self.calculate_strength(combined_cards)
        return hand_strength

    def evaluate_hand(self, community_cards):
        #  takes in community_cards, combines them with self.hand, and returns the ENUM for the player's hand.

        combined_cards = self.hand + community_cards
        hand_type = self.get_hand_type(combined_cards)
        return hand_type

    def make_decision(self, community_cards):
        # could use evaluate_strength and evaluate_hand as part of decision
        # random decision for now
        # EDIT needs to return a bet value if decision is bet. This can just be zero if the decision is not bet
        decisions = ["bet", "check", "fold"]
        choice = random.choice(decisions)
        if choice == "bet":
            bet_value = 5 * random.randint(1, 10)  # THIS IS A PLACEHOLDER
        else:
            bet_value = 0

        return choice, bet_value

    def predict_hand_strength(self,cards):
        #takes any size list of cards and analyzes them based on their rank, and matching suits or values
        #returns their potential as a score or something
        pass

    #calculates the strongest hand possible for showdown
    def calculate_strength(self, cards):

        #sorts the cards -- can someone explain/fix this? vvv
        sorted_cards = sorted(cards, key=lambda card: Card.RANK_ORDER.index(card.rank))
        #i dont know what this does
        counts = Counter(card.rank for card in sorted_cards)

        #rows being rank, columns being suit
        # memory for cards, sorted by value, holding a 5-tuple, first item holds bool representing whether or not a card with this
        #rank exists in this hand, the next 4 each representing a suit and holding a card of that suit
        memory = [[[False],[],[],[],[]], [[False],[],[],[],[]],
                  [[False],[],[],[],[]], [[False],[],[],[],[]],
                  [[False],[],[],[],[]], [[False],[],[],[],[]],
                  [[False],[],[],[],[]], [[False],[],[],[],[]],
                  [[False],[],[],[],[]], [[False],[],[],[],[]],
                  [[False],[],[],[],[]], [[False],[],[],[],[]],
                  [[False],[],[],[],[]]]
        pairs = 0
        pair_values = []
        flush = [[],[],[],[]]
        straight = []
        straight_flush = [[], [], [], []]

        def retrieve(lst):
            for e, i in enumerate(lst):
                pass

        #sort the cards into the memory
        for e, i in enumerate(cards):
            memory[i.get_value()][0] = True
            #sort cards into suits
            memory[i.get_value()][i.suit_val()] = i



        def straightSequence(cards):
            res = [[cards[0]]]

            for i in range (1,len(cards)):
                if cards[i-1].get_value() + 1 == cards[i].get_value():
                    res[-1].append(cards[i])
                else:
                    res.append([cards[i]])
            return res

        #e is the value, i is the list of cards in that value
        for e, i in enumerate(memory):
            #f > 0 is the suit (0 is the flag) and h is the card itself
            for f, h in enumerate(i):
                #memory[value][i] // i[suit][card]
                #so memory[value][suit][card]
                #suit value 0 is a flag for if a card of this value exists

                #if this card is an increment of the last one
                if f > 0 and e > 0 and memory[e-1][i][0] and memory[e][i][0]:
                    straight.append(h)




