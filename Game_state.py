from enum import Enum

''' 
Game State class to keep track of game information in the data base (to allow multi-player)
takes in a document name and database connection to create the object!! 
every getter and setter interfaces with the database (to avoid conflicting information)
'''
"""
pre-flop:After the Dealer has passed out two cards to everyone, 
the player clockwise to the Right Blind has the option to fold, 
call or raise the previous bet. Play then proceeds clockwise 
around the table.

flop:At the start of the Flop round, the Dealer places three community 
cards upright in the middle of the table. Normal play then proceeds 
starting with the player clockwise from the Dealer.

turn:At the start of the Turn Round, or Fourth Street, the Dealer places 
a fourth card in the community.

river:At the start of the River Round, the Dealer places a fifth 
and final card in the community. (this reuses turn())

showdown: If there are still players in the game after the River Round, 
players must over turn their cards for 
all to see with the highest hand taking the pot.

source: https://playingcarddecks.com/blogs/how-to-play/texas-holdem-game-rules
"""
round = Enum('round', ['dealing','pre-flop','flop','turn','river','showdown'])
play = Enum('play', ['bet', 'check', 'fold', 'call'])

class Game_state:
    def __init__(self, db, doc_name):
        #populate variables
        self.player_names = []
        # added player hands to be set and "got" only in showdown (for built-in security)
        self.player_hands = []
        # store card objects (?)
        self.community_cards = []
        # to bet updated each time
        self.total_pot = 0
        self.round_pot = 0

        #
        #to keep track of how much money everyone has (for drawing)
        # needs setters/getters
        #
        self.player_stacks = [1000, 1000, 1000, 1000]

        #
        # to keep track of the total per-person call amount per round
        #
        self.total_call = 0

        #
        # waiting is a flag set by host to indicate that a guest turn is being waited on
        # it needs a flip_waiting() function for guest/host to call that flips the boolean value
        # also needs a getter for the host/guest to check for
        #
        # whose turn is to keep track of which player is expected to upload turn info needs setter/getter
        #
        self.waiting = False
        self.whose_turn = 0

        # hard code first blind to be 10
        self.bet = 10
        # the current amount needed for a call (For graphics, check is only an option if this value is zero)
        self.minimum_call = 10 
        # index of the dealer
        self.dealer = 0
        # players left: array of int indexes (important for showdown round)
        self.actives = [0, 1, 2, 3]
        #first round is dealing
        self.round = 'dealing'
        self.player_decision = 'check'

        self.doc_name = doc_name

        # create a document in the database for the game's gamestate
        # ultimately, we decided to make one document and update it as needed to theoretically support multiple games at once
        # NOTE: player_hands and comunity_cards means that the card class with need a to_dict and from_dict 
        data = {"player_names": self.player_names, "player_hands": self.player_hands, "community_cards": self.community_cards, 
        "total_pot": self.total_pot, "round_pot": self.round_pot, "bet": self.bet, "minimum_call": self.minimum_call, "dealer": self.dealer,
        "actives": self.actives, "round": self.round, "player_decision": self.player_decision}
        game_state_ref = db.collection("states").document(self.doc_name).set(data)


    def set_players(self, players, db):
        for player in players:
            self.players.append(player.name)
        game_state_ref = db.collection("states").document(self.doc_name)
        game_state_ref.udpate({"player_names": self.players})

    # rather than appending this will just take a new array of cards and set that in the database
    def set_community_cards(self, community_cards, db):
        self.community_cards = community_cards 
        # can firebase store an array of custom object types?!
        game_state_ref = db.collection("states").document(self.doc_name)
        game_state_ref.update({"community_cards": self.community_cards})
    
    # function add a singular community card in turn and river 
    def add_community_card(self, card, db):
        self.community_cards.append(card)
        game_state_ref = db.collection("states").document(self.doc_name)
        game_state_ref.udpate({"community_cards": self.community_cards})

    # adds a community card in turn and river 
    def add_community_card(self, community_card, db):
        self.community_cards.append(community_card)
        game_state_ref = db.collection("states").document(self.doc_name)
        game_state_ref.udpate({"community_cards": self.community_cards})

    # function only to be used during showdown
    def set_player_hands(self, player_hands, db):
        self.player_hands = player_hands 
        game_state_ref = db.collection("states").document(self.doc_name)
        game_state_ref.update({"player_hands": self.player_hands})
    
    def set_total_pot(self, pot, db):
        self.total_pot = pot
        game_state_ref = db.collection("states").document(self.doc_name)
        game_state_ref.update({"total_pot": self.total_pot})
    
    def set_round_pot(self, round_pot, db):
        self.round_pot = round_pot
        game_state_ref = db.collection("states").document(self.doc_name)
        game_state_ref.update({"round_pot": self.round_pot})

    def set_bet(self, new_bet, db):
        # wherever this is called, only call if new_bet > bet
        self.bet = new_bet
        game_state_ref = db.collection("states").document(self.doc_name)
        game_state_ref.update({"bet": self.bet})
    
    def set_minimum_call(self, minimum_call, db):
        self.minimum_call = minimum_call
        game_state_ref = db.collection("states").document(self.doc_name)
        game_state_ref.update({"minimum_call": self.minimum_call})

    def set_player_decision(self, player_decision, db):
        self.player_decision = player_decision
        game_state_ref = db.collection("states").document(self.doc_name)
        game_state_ref.update({"player_decision": self.player_decision})

    def set_dealer(self, dealer, db):
        # dealer is the index of the dealer
        self.dealer = dealer
        game_state_ref = db.collection("states").document(self.doc_name)
        game_state_ref.udpate({"dealer": self.dealer})

    def update_dealer(self, db):
        # dealer is the index of the dealer
        # use this index and add (and mod) to get other players such as blind and double_blind
        self.dealer += 1
        self.dealer = self.dealer % 4
        game_state_ref = db.collection("states").document(self.doc_name)
        game_state_ref.udpate({"dealer": self.dealer})

    # set_actives is really just removing anyone who folds
    def remove_player(self, player_index, db):
        self.actives.remove(player_index)
        game_state_ref = db.collection("states").document(self.doc_name)
        game_state_ref.update({"actives": self.actives})

    def set_round(self, round, db):
        # updates the enumerated type for round after the right number of turns have passed (depending on len(actives))
        # do we need to check that this is "next in line"?
        self.round = round
        game_state_ref = db.collection("states").document(self.doc_name)
        game_state_ref.udpate({"round": self.round})
    
    def set_player_stacks(self, player_stacks, db):
        self.player_stacks = player_stacks 
        game_state_ref = db.collection("states").document(self.doc_name)
        game_state_ref.udpate({"player_stacks": self.player_stacks})

    def set_total_call(self, total_call, db):
        self.total_call = total_call
        game_state_ref = db.collection("states").document(self.doc_name)
        game_state_ref.udpate({"total_call": self.total_call})
    
    def set_waiting(self, waiting, db):
        self.waiting = waiting
        game_state_ref = db.collection("states").document(self.doc_name)
        game_state_ref.udpate({"waiting": self.waiting})
    
    def increment_whose_turn(self, db):
        self.whose_turn += 1
        while self.whose_turn not in self.actives:
            self.whose_turn += 1
            self.whose_turn = self.whose_turn % 4
        game_state_ref = db.collection("states").document(self.doc_name)
        game_state_ref.update({"whose_turn": self.whose_turn})
    
