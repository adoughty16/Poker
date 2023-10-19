import Player
import deck
import cards
import Game_state
import time
import threading



class Game():

	def __init__ (self, num_players, game_state, host, db):
		self.game_state = game_state
		self.num_players = num_players
		self.players = [Player() for _ in range(num_players)]
		self.deck = deck()
		self.pot = 0
		self.dealer = 0
		self.host = host
		self.db = db

	def initial_main(self, lock): #determines which game loop to call
		if (self.host):
			self.host_main(lock)
		else:
			self.guest_main(lock)
		pass

	def host_main(self):
		# Needs to establish and confirm connection with guests VIA firestore before game loop
		playing = True
		connected = False
		#first spots in flags hold 0s for players to flip to 1s when they connect.
		#last spot is host confirmation bit that host will flip when all player spots are filled
		flags = [0 for _ in range(self.num_players + 1)]
		self.db.collection("flags").document("flag_document").set({"values": flags})
		flag_document = self.db.collection("flags").document("flag_document").get()

		while not connected:
			#update local flags from database
			flags = flag_document.to_dict()["values"]
			connected = True
			for i in range(self.num_players - 1):
				#if any are 0
				if flags[i] == 0:
					#not everyone is connected yet
					connected = False
			#if all players have connected
			if connected:
				#update and upload confirmation bit
				flags[self.num_players] = 1
				self.db.collection("flags").document("flag_document").set({"values": flags})
		
		#NOTE: game_state = Enum('game_state',['dealing','pre-flop','flop','turn','river','showdown'])
		while playing:
			if self.game_state.fetch_game_state() == 'dealing':
				#deal
				hands = self.deck.deal()
				for player, hand in zip(self.players, hands):
					player.set_hand(hand)

				#update game_state locally, then on db
				self.game_state

			if self.game_state.fetch_game_state() == 'pre-flop':
				pass
			if self.game_state.fetch_game_state() == 'flop':
				pass
			if self.game_state.fetch_game_state() == 'turn':
				pass
			if self.game_state.fetch_game_state() == 'river':
				pass
			if self.game_state.fetch_game_state() == 'showdown':
				pass


	def guest_main(self):
		playing = True
		connected = False
		waiting_for_host = False
		#Needs to establish and confirm connection to host VIA firestore before game loop

		while not connected:
			#check flags on database
			flag_document = self.db.collection("flags").document("flag_document").get()
			if flag_document.exists:
				#grab flags from db
				flags = flag_document.to_dict()["values"]
				#if we haven't reserved a spot in the game
				if not waiting_for_host:
					#look through all flags except the confirmation bit at the end until we find an opening
					for i in range(self.num_players - 1):
						if flags[i] == 0:
							#reserve the opening
							flags[i] = 1
						#break out so we only reserve one spot
						break
					#update flags on the database
					self.db.collection("flags").document("flag_document").set({"values": flags})
					#now we just need to check for the host's confirmation bit
					waiting_for_host = True
				#if we are awaiting confirmation
				if waiting_for_host:
					#check the confirmation bit
					if flags[self.num_players] == 1:
						connected = True
			#sleeping might not be necessary but it keeps us from making maybe 100s of queries while connecting
			time.sleep(1)

		#while playing is true:
		while (playing):
			
			if self.game_state.fetch_game_state() == 'dealing':
				pass
			if self.game_state.fetch_game_state() == 'pre-flop':
				pass
			if self.game_state.fetch_game_state() == 'flop':
				pass
			if self.game_state.fetch_game_state() == 'turn':
				pass
			if self.game_state.fetch_game_state() == 'river':
				pass
			if self.game_state.fetch_game_state() == 'showdown':
				pass

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

	def upload_turn(): #guess uploads turn
		pass

	def fetch_turn(player_index): # host fetches guest turn and updates game state
		pass
