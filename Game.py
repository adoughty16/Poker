import Deck
import Card
import Game_state



class Game:

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

		#uploads to firestore indicating how many live players are expected (these can just be bits set to zero)

		#periodically checks until all bits are set to 1, indicating lives players are connected and ready.
		#uploads confirmation bit so that lives players can enter game loop.

	def guest_main():
		pass
		#Needs to establish and confirm connection to host VIA firestore before game loop

		#periodically checks firestore for host connection upload.
		#when host is connected, flips the first available bit to 1.
		#periodically checks for confirmation bit. When confirmation bit flips, enter game loop

		#while playing is true:
		while (Game_state==)

			#fetch_game_state() until it is your turn

			#update game_state for drawing

			#while your turn:
				#check for decision from GUI (maybe a shared list called decision with 
											#binary values for  [check, call, fold, bet], and a separate shared value for
											#bet amount)
				#if bet
					#reduce stack by bet amount
					#upload_turn()
				#if call
					#reduce stack by call
					#upload_turn()
				#if fold
					##upload_turn()
				#if check
					##upload_turn()


				#your turn is false





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
