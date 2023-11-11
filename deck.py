import random
from enum import Enum
from cards import Card 

# DECK:
# -Cards[]
# get_deck()
# deal() returns 4-tuple of lists of 2 cards each and removes them from Cards[]
# flop() returns list of 3 cards and removes them from Cards[]
# turn() returns 1 card and removes it from Cards[]

suit = Enum('suit', ['d','c','h','s'])
deck = []

class Deck:

    def __init__(self):
        these_cards=[]
        #for i less than 4
        # suit = ['d','c','h','s']
        for suit in range(4):
            #for e less than 13
            for value in range(14):
            #add card to the list these_cards, passing in card variables
                these_cards.append(Card(suit,value))
        #shuffle this deck
        random.shuffle(these_cards)
        self.deck = these_cards


    def get_deck(self):
        return self.deck
    
    #returns 4-tuple of lists of 2 cards for each hand (h) and removes them from cards
    def deal(self):
        h1 = [self.deck.pop() for _ in range(2)]
        h2 = [self.deck.pop() for _ in range(2)]
        h3 = [self.deck.pop() for _ in range(2)]
        h4 = [self.deck.pop() for _ in range(2)]

        return [h1, h2, h3, h4]

    #returns list of 3 cards and removes them from Cards
    def flop(self):
        flop=[self.deck.pop() for _ in range(3)]
        return flop


    #returns 1 card and removes it from deck[]
    def turn(self):
        return self.deck.pop()
 