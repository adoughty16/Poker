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
        # Image to use for the sprite when face up (from graphics to interface the two)
        self.image_file_name = f":resources:images/cards/card{self.suit}{self.value}.png"

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
        return self.image_file_name

    # overridden equality operator to compare card objects using == and != (useful in Game_state and maybe other game logic)
    def __eq__(self, other):
        if self.suit == other.suit and self.value == other.value:
            return True
        else:
            return False
    
    # would it help to have a draw function face up and face down? 