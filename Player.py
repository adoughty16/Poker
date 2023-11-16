import cards
import random
from enum import Enum
from cards import Card
from itertools import groupby, count
from collections import Counter

# for reference- https://en.wikipedia.org/wiki/List_of_poker_hands#Full_house

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
        self.handRank = 0
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

    def set_hand(self, lst_cards: [Card]):
        self.hand = lst_cards

    def set_computer_player(self, boolean_value):
        self.is_computer_player = boolean_value

    def turn(self, community_cards):
        # return decision (bet, check, fold)
        decision = self.make_decision(community_cards)
        return decision

    def evaluate_hand(self, community_cards):
        #  takes in community_cards, combines them with self.hand, and returns the ENUM for the player's hand.

        combined_cards = self.hand + community_cards

        hand_type = self.best_hand(self.possible_hands(combined_cards))

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

        # ------------------------------------------ AI PSEUDOCODE

        # lst_cards = self.hand + community_cards
        lst_cards = self.hand
        # if first round, buy in
        # if len(community_cards)
        # if second round
            # possible_hands(lst_cards)
            # if returns straight flush > 2
                # if straight flush has a high card
                    # raise = current_pot * 2/3
                # raise = current_ pot * 1/2
            # if returns flush > 2
                # raise = current_pot * 1/3
            # if returns straight > 2/ royals > 2/ straight flush > 1 / pair > 1
                # raise = current_pot * 1/5
            # if none
                # random: 50/50% chance btwn match or raise current_pot * 1/10

        return choice, bet_value

    def best_hand(self, possible_hands):

        best = []

        return best



    # returns a list of all possible hands from cards, winning hand to be deciphered
    def possible_hands(self, lst_cards):

        # sort the cards by value
        lst_cards = sorted(lst_cards, key=lambda card: card.value)

        # memory to sort lst_cards by value
        memory = [[], [], [], [], [], [], [], [], [], [], [], [], []]

        flushes = [[], [], [], []]
        player_straights = []
        player_straight_flushes = []
        pair_values = []

        # sort input lst_cards into memory[] by index of value
        for i in lst_cards:
            memory[i.get_value()].append(i)

        # iterate through memory[]
        for lst in memory:
            # iterate through cards of this rank
            for card in lst:
                # add card to flushes array by index of suit
                flushes[card.suit].append(card)
            # if the list of cards of this rank is greater than 1, append it as a list to the list of pairs, pair_values
            if len(lst) > 1:
                pair_values.append(lst)

        # mem for straight flush
        current_sf_subset = [lst_cards[0]]
        # mem for straight
        current_straight_subset = [lst_cards[0]]

        # iterate through given lsit of cards
        for i in range(1, len(lst_cards)):
            # if this cards value equals the last card value plus one
            if lst_cards[i].value == current_straight_subset[-1].value + 1:
                # add it to a subset of straights
                current_straight_subset.append(lst_cards[i])
                # if this card suit equals the last cards suit as well,
                if lst_cards[i].suit == current_straight_subset[-1].suit:
                    # add it to the straight flush mem
                    current_sf_subset.append(lst_cards[i])
            else:
                player_straights.append(current_straight_subset)
                player_straight_flushes.append(current_sf_subset)
                current_straight_subset = [lst_cards[i]]
                current_sf_subset = [lst_cards[i]]

        player_straight_flushes.append(current_sf_subset)
        player_straights.append(current_straight_subset)

        def prune(by, lst):
            prune = []
            for i in lst:
                if len(i) > by:
                    prune.append(i)
            return prune

        pruned_pair_values = prune(1, pair_values)
        pruned_player_straight_flushes = prune(3, player_straight_flushes)
        pruned_player_straights = prune(3, player_straights)
        pruned_flushes = prune(3, flushes)

        return [pruned_pair_values, pruned_player_straight_flushes, pruned_player_straights, pruned_flushes]


