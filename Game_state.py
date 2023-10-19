from enum import Enum


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
game_state = Enum('game_state',['dealing','pre-flop','flop','turn','river','showdown'])

class Game_state:
    
    #players: list of strings (need their hands at the end)
    #should we consider dict?
    players=[]

    community_cards=[]

    pot=0

    minimum_bet=10

    #dealer: index integer of players (list of strings)
    dealer=[]

    #active players: list of indexes of players (list of strings)
    active_players=[]

    #where should we track who is the dealer, blind, and double blind?

    #ANSWER/IDEA: dealer can maybe just be an integer mod 4 that keeps track of their index in the player list?
    #blind is the next player after the dealer
    #double blind is the next player after that

    def __init__(self):
        #populate variables
        self.players = []
        # store card objects (?)
        self.community_cards = []
        # to bet updated each time
        self.pot = 0
        # hard code first blind to be 10
        self.bet = 10
        # index of the dealer
        self.dealer = 0
        # players left: array of int indexes (important for showdown round)
        self.actives = [0, 1, 2, 3]

        #start the game dealing
        self.game_state = 'dealing'

    def set_players(self, players):
        for player in players:
            self.players.append(player.name)

    def set_community_cards(self, community_cards):
        # add to the community cards
        # self.community_cards.append()
        # based on where these are decided, maybe add makes more sense and call twice in flop
    

    def set_pot(self, pot):
        self.pot = pot

    def set_bet(self, new_bet):
        # wherever this is called, only call if new_bet > bet
        self.bet = new_bet

    def set_dealer(self):
        # dealer is the index of the dealer
        # use this index and add (and mod) to get other players such as blind and double_blind
        self.dealer += 1
        self.dealer % 4

    # set_actives is really just removing anyone who folds
    def remove_player(self, player):
        self.actives.remove(player.name)

    def set_round(self, round):
        # updates the enumerated type for round after the right number of turns have passed (depending on len(actives))
        # do we need to check that this is "next in line"?
        self.round = round


    def upload(self):
        return
    
    def fetch(self):
        return self.game_state
    
    def upload_turn():
        return
    
    def fetch_turn(player):
        return

