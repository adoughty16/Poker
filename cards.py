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

    # TODO: add a to_dict and from_dict to use with firebase 
    # need to add in a from_dict and to_dict for storing card objects in arrays in database (see Game State get_player_hands, set_community_cards, etc) 
    def __init__(self, dict):
        self.suit = ''
        self.value = ''
        for key in dict:
            setattr(self, key, dict[key])

    

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