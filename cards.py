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

class Card:
    
    def __init__(self, suit, value):
        self.suit=suit
        self.value=value
        #for key in dictionary:
         #   if key == 'suit':
          #      self.set_suit(self, dictionary[key])
           # if key == 'value':
            #    self.set_value(self, dictionary[key])

    def to_dict(self):
        return {"suit": self.suit, "value": self.value}

    def set_suit(self, suit):
        self.suit = suit
    
    def set_value(self, value):
        self.value = value 

    #compare to function
    #if the card passed in is greater than this card, return 1
    #if the card passed in is less than this card, return -1
    #if the card passed in is equal to this card, return 0
    def compareTo(self, this_card):
        if (this_card.value>self.card.value):
            return 1
        if (this_card.value<self.card.value):
            return -1
        if (this_card.value==self.card.value):
            return 0
        
    
    def get_suit(self):
        return self.suit
    def get_value(self):
        return self.value
    def get_image(self):
        pass

    