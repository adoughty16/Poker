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

        #these both can probably be consolidated into one matrix- a 13-list of a 4-list of cards
        #columns being rank, rows being suit. but for now its this
        # memory for matching cards, stores a list of a list of cards
        matching = [[], [], [], [], [], [], [], [], [], [], [], [], []]
        # memory for sequential cards, stores a list of a list of cards
        straight = [[], [], [], [], [], [], [], [], [], [], [], [], []]
        flushing = [[], [], [], []]
        # memory for number of pairs
        pairs = 0
        pair_values = []
        #memory for flush/ sequential cards
        sequence = [[straight[0]]]

        #sort the cards into the memory
        for e, i in enumerate(cards):
            # add the card to its position in straight[] as indexed by the cards own value
            straight[cards[i].get_value()].append(cards[e])
            # same as above but store in matching[]
            matching[cards[i].get_value()].append(cards[i])
            #sort cards into suits
            if i.get_suit() == 'd':
                flushing[0].append(i)
            if i.get_suit() == 'c':
                flushing[1].append(i)
            if i.get_suit() == 'h':
                flushing[2].append(i)
            if i.get_suit() == 's':
                flushing[3].append(i)

        #find sequential cards
        for i in range(1, len(straight)):
            if straight[i-1][0] + 1 == straight[i][0]:
                sequence[-1].append(straight[i][0])
            else:
                sequence.append([straight[i]])

        # find cards sequential strength
        if len(straight) == 5 and len(sequence) == 5:  # and minimum card in this flush is ace:
            self.handStrength = HandStrength.FLUSH
        if len(straight) == 5:
            self.handStrength = HandStrength.FLUSH

        #find hand strength for matching cards
        for e, i in enumerate(matching):

            # if the list of cards sorted by index contains
            if len(i) == 4:
                # set this players handstrength to four of a kind and set their showdown cards to these cards
                self.handStrength = HandStrength.FOUR_OF_A_KIND
                self.showdown = i
                return HandStrength.FOUR_OF_A_KIND

            if len(i) == 3:
                # same as before
                self.handStrength = HandStrength.THREE_OF_A_KIND
                self.showdown = i
                return HandStrength.THREE_OF_A_KIND

            if len(i) == 2:
                # if there is a pair, add it to a pair counter and store the value for later
                pairs = +1
                pair_values.append(e)

        if pairs == 1:
            self.handStrength = HandStrength.ONE_PAIR
            # set the showdown cards to the pair by their index as stored in pair_values[]
            self.showdown = matching[pair_values.pop()]
            return HandStrength.ONE_PAIR

        if pairs == 2:
            self.handStrength = HandStrength.TWO_PAIR
            # same as above but pop from pair values one more time
            self.showdown = matching[pair_values.pop()]
            self.showdown.append(matching[pair_values.pop()])
            return HandStrength.TWO_PAIR
