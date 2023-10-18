#import


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

    def __init__(self):
        #populate variables

        #start the game dealing
        self.game_state = 'dealing'
        return

    def upload_game_state():
        return
    
    def fetch_game_state():
        return self.game_state
    
    def upload_turn():
        return
    
    def fetch_turn(player):
        return

