import random
import cards
# DECK:
# -Cards[]
# get_deck()
# deal() returns 4-tuple of lists of 2 cards each and removes them from Cards[]
# flop() returns list of 3 cards and removes them from Cards[]
# turn() returns 1 card and removes it from Cards[]


deck = []

class Deck:

    def __init__(self, deck):
        these_cards=[]
        #for i less than 4
        for suit in range(4):
            #for e less than 13
            for value in range(13):
            #add card to the list these_cards, passing in card variables
                these_cards.append(suit,value)
        #shuffle this deck
        random.shuffle(these_cards)
        return these_cards


    def get_deck(self):
        return self.deck
    
    #returns 4-tuple of lists of 2 cards for each hand (h) and removes them from cards
    def deal(self):
        h1 = [self.deck.pop() for _ in range(2)]
        h2 = [self.deck.pop() for _ in range(2)]
        h3 = [self.deck.pop() for _ in range(2)]
        h4 = [self.deck.pop() for _ in range(2)]

        return (h1, h2, h3, h4)

    #returns list of 3 cards and removes them from Cards
    def flop():
        this_flop=[]
        this_flop.append(deck.pop())
        this_flop.append(deck.pop())
        this_flop.append(deck.pop())
        return this_flop

    #returns 1 card and removes it from deck[]
    def turn():
        return deck.pop()
 