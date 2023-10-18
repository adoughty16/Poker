
import cards
# DECK:
# -Cards[]
# get_deck()
# deal() returns 4-tuple of lists of 2 cards each and removes them from Cards[]
# flop() returns list of 3 cards and removes them from Cards[]
# turn() returns 1 card and removes it from Cards[]
# river() returns 1 card and removes it from Cards[]


deck = []

class Deck:

    def __init__(self, deck):
        #for i less than 4
            #for e less than 13
            #add card to the list these_cards, passing in card constructer
            # i is the suit and e is the value
        for i in range(4):
            for e in range(13):
                this_card = cards(i,e)
        
        pass

    def get_deck():
        return self.deck
    def deal():
        
        pass
    def flop():
        pass
    def turn():
        pass
    def river():
        pass
    
 