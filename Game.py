import Deck
import Card
import Game_state
import time



class Game:

	def __init__ (self, players, game_state, host, db):
		self.game_state = game_state
		self.players = players
		self.deck = Deck()
		self.pot = 0
		self.dealer = 0
		self.host = host
		self.db = db


	def initial_main(): #determines which game loop to call
		if (host):
			host_main()
		else:
			guest_main()
		pass

	def host_main(self):
		pass
		# Needs to establish and confirm connection with guests VIA firestore before game loop
		flags = [0 for _ in range(self.players + 1)]
		self.db.collection("flags").document("flag_document").set({"values": flags})
		



		#uploads to firestore indicating how many live players are expected (these can just be bits set to zero)

		#periodically checks until all bits are set to 1, indicating lives players are connected and ready.
		#uploads confirmation bit so that lives players can enter game loop.

	def guest_main(self):
		playing = True
		connected = False
		waiting_for_host = False
		#Needs to establish and confirm connection to host VIA firestore before game loop

		while not connected:
			#check firestore for host's flag
			flag_document = self.db.collection("flags").document("flag_document").get()
			if flag_document.exists:
				#grab flags from db
				flags = flag_document.to_dict()["values"]
				#if we haven't reserved a spot in the game
				if not waiting_for_host:
					#look through flags until we find an opening
					for i in range(self.players - 1):
						if flags[i] == 0:
							#reserve the opening
							flags[i] = 1
						#break out so we only reserve one spot
						break
					#now we just need to check for the host's confirmation bit
					waiting_for_host = True
				#if we are awaiting confirmation
				if waiting_for_host:
					#check the confirmation bit
					if flags[self.players] == 1:
						connected = True
			#sleeping might not be necessary but it keeps us from making maybe 100s of queries while connecting
			time.sleep(1)

		#while playing is true:
		while (playing):

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
