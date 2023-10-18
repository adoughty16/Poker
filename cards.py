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


    def get_suit():
        return self.suit
    def get_value():
        return self.value
    def get_image():
        pass