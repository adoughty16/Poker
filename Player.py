import cards
import random
from enum import Enum
from collections import Counter


class HandStrength(Enum):
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
        self.is_computer_player = True #defaults to computer player
    
    def get_name(self):
        return self.name
    
    def get_hand(self):
        return self.hand
    
    def get_stack(self):
        return self.stack
    
    def is_computer_player(self):
        return self.is_computer_player
    
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
        #EDIT needs to return a bet value if decision is bet. This can just be zero if the decision is not bet
        bet_value = None
        decisions = ["bet", "check", "fold"]
        return random.choice(decisions), bet_value

    def calculate_strength(self, cards):
        # Implement hand strength evaluation
        # Sort the cards by rank (e.g., 2, 3, 4, ..., A)
        sorted_cards = sorted(cards, key=lambda card: Card.RANK_ORDER.index(card.rank))
        counts = Counter(card.rank for card in sorted_cards)

        if self.is_royal_flush(sorted_cards):
            return HandStrength.ROYAL_FLUSH
        elif self.is_straight_flush(sorted_cards):
            return HandStrength.STRAIGHT_FLUSH
        elif self.is_four_of_a_kind(counts):
            return HandStrength.FOUR_OF_A_KIND
        elif self.is_full_house(counts):
            return HandStrength.FULL_HOUSE
        elif self.is_flush(sorted_cards):
            return HandStrength.FLUSH
        elif self.is_straight(sorted_cards):
            return HandStrength.STRAIGHT
        elif self.is_three_of_a_kind(counts):
            return HandStrength.THREE_OF_A_KIND
        elif self.is_two_pair(counts):
            return HandStrength.TWO_PAIR
        elif self.is_one_pair(counts):
            return HandStrength.ONE_PAIR
        else:
            return HandStrength.HIGH_CARD
    def get_hand_type(self, cards):
        # Implement hand type evaluation logic
        # Return the appropriate ENUM from HandStrength

        def is_royal_flush(self, cards):
            # Check if it's a Royal Flush (A, K, Q, J, 10 of the same suit)
            pass

        def is_straight_flush(self, cards):
            # Check if it's a Straight Flush
            pass

        def is_four_of_a_kind(self, counts):
            # Check if it's Four of a Kind
            pass

        def is_full_house(self, counts):
            # Check if it's a Full House
            pass

        def is_flush(self, cards):
            # Check if it's a Flush
            pass

        def is_straight(self, cards):
            # Check if it's a Straight
            pass

        def is_three_of_a_kind(self, counts):
            # Check if it's Three of a Kind
            pass

        def is_two_pair(self, counts):
            # Check if it's Two Pair
            pass

        def is_one_pair(self, counts):
            # Check if it's One Pair
            return 2 in counts.values()