# getters 
    def get_players(self, db):
        game_state_ref = db.collection("states").document(self.doc_name)
        doc = game_state_ref.get()
        return doc.players

    # going to need some interfacing with the cards class
    # since these are custom objects, a to_dict and from_dict may be necessary 
    # it is also an array of 3 - 5 of these custom objects 
    def get_community_cards(self, db):
        game_state_ref = db.collection("states").document(self.doc_name)
        doc = game_state_ref.get()
        return doc.community_cards
    
    def get_total_pot(self, db):
        game_state_ref = db.collection("states").document(self.doc_name)
        doc = game_state_ref.get()
        return doc.total_pot 
    
    def get_round_pot(self, db):
        game_state_ref = db.collection("states").document(self.doc_name)
        doc = game_state_ref.get()
        return doc.round_pot

    def get_bet(self, db):
        game_state_ref = db.collection("states").document(self.doc_name)
        doc = game_state_ref.get()
        return doc.bet 
    
    def get_minimum_call(self, db):
        game_state_ref = db.collection("states").document(self.doc_name)
        doc = game_state_ref.get()
        return doc.minimum_call 

    # get_player_decision returns the enumerated type of the decision AND the value of that decision (0 unless bet) 
    def get_player_decision(self, db): 
        game_state_ref = db.collection("states").document(self.doc_name)
        doc = game_state_ref.get()
        if doc.player_decision == 'bet':
            bet_value = 1
        else:
            bet_value = self.get_bet()
        return doc.player_decision, bet_value 

    def get_bet(self, db):
        game_state_ref = db.collection("states").document(self.doc_name)
        doc = game_state_ref.get()
        return doc.bet 

    def get_dealer(self, db):
        game_state_ref = db.collection("states").document(self.doc_name)
        doc = game_state_ref.get()
        return doc.dealer

    def get_actives(self, db):
        game_state_ref = db.collection("states").document(self.doc_name)
        doc = game_state_ref.get()
        return doc.actives

    def get_round(self, db):
       game_state_ref = db.collection("states").document(self.doc_name)
       doc = game_state_ref.get()
       return doc.round

    def get_total_call(self, db):
        game_state_ref = db.collection("states").document(self.doc_name)
        doc = game_state_ref.get()
        return doc.total_call 
    
    def get_player_stacks(self, db):
        game_state_ref = db.collection("states").document(self.doc_name) 
        doc = game_state_ref.get()
        return doc.player_stacks
    
    def get_waiting(self, db):
        game_state_ref = db.collection("states").document(self.doc_name)
        doc = game_state_ref.get()
        return doc.waiting 

    def get_whose_turn(self, db):
        game_state_ref = db.collection("states").document(self.doc_name)
        doc = game_state_ref.get()
        return doc.whose_turn 
    
    # this also may need some help from cards class as it will be an array of arrays of card objects 
    def get_player_hands(self, db):
        game_state_ref = db.collection("states").document(self.doc_name)
        doc = game_state_ref.get()
        return doc.player_hands 

# other funcitons 
    # i'm confused by what the difference between upload and upload_turn are - this is only called once (so far) in the game loop
    # i didn't think we would need to store player decisions or anything like that and could just update whatever attribute specifically changed in the game loop 
    def upload(self, db): #uploads game_state to db
        pass
    
    def upload_turn():
        #data = {"players": players, "community_cards": community_cards, "pot": self.pot, "bet": self.bet , "dealer": , "actives": , "round": }
        #db.collection("").document("").set(data)
        pass

    # this will be the parser where we reset everything? 
    def fetch_turn(player):
        pass