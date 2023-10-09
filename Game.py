import Deck
import Card
import Game_state

class Game

def __init__ (self, players, game_state):
self.game_state = game_state
self.players = players
self.deck = Deck()
self.pot = 0
self.dealer = 0

def initial_main(): #determines which game loop to call
	if (???):
		host_main()
	else:
		guest_main()
	pass

def host_main():
	pass
	# Needs to establish and confirm connection with guests VIA firestore before game loop
def guest_main():
	pass
	#Needs to establish and confirm connection to host VIA firestore before game loop

def find_best_hand():
	#calls each player's evaluate_hand() and determines the winner. If there is a tie, it can 
	#systematically search through individual hands for the highest card.
	pass

def upload_game_state(): #uploads game-state to server
	pass
	
def fetch_game_state(): #fetches game-state from server
	pass

def upload_turn() #guess uploads turn
	pass

def fetch_turn(player_index): # host fetches guest turn and updates game state
	pass
