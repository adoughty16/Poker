import Player
import deck
import cards
import Game_state
import time



class Game():
#
	def __init__ (self, num_players, game_state, host, db):
		#the gamestate
		self.game_state = game_state
		#number of human players in this game
		self.num_players = num_players
		#shared cards on table 
		self.community_cards = []
		#list of local player objects
		self.players = [Player() for _ in range(4)]
		#the deck
		self.deck = deck()
		#the current betting pot
		self.pot = 0
		#players[] index to track current dealer
		self.dealer = 0
		#players[] index to track the current player (whose turn it is)
		#automatically 3 because in the first round the dealer/smallblind/bigblind players are in 0,1,2
		self.current = 3
		#total call is the maximum value that has been bet in the current round by any player (this helps keep track of
		# the miniumum call values for players who have already put money into the pot for the round. So the call value for
		# a given player is the total_call minus the amount they have already bet this round)
		self.total_call = 10
		#round bets keeps track of the total money bet so far in the current round by each player (organized by index)
		self.round_bets = [0, 0, 0, 0]
		#everyone starts with 1000
		self.stacks = [1000, 1000, 1000, 1000]
		#me is my index in the player list
		self.me = 0
		#host is a boolean that tells me if I am the host or not
		self.host = host
		#db is the firestore db that holds the game state and the connection flags
		self.db = db
		#actives is the indexes of all the players in the round who have not folded and who have not busted out of the game
		self.actives = [0, 1, 2, 3]

	def initial_main(self, lock): #determines which game loop to call
		if (self.host):
			self.host_main(lock)
		else:
			self.guest_main(lock)
		pass

	def host_main(self, lock):
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
			#for all the flags that  aren't the confirmation bit
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
		
		while playing:
			#set dealer in game state
			#and erase player hands in database
			#DECK WILL NEED TO BE RESET TOO.
			lock.aquire:()
			self.game_state.set_dealer(self.dealer, self.db)
			self.game_state.set_player_hands([None] for i in range(4))
			lock.release()
			# other inits for game_state

			#if round is dealing
			if self.game_state.get_round() == 'dealing':
				#deal from the deck
				hands = self.deck.deal()
				for player, hand in zip(self.players, hands):
					player.set_hand(hand)

				#update game_state with the hands (automatically uploads)
				#BECAUSE THE GAME STATE NEEDS TO BE UPDATED BUT WE DON'T WANT HANDS TO BE AVAILABLE
				#ON THE DATABASE MAYBE WE SHOULD HAVE THIS FUNCTION BE THE ONLY ONE THAT DOESN'T AUTOMATICALLY
				#UPDATE TO THE DB. INSTEAD WE COULD HAVE A DIFFERENT FUNCTION TO PUSH HANDS TO THE DB DURING SHOWDOWN
				lock.aquire() 
				for player, hand in zip(self.game_state.get_players(self.db), hands):
					player.set_hand(hand)
				lock.release()

			#if we are in a betting round
			if self.game_state.get_round() == 'pre-flop' or 'flop' or 'turn' or 'river':
				#enter the betting loop
				#all_called will tell us if we can move on to the next round
				all_called = False
				#establish dealer/blinds by adding to the pot and removing the values from the players in the blind positions
				#(blind positions are determined relative to the dealer position)
				self.pot += 15
				self.players[(self.dealer + 1) % 4].set_stack(self.players[(self.dealer + 1) % 4].get_stack() - 5)
				self.round_bets[(self.dealer + 1) % 4] = 5
				self.players[(self.dealer + 2) % 4].set_stack(self.players[(self.dealer + 2) % 4].get_stack() - 10)
				self.round_bets[(self.dealer + 1) % 4] = 10

				self.stacks = [self.players.get_stack() for _ in range(4)]
				#now reflect those changes in the gamestate
				lock.aquire()
				self.game_state.set_round_pot(self.pot, self.db)
				self.set_player_stacks(self.stacks)
				lock.release()

				while not all_called:
					#get the decision from the current player

					#if it is an AI turn
					if self.players[self.current].is_computer_player():
						#give the player's turn() function the community cards and it will return a decision
						choice, value = self.players[self.current].turn(self.community_cards)
						#if the AI decides to bet
						if choice == 'bet':
							#compute the amount of money this player is putting into the pot:
							#	The value is the amount over the minimum call that the player is putting into the pot
							#	To compute the total amount you just take the total_call minus the amount the player has
							#	already bet that round. Then you add the bet value.
							bet_amount = ((self.total_call - self.round_bets[self.current]) + value)
							#pot goes up by bet amount
							self.pot += bet_amount
							#total_call goes up by the bet value
							self.total_call += value
							#add the bet_amount to the round_bets for the current player
							self.round_bets[self.current] += bet_amount
							#subtract that amount from the player's stack
							self.players[self.current].set_stack(self.player[self.current].get_stack - bet_amount)
							#update local stacks
							self.stacks[self.current] = self.players[self.current].get_stack()
							#now reflect those changes in the gamestate
							lock.aquire()
							self.set_player_stacks(self.stacks)
							self.game_state.set_round_pot(self.game_state.get_round_pot(self.db) + bet_amount, self.db)
							self.game_state.set_bet(value, self.db)
							self.game_state.set_total_call(self.game_state.get_total_call() + value, self.db)
							self.game_state.set_player_decision(choice, self.db)
							self.game_state.increment_whose_turn()
							lock.release()
						
						#if the AI decides to check
						elif choice == 'check':
							#basically just skipping their turn
							#reflect in game state
							lock.aquire()
							self.game_state.set_player_decision(choice, self.db)
							self.game_state.increment_whose_turn()
							lock.release()
						
						#if AI decides to fold
						elif choice == 'fold':
							#remove their index from actives[]
							self.actives.remove(self.current)
							#tell gamestate
							lock.aquire()
							self.game_state.remove_player(self.current, self.db)
							lock.release()

						# if AI decides to call
						elif choice == 'call':
							# add to the pot the call amount (based on the amount below the total_call the current player
							# has already bet in round_bets)
							self.pot += (self.total_call - self.round_bets[self.current])
							#reflect that in the player's stack
							self.players[self.current].set_stack(self.player[self.current].get_stack - (self.total_call - self.round_bets[self.current]))
							#set that players round_bets to the call value
							self.round_bets[self.current] = self.total_call
							#update local stacks with the new player stack
							self.stacks[self.current] = self.players[self.current].get_stack()
							#reflect the changes in the gamestate
							lock.aquire()
							self.set_player_stacks(self.stacks)
							self.game_state.set_round_pot(self.game_state.get_round_pot(self.db) + value, self.db)
							self.game_state.set_bet(value, self.db)
							self.game_state.set_total_call(self.game_state.get_total_call() + value, self.db)
							self.game_state.set_player_decision(choice, self.db)
							self.game_state.increment_whose_turn()
							lock.release()

					if self.current == self.me:
						#It's my turn! This turn happens in the graphics window.
						#This will be the same as the turn in guest_main()
						
						#graphics will constantly check local gamestate for whose_turn
						#when it is the local players turn, graphics will prompt/allow input for that turn
						#that turn info will then be put into the local gamestate as the decision, and then flips the waiting
						#boolean

						#host_main then procedes as if it was a normal turn, and then uploads the game state
						pass
					
					if (self.current is not self.me) and (not self.players[self.current].is_computer_player()):
						#it is a guest players turn
						#we need to wait and let them update the gamestate
						#once they have updated the game state, we update the local game and then move on
						lock.aquire()
						while self.game_state.get_waiting():
							#if the host is waiting, just keep checking until the turn has been taken
							time.sleep(3)
						lock.release()
						# once the player takes their turn we just get the decision and then use the same logic from the AI
						# player turn

						choice, value = self.game_state.get_player_decision(self.db)
						#if bet
						if choice == 'bet':
							#compute the amount of money this player is putting into the pot:
							#	The value is the amount over the minimum call that the player is putting into the pot
							#	To compute the total amount you just take the total_call minus the amount the player has
							#	already bet that round. Then you add the bet value.
							bet_amount = ((self.total_call - self.round_bets[self.current]) + value)
							#pot goes up by bet amount
							self.pot += bet_amount
							#total_call goes up by the bet value
							self.total_call += value
							#add the bet_amount to the round_bets for the current player
							self.round_bets[self.current] += bet_amount
							#subtract that amount from the player's stack
							self.players[self.current].set_stack(self.player[self.current].get_stack - bet_amount)
							#update local stacks
							self.stacks[self.current] = self.players[self.current].get_stack()
							#now reflect those changes in the gamestate
							lock.aquire()
							self.set_player_stacks(self.stacks)
							self.game_state.set_round_pot(self.game_state.get_round_pot(self.db) + bet_amount, self.db)
							self.game_state.set_bet(value, self.db)
							self.game_state.set_total_call(self.game_state.get_total_call() + value, self.db)
							self.game_state.set_player_decision(choice, self.db)
							self.game_state.increment_whose_turn()
							lock.release()
						
						#if check
						elif choice == 'check':
							#basically just skipping their turn
							#reflect in game state
							lock.aquire()
							self.game_state.set_player_decision(choice, self.db)
							self.game_state.increment_whose_turn()
							lock.release()
						
						#if fold
						elif choice == 'fold':
							#remove their index from actives[]
							self.actives.remove(self.current)
							#tell gamestate
							lock.aquire()
							self.game_state.remove_player(self.current, self.db)
							lock.release()

						# if call
						elif choice == 'call':
							# add to the pot the call amount (based on the amount below the total_call the current player
							# has already bet in round_bets)
							self.pot += (self.total_call - self.round_bets[self.current])
							#reflect that in the player's stack
							self.players[self.current].set_stack(self.player[self.current].get_stack - (self.total_call - self.round_bets[self.current]))
							#set that players round_bets to the call value
							self.round_bets[self.current] = self.total_call
							#update local stacks with the new player stack
							self.stacks[self.current] = self.players[self.current].get_stack()
							#reflect the changes in the gamestate
							lock.aquire()
							self.set_player_stacks(self.stacks)
							self.game_state.set_round_pot(self.game_state.get_round_pot(self.db) + value, self.db)
							self.game_state.set_bet(value, self.db)
							self.game_state.set_total_call(self.game_state.get_total_call() + value, self.db)
							self.game_state.set_player_decision(choice, self.db)
							self.game_state.increment_whose_turn()
							lock.release()

					#increment current player based on actives[]
					self.current += 1
					while self.current not in self.actives:
						self.current += 1
						self.current = self.current % 4
					
					#if at any point only one player is active
					if len(self.actives) == 1:
						#everyone else folded and the last one is the winner
						#award the pot to the winner
						self.players[self.actives[0]].set_stack(self.players[self.actives[0]].get_stack() + self.pot)
						self.stacks[self.actives[0]] = self.players[self.actives[0]].get_stack()
						#reset the game to dealing values
						self.round_bets = [0, 0, 0, 0]
						self.actives = [1, 2, 3, 4] #NOTE: THIS IS A PLACEHOLDER AND WILL NOT WORK AFTER SOMEONE 
													# HAS BUSTED OUT OF THE GAME
						self.pot = 0
						lock.aquire()
						self.set_player_stacks(self.stacks)
						self.game_state.set_total_pot(0, self.db)
						self.game_state.set_round('dealing', self.db)
						lock.release()
					
					#if at any point all the round bets of the active players are all equal then everyone has called
					all_called = True
					active_bets = []
					for i in self.actives:
						active_bets.append(self.round_bets[i])
					for i in range(len(active_bets)):
						if active_bets[i] is not active_bets[(i + 1) % len(active_bets)]:
							all_called == False

					if all_called:
						#merge round pot and total pot
						#also deal more cards
						#also change round
						lock.aquire()
						self.game_state.set_total_pot(self.game_state.get_total_pot() + self.game_state.get_round_pot())
						if self.game_state.get_round() == 'pre-flop':
							self.game_state.set_round('flop', self.db)
							self.community_cards = self.deck.flop()
							self.game_state.set_community_cards(self.community_cards, self.db)
						elif self.game_state.get_round() == 'flop':
							self.game_state.set_round('turn', self.db)
							self.community_cards.append(self.deck.turn())
							self.game_state.set_community_cards(self.community_cards, self.db)
						elif self.game_state.get_round() == 'turn':
							self.game_state.set_round('river', self.db)
							self.community_cards.append(self.deck.turn())
							self.game_state.set_community_cards(self.community_cards, self.db)
						elif self.game_state.get_round() == 'river':
							self.game_state.set_round('showdown', self.db)
						lock.release()

						#reset betting/round values
						self.current = (self.dealer + 3) % 4
						self.total_call = 10
						self.round_bets = [0, 0, 0, 0]

			if self.game_state.get_round() == 'showdown':
				#award winner
				self.players[self.actives[0]].set_stack(self.players[self.actives[0]].get_stack() + self.pot)
				#reset values
				#change the round
				lock.aquire()
				self.game_state.set_player_stacks(self.stacks, self.db)
				self.game_state.set_round('dealing', self.db)
				self.game_state.set_total_pot(0, self.db)
				self.game_state.set_round_pot(0, self.db)
				self.game_state.set_player_hands([player.get_hand() for player in self.players], self.db)
				lock.release()
				self.pot = 0
				self.dealer += 1
				self.current = (self.dealer + 3) % 4
				self.total_call = 10
				self.round_bets = [0, 0, 0, 0]
				self.actives = [0, 1, 2, 3]
			
			num_busts = 0
			for stack in self.stacks:
				if stack == 0:
					num_busts += 1
			
			if num_busts == 3:
				playing = False
		
		#Need some game over screen here.
			
	def guest_main(self, lock):
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

			#once connected, the game takes place entirely in the graphics window.
	
	def find_best_hand():
		#calls each player's evaluate_hand() and determines the winner. If there is a tie, it can 
		#systematically search through individual hands for the highest card.
		pass

	def upload_turn(): #guess uploads turn
		pass

	def fetch_turn(player_index): # host fetches guest turn and updates game state
		pass
