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
    def __init__(self, name, is_computer_player=False):
        self.name = name
        self.hand = []
        self.stack = 0
        self.is_computer_player = is_computer_player
        showdown_cards = []
        showdown_strength = HandStrength.DEFAULT
    
    def get_name(self):
        return self.name
    
    def get_hand(self):
        return self.hand
    
    def get_stack(self):
        return self.stack
    
    def is_computer_player(self):
        return self.is_computer_player

    def set_strength(self, HandStrength):
        self.HandStrength = HandStrength

    def set_name(self, name):
        self.name = name
    
    def set_hand(self, hand):
        self.hand = hand
    
    def set_player_type(self, boolean_value):
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
        bet_value = 0
        decisions = ["bet", "check", "fold"]
        return random.choice(decisions), bet_value

    def calculate_strength(self, cards):
        # Implement hand strength evaluation
        # Sort the cards by rank (e.g., 2, 3, 4, ..., A)
        sorted_cards = sorted(cards, key=lambda card: card.RANK_ORDER.index(card.rank)) #<---- card sorter i assume. could we merge this into get_hand_type?
        counts = Counter(card.rank for card in sorted_cards) #<----- what is this?

    def get_hand_type(self, cards):
        # Implement hand type evaluation logic
        # Return the appropriate ENUM from HandStrength

        def matching(self, cards):
            #create memory for cards in form list[]
            matching_mem = [0,0,0,0,0,0,0,0,0,0,0,0,0]
            #count of card pairs
            pair_count = 0
            #iterate thru cards
            for i in cards:
                #count each card and add it to matching mem, index = card value
                matching_mem[i.getValue] =+ 1
            #index through matching mem
            for e in matching_mem:
                #if a card value occurs 4 times, return enum four of a kind
                if e == 4:
                    showdown_strength = HandStrength.FOUR_OF_A_KIND
                    return HandStrength.FOUR_OF_A_KIND
                #if a card value occurs 3 times, return enum three of a kind
                if e == 3:
                    showdown_strength = HandStrength.THREE_OF_A_KIND
                    return HandStrength.THREE_OF_A_KIND
                #if a card value occurs twice, increment the count of pairs
                if e == 2:
                    pair_count=+1
            #if there are two pairs, return enum two pair
            if pair_count == 2:
                showdown_strength = HandStrength.TWO_PAIR
                return HandStrength.TWO_PAIR
            #if there is one pair, return enum one_pair
            if pair_count == 1:
                showdown_strength = HandStrength.ONE_PAIR
                return HandStrength.ONE_PAIR

        #this function will use a similar algo to the matching algo
        def flushing(self, cards):
            #create memory for increasing
            flushing_mem = [0,0,0,0,0,0,0,0,0,0,0,0,0]
            current_strength = HandStrength.HIGH_CARD


