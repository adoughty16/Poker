import random
from enum import IntEnum
from cards import Card
from Game_state import Game_state


# for reference- https://en.wikipedia.org/wiki/List_of_poker_hands#Full_house


class HandStrength(IntEnum):
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
        self.stack = 1000
        self.is_computer_player = True  # defaults to computer player
        self.showdown = []
        self.handRank = 0
        self.handStrength = HandStrength.DEFAULT
        self.possiblehands = []

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

    def turn(self, community_cards, db):
        # return decision (bet, check, fold)
        decision = self.make_decision(community_cards, db)
        return decision

    def evaluate_hand(self, community_cards):
        #  takes in community_cards, combines them with self.hand, and returns the ENUM for the player's hand.

        combined_cards = self.hand + community_cards

        hand_type = self.possible_hands(combined_cards)

        return hand_type

    # returns a list of all possible hands from cards, winning hand to be deciphered
    def possible_hands(self, community_cards):

        lst_cards = self.hand + community_cards
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
            memory[i.get_value()-1].append(i)

        # finding pairs and flushes ----------------------------------------------------------

        # iterate through memory[]
        for lst in memory:
            # iterate through cards of this rank
            for card in lst:
                # add card to flushes array by index of suit
                flushes[card.suit].append(card)
            # if the list of cards of this rank is greater than 1, append it as a list to the list of pairs, pair_values
            if len(lst) > 1:
                pair_values.append(lst)

        # finding straights and straight flushes --------------------------------------

        # mem for straight flush
        current_sf_subset = [lst_cards[0]]
        # mem for straight
        current_straight_subset = [lst_cards[0]]

        # iterate through given list of cards
        for i in range(1, len(lst_cards)):
            # if this cards value equals the last card value plus one
            if lst_cards[i].value == current_straight_subset[-1].value + 1:
                # add it to a subset of straights
                current_straight_subset.append(lst_cards[i])
                # if this card suit equals the last cards suit as well,
                if lst_cards[i].suit == current_sf_subset[-1].suit:
                    # add it to the straight flush mem
                    current_sf_subset.append(lst_cards[i])
            else:
                player_straights.append(current_straight_subset)
                player_straight_flushes.append(current_sf_subset)
                current_straight_subset = [lst_cards[i]]
                current_sf_subset = [lst_cards[i]]

        player_straight_flushes.append(current_sf_subset)
        player_straights.append(current_straight_subset)

        # high card ----------------------------------------------
        max_val = 0
        for i in lst_cards:
            if i.get_value() > max_val:
                max_val = i.get_value()
                highest_card = i

        # pruning ------------------------------------------------
        def prune(by, to_prune):
            prune = []
            for e, i in enumerate(to_prune):
                if len(i) > 5:
                    i = i[-5:]
                if len(i) > by:
                    prune.append(i)

            return prune

        def maxed(lst):
            maxed = []
            if len(lst) > 0:
                maxed.append(max(lst, key=len))
            return maxed

        def denest(lst):
            if len(lst) == 1 and isinstance(lst, list):
                return lst[0]

        pair_values = prune(1, pair_values)
        pruned_player_straight_flushes = prune(3, player_straight_flushes)
        pruned_player_straights = prune(3, player_straights)
        pruned_flushes = prune(3, flushes)
        straight = denest(maxed(pruned_player_straights))
        flush = denest(maxed(pruned_flushes))
        straight_flush = denest(maxed(pruned_player_straight_flushes))

        # for AI use
        self.possiblehands = [pair_values, player_straight_flushes, player_straights, flushes, highest_card]

        # deciding -----------------------------------------

        if straight_flush and len(straight_flush) == 5:
            return [straight_flush[0].value, HandStrength.STRAIGHT_FLUSH]
        if pair_values:
            max_pair = max(pair_values, key=len)
            if len(max_pair) == 4:
                return [max_pair[0].value, HandStrength.FOUR_OF_A_KIND]
            if len(pair_values) > 1 and len(pair_values[-1]) == 3 and len(pair_values[-2]) == 2:
                return [pair_values[-1][0].value, HandStrength.FULL_HOUSE]
        if flush:
            if len(flush) == 5:
                flush_rank = max(flush, key=lambda card: card.value)
                return [flush_rank.value, HandStrength.FLUSH]
        if straight:
            if len(straight) == 5:
                return [straight[0].value, HandStrength.STRAIGHT]
        if pair_values:
            max_pair = max(pair_values, key=len)
            if len(max_pair) == 3:
                return [max_pair[0].value, HandStrength.THREE_OF_A_KIND]
            if len(pair_values) == 2:
                return [pair_values[-1][0].value, HandStrength.TWO_PAIR]
            if len(pair_values) == 1:
                return [pair_values[-1][0].value, HandStrength.ONE_PAIR]

        return [highest_card.value, HandStrength.HIGH_CARD]

    def make_decision(self, community_cards, db):

        # # for now
        # return "call", 0
        #
        # # could use evaluate_strength and evaluate_hand as part of decision
        # # random decision for now
        # # EDIT needs to return a bet value if decision is bet. This can just be zero if the decision is not bet
        # decisions = ["bet", "check", "fold"]
        # choice = random.choice(decisions)
        # if choice == "bet":
        #     bet_value = 5 * random.randint(1, 10)  # THIS IS A PLACEHOLDER
        # else:
        #     bet_value = 0
        #
        # # ------------------------------------------ AI PSEUDOCODE

        # lst_cards = self.hand + community_cards
        lst_cards = self.hand + community_cards
        # [pair_values, player_straight_flushes, player_straights, flushes, highest_card]
        decided = self.possible_hands(lst_cards)

        # if len(community_cards)
        # if second round
        if len(lst_cards) == 7:
            if decided[1] > 6:
                if decided[0] > 9:
                    decision = "bet"
                    # ALL IN!
                    bet_value = Game_state.get_total_pot(db)
                    return decision, bet_value
                decision = "bet"
                bet_value = Game_state.get_total_pot(db) * (1 + random.randint(5, 10))
                return decision, bet_value
            if decided[1] > 3:
                decision = "bet"
                bet_value = decided[0] * (1 + random.randint(5, 10))
                return decision, bet_value
            if decided[1] > 1:
                decision = "bet"
                bet_value = decided[0] * (1 + random.randint(1, 5))
                return decision, bet_value

        if len(lst_cards) == 4:

            if decided[1] == HandStrength.HIGH_CARD:
                if decided[0] > 9:
                    decision = "bet"
                    bet_value = decided[0] * random.randint(0, 5)
                    return decision, bet_value
                else:
                    decision = "bet"
                    bet_value = decided[0] * random.randint(1, 5)
                    return decision, bet_value
        if len(lst_cards) < 4:

            # if rank is two pair or greater
            if decided[1] > 6:
                # if straight flush has a high card
                if decided[0] > 7:
                    # raise = current_pot * 2/3
                    decision = "bet"
                    #              vvvvvvvvvvvvvvvvvvvvvvvv  how get total pot?
                    bet_value = Game_state.get_total_pot(db) * (1 + random.randint(1, 4) / 3)
                    return decision, bet_value
                # raise = current_ pot * 1/2
                decision = "bet"
                bet_value = Game_state.get_total_pot(db) * 1.5
                return decision, bet_value
            # if returns flush > 2
            if decided[1] == HandStrength.ONE_PAIR:
                decision = "bet"
            # raise = current_pot * 1/3
                bet_value = Game_state.get_total_pot(db) * (1 + 1/3)
                return decision, bet_value
            if decided[1] < 2:
                decisions = ["bet", "check", "fold"]
                choice = random.choice(decisions)
                return choice, 0
            # if first round, check
        if len(lst_cards) == 2:
            decision = "check"
            choice = random.choice(decision)
            if choice == "bet":
                bet_value = 5 * random.randint(1, 10)  # THIS IS A PLACEHOLDER
                return choice, bet_value
            else:
                bet_value = 0
                return choice, bet_value


