from enum import Enum
from db_connect import db 

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
round = Enum('dealing','pre-flop','flop','turn','river','showdown')
play = Enum('bet', 'check', 'fold', 'call')

class Game_state:
    def __init__(self):
        #populate variables
        self.player_names = []
        # added player hands to be set and "got" only in showdown (for built-in security)
        self.player_hands = []
        # store card objects (?)
        self.community_cards = []
        # to bet updated each time
        self.total_pot = 0
        self.round_pot = 0 
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

        # create a document in the database for the game's gamestate
        # ultimately, we decided to make one document and update it as needed to theoretically support multiple games at once
        # NOTE: player_hands and comunity_cards means that the card class with need a to_dict and from_dict 
        data = {"player_names": self.player_names, "player_hands": self.player_hands, "community_cards": self.community_cards, 
        "total_pot": total_pot, "round_pot": round_pot, "bet": self.bet, "minimum_call": self.minimum_call, "dealer": self.dealer,
        "actives": self.actives, "round": self.round, "player_decision": self.player_decision}
        game_state_ref = db.collection("states").add(data)


    def set_players(self, players):
        for player in players:
            self.players.append(player.name)
        game_state_ref.udpate({"player_names": self.players})

    # takes in community cards and sets them for flop
    def set_community_cards(self, community_cards):
        # add to the community cards
        # self.community_cards.append()
        # based on where these are decided, maybe add makes more sense and call twice in flop
        for card in community_cards:
            self.community_cards.append(card)
        # NOTE: can firebase store an array of custom object types? 
        game_state_ref.update("community_cards": self.community_cards)
    
    # adds a community card in turn and river 
    def add_community_card(self, community_card):
        self.community_cards.append(community_card)
        game_state_ref.udpate("community_cards": self.community_cards)

    # function only to be used during showdown
    def set_player_hands(self, player_hands):
        for player in self.players:
            self.player_hands.append(player.hand)
        game_state_ref.update("player_hands": self.player_hands)
    
    def set_total_pot(self, pot):
        self.total_pot = pot
        game_state_ref.update({"total_pot": self.total_pot})
    
    def set_round_pot(self, round_pot)
        self.round_pot = round_pot
        game_state_ref.update({"round_pot": self.round_pot})

    def set_bet(self, new_bet):
        # wherever this is called, only call if new_bet > bet
        self.bet = new_bet
        game_state_ref.update({"bet": self.bet})
    
    def set_minimum_call(self, minimum_call):
        self.minimum_call = minimum_call
        game_state_ref.update({"minimum_call": self.minimum_call})

    def set_player_decision(self, player_decision):
        self.player_decision = player_decision
        game_state_ref.update({"player_decision": self.player_decision})

    def set_dealer(self, dealer):
        # dealer is the index of the dealer
        self.dealer = dealer
        game_state_ref.udpate({"dealer": self.dealer})

    def update_dealer(self):
        # dealer is the index of the dealer
        # use this index and add (and mod) to get other players such as blind and double_blind
        self.dealer += 1
        self.dealer % 4
        game_state_ref.udpate({"dealer": self.dealer})

    # set_actives is really just removing anyone who folds
    def remove_player(self, player):
        self.actives.remove(player.name)
        game_state_ref.update({"actives": self.actives})

    def set_round(self, round):
        # updates the enumerated type for round after the right number of turns have passed (depending on len(actives))
        # do we need to check that this is "next in line"?
        self.round = round
        game_state_ref.udpate({"round": self.round})

# getters 
    def get_players(self):
        doc = game_state_ref.get()
        return doc.players

    def get_community_cards(self):
        return self.community_cards
    
    def get_total_pot(self):
        return self.total_pot 
    
    def get_round_pot(self)
        return self.round_pot

    def get_bet(self):
        # wherever this is called, only call if new_bet > bet
        return self.bet 
    
    def get_minimum_call(self):
        return self.minimum_call 

    def get_player_decision(self):
        return self.player_decision

    def get_bet(self):
        return self.bet 

    def get_dealer(self):
        # dealer is the index of the dealer
        # use this index and add (and mod) to get other players such as blind and double_blind
        return self.dealer

    # set_actives is really just removing anyone who folds
    def get_actives(self):
        return self.actives

    def get_round(self):
       return self.round

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

# an attempt at testing the database and game state classes 
def main():
    game_state = Game_state()
    print(game_state.get_actives)
    game_state.set_total_pot(100)
    print(game_state.get_total_pot)

main()