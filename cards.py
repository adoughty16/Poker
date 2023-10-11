from enum import Enum

# -Suit (ENUM)
# -Value (ENUM?)
# -GUI Asset
# get_suit()
# get_value()
# get_image()

suit = Enum('suit', ['DIAMOND','HEART', 'SPADE', 'CLUB'])

value = Enum('value',[1,2,3,4,5,6,7,8,9,10,11,12,13])

class Card:
    


    def get_suit():
        return suit
    def get_value():
        return value
    def get_image():
        pass