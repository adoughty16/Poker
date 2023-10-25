from enum import Enum
from cards import Card 
from firebase_admin import firestore 
''' 
Game State class to keep track of game information in the data base (to allow multi-player)
takes in a document name and database connection to create the object!! 
every getter and setter interfaces with the database (to avoid conflicting information)
'''

'''
What needs doing:
- test the community card and hand functions after implementing to_dict and from_dict in Card
- test all functions getters and setters 
'''

round = Enum('round', ['dealing','pre-flop','flop','turn','river','showdown'])
play = Enum('play', ['bet', 'check', 'fold', 'call'])

class Game_state:
    def __init__(self, db, doc_name, dictionary = {}):
        #populate variables
        self.player_names = []
        # added player hands to be set and "got" only in showdown (for built-in security)
        self.player_hands = []
        # store card objects (?)
        self.community_cards = []
        # to bet updated each time
        self.total_pot = 0
        self.round_pot = 0

        #to keep track of how much money everyone has (for drawing)
        self.player_stacks = [1000, 1000, 1000, 1000]
        # to keep track of the total per-person call amount per round
        self.total_call = 0
        # waiting is a flag set by host to indicate that a guest turn is being waited on
        self.waiting = False
        # whose turn is to keep track of which player is expected to upload turn info needs setter/getter
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

        # selected_host and selected_players for graphics
        self.selected_host = True 
        self.selected_players = 1 

        for key in dictionary:
            setattr(self ,key , dictionary[key])

        self.doc_name = doc_name

        # create a document in the database for the game's gamestate
        # ultimately, we decided to make one document and update it as needed to theoretically support multiple games at once
        # NOTE: player_hands and comunity_cards means that the card class with need a to_dict and from_dict 

        data = {"player_names": self.player_names, "player_hands": self.player_hands, "community_cards": self.community_cards, 
        "total_pot": self.total_pot, "round_pot": self.round_pot, "player_stacks": self.player_stacks, "total_call": self.total_call, 
        "waiting": self.waiting, "whose_turn": self.whose_turn, "bet": self.bet, "minimum_call": self.minimum_call, 
        "dealer": self.dealer, "actives": self.actives, "round": self.round, "player_decision": self.player_decision}
        game_state_ref = db.collection("states").document(self.doc_name).set(data)

    #def from_dict(source):
     #   return Game_state(source["player_names"], source["player_hands"], source["community_cards"], source["total_pot"], source["round_pot"], 
      #             source["player_stacks"], source["total_call"], source["waiting"], source["whose_turn"], source["bet"], source["minimum_call"], 
       #            source["dealer"], source["actives"], source["round"], source["player_decision"])
    
    def to_dict(self):
        return {"player_names": self.player_names, "player_hand": self.player_hands, "community_cards": self.community_cards, "total_pot": self.total_pot, 
                "round_pot": self.round_pot, "player_stacks": self.player_stacks, "total_call": self.total_call, "waiting": self.waiting, "whose_turn": self.whose_turn, 
                "bet": self.bet, "minimum_call": self.minimum_call, "dealer": self.dealer, "actives": self.actives, "round": self.round, "player_decision": self.player_decision}

    def set_players(self, players, db):
        for player in players:
            self.players.append(player.name)
        game_state_ref = db.collection("states").document(self.doc_name)
        game_state_ref.update({"player_names": self.players})

    # rather than appending this will just take a new array of cards and set that in the database
    def set_community_cards(self, community_cards, db):
        self.clear_community_cards(self, db)
        game_state_ref = db.collection("states").document(self.doc_name)
        for card in community_cards:
            self.community_cards.append(card)
            game_state_ref.update({"community_cards": firestore.ArrayUnion(Card.to_dict(card))})

    def clear_community_cards(self, db):
        game_state_ref = db.collection("states").document(self.doc_name)
        for card in self.community_cards:
            game_state_ref.update({"community_cards": firestore.ArrayRemove(Card.to_dict(card))})
            self.community_cards.remove(card)
        
    # function add a singular community card in turn and river 
    def add_community_card(self, card, db):
        self.community_cards.append(card)
        game_state_ref = db.collection("states").document(self.doc_name)
        game_state_ref.update({"community_cards": firestore.ArrayUnion(Card.to_dict(card))})

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
        game_state_ref.update({"dealer": self.dealer})

    def update_dealer(self, db):
        # dealer is the index of the dealer
        # use this index and add (and mod) to get other players such as blind and double_blind
        self.dealer += 1
        self.dealer = self.dealer % 4
        game_state_ref = db.collection("states").document(self.doc_name)
        game_state_ref.update({"dealer": self.dealer})

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
        game_state_ref.update({"round": self.round})
    
    def set_player_stacks(self, player_stacks, db):
        self.player_stacks = player_stacks 
        game_state_ref = db.collection("states").document(self.doc_name)
        game_state_ref.update({"player_stacks": self.player_stacks})

    def set_total_call(self, total_call, db):
        self.total_call = total_call
        game_state_ref = db.collection("states").document(self.doc_name)
        game_state_ref.update({"total_call": self.total_call})
    
    def set_waiting(self, waiting, db):
        self.waiting = waiting
        game_state_ref = db.collection("states").document(self.doc_name)
        game_state_ref.update({"waiting": self.waiting})
    
    def flip_waiting(self, db):
        if self.waiting == True:
            self.waiting = False
        else:
            self.waiting = True
        game_state_ref = db.collection("states").document(self.doc_name)
        game_state_ref.update({"waiting": self.waiting})
    
    def increment_whose_turn(self, db):
        self.whose_turn += 1
        while self.whose_turn not in self.actives:
            self.whose_turn += 1
            self.whose_turn = self.whose_turn % 4
        game_state_ref = db.collection("states").document(self.doc_name)
        game_state_ref.update({"whose_turn": self.whose_turn})
    
    # get/set the selected host and selected players from graphics

    def set_selected_host(self, selected_host):
        self.selected_host = selected_host 

    def set_selected_players(self, selected_players):
        self.selected_players = selected_players
        
