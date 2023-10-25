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
		self.community_cards = []
		self.players = [Player() for _ in range(num_players)]
		self.deck = deck()
		self.pot = 0
		self.dealer = 0
		self.current = 3
		self.total_call = 10
		self.round_bets = [0, 0, 0, 0]
		self.me = 0
		self.host = host
		self.db = db
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

			if self.game_state.get_round() == 'pre-flop' or 'flop' or 'turn' or 'river':
				all_called = False
				#establish dealer/blinds
				self.pot += 15
				self.players[(self.dealer + 1) % 4].set_stack(self.players[(self.dealer + 1) % 4].get_stack() - 5)
				self.round_bets[(self.dealer + 1) % 4] = 5
				self.players[(self.dealer + 2) % 4].set_stack(self.players[(self.dealer + 2) % 4].get_stack() - 10)
				self.round_bets[(self.dealer + 1) % 4] = 10

				self.stacks = [self.players.get_stack() for _ in range(4)]
				lock.aquire()
				self.game_state.set_round_pot(self.pot, self.db)
				self.set_player_stacks(self.stacks)
				lock.release()

				while not all_called:
					#get the decision from the current player

					#if it is an AI turn
					if self.players[self.current].is_computer_player():
						choice, value = self.players[self.current].turn(self.community_cards)
						if choice == 'bet':
							self.pot += value
							self.total_call += value
							self.round_bets[self.current] += value
							self.players[self.current].set_stack(self.player[self.current].get_stack - value)
							self.stacks[self.current] = self.players[self.current].get_stack()
							lock.aquire()
							self.set_player_stacks(self.stacks)
							self.game_state.set_round_pot(self.game_state.get_round_pot(self.db) + value, self.db)
							self.game_state.set_bet(value, self.db)
							self.game_state.set_total_call(self.game_state.get_total_call() + value, self.db)
							self.game_state.set_player_decision(choice, self.db)
							self.game_state.increment_whose_turn()
							lock.release()

						elif choice == 'check':
							lock.aquire()
							self.game_state.set_player_decision(choice, self.db)
							self.game_state.increment_whose_turn()
							lock.release()
							
						elif choice == 'fold':
							self.actives.remove(self.current)
							lock.aquire()
							self.game_state.remove_player(self.current, self.db)
							lock.release()

						elif choice == 'call':
							self.pot += (self.total_call - self.round_bets[self.current])
							self.players[self.current].set_stack(self.player[self.current].get_stack - (self.total_call - self.round_bets[self.current]))
							self.round_bets[self.current] = self.total_call
							self.stacks[self.current] = self.players[self.current].get_stack()
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
						if choice == 'bet':
							self.pot += value
							self.total_call += value
							self.round_bets[self.current] += value
							self.players[self.current].set_stack(self.player[self.current].get_stack - value)
							self.stacks[self.current] = self.players[self.current].get_stack()
							lock.aquire()
							self.set_player_stacks(self.stacks)
							self.game_state.set_round_pot(self.game_state.get_round_pot(self.db) + value, self.db)
							self.game_state.set_bet(value, self.db)
							self.game_state.set_total_call(self.game_state.get_total_call() + value, self.db)
							self.game_state.set_player_decision(choice, self.db)
							self.game_state.increment_whose_turn()
							lock.release()

						elif choice == 'check':
							lock.aquire()
							self.game_state.set_player_decision(choice, self.db)
							self.game_state.increment_whose_turn()
							lock.release()
							
						elif choice == 'fold':
							self.actives.remove(self.current)
							lock.aquire()
							self.game_state.remove_player(self.current, self.db)
							lock.release()

						elif choice == 'call':
							self.pot += (self.total_call - self.round_bets[self.current])
							self.players[self.current].set_stack(self.player[self.current].get_stack - (self.total_call - self.round_bets[self.current]))
							self.round_bets[self.current] = self.total_call
							self.stacks[self.current] = self.players[self.current].get_stack()
							lock.aquire()
							self.set_player_stacks(self.stacks)
							self.game_state.set_round_pot(self.game_state.get_round_pot(self.db) + value, self.db)
							self.game_state.set_bet(value, self.db)
							self.game_state.set_total_call(self.game_state.get_total_call() + value, self.db)
							self.game_state.set_player_decision(choice, self.db)
							self.game_state.increment_whose_turn()
							lock.release()
						lock.release()

					#change current player
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
