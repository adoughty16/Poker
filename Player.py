from enum import Enum
import cards

player_turn = Enum('player_turn',['bet','check','fold'])


class player:

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

    def evaluate_strength(community_cards):
        return
    
    def evaluate_hand(community_cards):
        return
            
