from enum import Enum
import cards

player_turn = Enum('player_turn',['bet','check','fold'])


class Player:

    def __init__(self, name, is_computer_player):
        self.name=name
        self.is_computer_player=is_computer_player

    #hand is 2 card objects 
    hand = []

    #stack is an int (money value)
    stack = 0

    def is_computer_player(self):
        return self.is_computer_player

    def turn():
        #if !is_computer_player
            #ask the player for their turn
            #return turn
        #if !is_computer_player
            #future: analyze hand and able and make turn accordingly
            #sprint 1: randomized
        return
    
    def set_hand(self, hand):
        self.hand = hand

    def get_hand(self):
        return self.hand

    def set_stack(self, value):
        self.stack = value

    def get_stack(self):
        return self.stack

    def evaluate_strength(community_cards):
        return
    
    def evaluate_hand(community_cards):
        return
            
