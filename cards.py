from enum import Enum

# -Suit (ENUM)
# -Value (ENUM?)
# -GUI Asset
# get_suit()
# get_value()
# get_image()

# d = diamonds
# c = clubs
# h = hearts
# s = spades
suit = Enum('suit', ['d','c','h','s'])

value = Enum('value',[1,2,3,4,5,6,7,8,9,10,11,12,13])

class Card:
    
    def __init__(self, suit, value ):
        self.suit=suit
        self.value=value

    #compare to function
    #if the card passed in is greater than this card, return 1
    #if the card passed in is less than this card, return -1
    #if the card passed in is equal to this card, return 0
    def compareTo(this_card):
        if (this_card.value>this.card.value):
            return 1
        if (this_card.value<this.card.value):
            return -1
        if (this_card.value==this.card.value):
            return 0
        
    
    def get_suit(self):
        return self.suit
    def get_value(self):
        return self.value
    def get_image(self):
        pass