# getters 
    def get_selected_host(self):
        return self.selected_host 

    def get_selected_players(self):
        return self.selected_players
    
    def get_players(self, db):
        game_state_ref = db.collection("states").document(self.doc_name)
        doc = game_state_ref.get()
        return doc.to_dict()["player_names"]

    # going to need some interfacing with the cards class
    # since these are custom objects, a to_dict and from_dict may be necessary 
    # it is also an array of 3 - 5 of these custom objects 
    def get_community_cards(self, db):
        game_state_ref = db.collection("states").document(self.doc_name)
        doc = game_state_ref.get()
        comm_cards = []
        for comm_card in doc.community_cards:
            comm_cards.append(Card.from_dict(comm_card))
        return comm_cards 
    
    def get_total_pot(self, db):
        game_state_ref = db.collection("states").document(self.doc_name)
        doc = game_state_ref.get()
        return doc.to_dict()["total_pot"]
    
    def get_round_pot(self, db):
        game_state_ref = db.collection("states").document(self.doc_name)
        doc = game_state_ref.get()
        return doc.to_dict()["round_pot"]

    def get_bet(self, db):
        game_state_ref = db.collection("states").document(self.doc_name)
        doc = game_state_ref.get()
        return doc.to_dict()["bet"]
    
    def get_minimum_call(self, db):
        game_state_ref = db.collection("states").document(self.doc_name)
        doc = game_state_ref.get()
        return doc.to_dict()["minimum_call"]

    # get_player_decision returns the enumerated type of the decision AND the value of that decision (0 unless bet) 
    def get_player_decision(self, db): 
        game_state_ref = db.collection("states").document(self.doc_name)
        doc = game_state_ref.get()
        if doc.to_dict()["player_decision"] == 'bet':
            bet_value = 1
        else:
            bet_value = self.get_bet(db)
        return doc.to_dict()["player_decision"], bet_value 

    def get_bet(self, db):
        game_state_ref = db.collection("states").document(self.doc_name)
        doc = game_state_ref.get()
        return doc.to_dict()["bet"]

    def get_dealer(self, db):
        game_state_ref = db.collection("states").document(self.doc_name)
        doc = game_state_ref.get()
        return doc.to_dict()["dealer"]

    def get_actives(self, db):
        game_state_ref = db.collection("states").document(self.doc_name)
        doc = game_state_ref.get()
        return doc.to_dict()["actives"]

    def get_round(self, db):
       game_state_ref = db.collection("states").document(self.doc_name)
       doc = game_state_ref.get()
       return doc.to_dict()["round"]

    def get_total_call(self, db):
        game_state_ref = db.collection("states").document(self.doc_name)
        doc = game_state_ref.get()
        return doc.to_dict()["total_call"]

    
    def get_player_stacks(self, db):
        game_state_ref = db.collection("states").document(self.doc_name) 
        doc = game_state_ref.get()
        return doc.to_dict()["player_stacks"]
    
    def get_waiting(self, db):
        game_state_ref = db.collection("states").document(self.doc_name)
        doc = game_state_ref.get()
        return doc.to_dict()["waiting"]

    def get_whose_turn(self, db):
        game_state_ref = db.collection("states").document(self.doc_name)
        doc = game_state_ref.get()
        return doc.to_dict()["whose_turn"]
    
    # this also may need some help from cards class as it will be an array of arrays of card objects 
    def get_player_hands(self, db):
        game_state_ref = db.collection("states").document(self.doc_name)
        doc = game_state_ref.get()
        player_hands = []
        for hand in doc.player_hands:
            player_hands.append(Card.from_dict(hand))
        return player_hands 
