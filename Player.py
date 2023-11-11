import cards
import random
from enum import Enum
from cards import Card
from itertools import groupby, count
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

    def set_hand(self, lst_cards : [Card]):
        self.hand = lst_cards

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

    def get_hand_type(self, cards):
        # Implement hand type evaluation logic
        # Return the appropriate ENUM from HandStrength

        # high card logic
        pass

    # returns a list of all possible hands from cards, winning hand to be deciphered
    def possible_hands(self, lst_cards):

        # memory to sort lst_cards by value
        memory = [[], [], [], [], [], [], [], [], [], [], [], [], []]

        # memory to count the different types of hands
        flushes = [[],[],[],[]]
        player_straights = []
        player_straight_flushes = []
        pair_values = []

        # sort input lst_cards into memory[] by index of value
        for i in lst_cards:
            memory[i.get_value()].append(i)

        # value = card rank, lst = list of cards in that rank
        # iterate through memory[]
        for value, lst in enumerate(memory):
            # suit = memory[value][i][card].get_suit()
            # iterate through cards of this rank
            for suit, card in enumerate(lst):
                # if there exists a card of the last rank and there exists a card in this rank
                val = value
                last_val_men = memory[value - 1]
                this_val_mem = memory[value][suit]
                if value > 0 and memory[value - 1] and memory[value][suit]:

                    # if the card of the last rank has the same suit of the card of this rank
                    if memory[value - 1][suit].get_suit() == memory[value][suit].get_suit():

                        # add the last card to straight_flushes
                        player_straight_flushes.append([memory[value - 1][suit]])
                        # if card not in player_straight_flushes:
                        #     player_straight_flushes.append(card)
                    # add to straights
                    player_straights.append([memory[value - 1][suit]])
                    # if card not in player_straights:
                    #     player_straights.append(card)
                # add card to flushes array by index of suit
                flushes[card.suit].append(card)
            # if the list of cards of this rank is greater than 1, append it as a list to the list of pairs, pair_values
            if len(lst) > 1:
                pair_values.append(lst)

        return [pair_values,player_straight_flushes,player_straights, flushes]

    # takes in a lst from strength() [pair_values,player_straight_flushes,player_straights, flushes]
    def calculate_strength(self, lst):
        pass
