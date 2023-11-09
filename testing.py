
from Game_state import Game_state
import db_connect as database
from cards import Card
from deck import Deck
from Player import Player

# function to test game_state class 

''' current failures
- community cards 
- community cards setter
- get bet
- decision 
- '''

def test_possible_hands():

    # [pair_values[[]],player_straight_flushes[[]],player_straights[[]], flushes[[],[],[],[]]
    def possible_hands_to_string(lst):
        # lst[0] is pair_values[ [] ], i is [], a list of cards of the same value
        for j, i in enumerate(lst):
            for e in i:
                for f in e:
                    if isinstance(f, list):
                        for g in f:
                            if j == 0:
                                print(f'pair values: {g.value} of {g.suit_to_str()}')
                            if j == 1:
                                print(f'straight flushes: {g.value} of {g.suit_to_str()}')
                            if j == 2:
                                print(f'straights: {g.value} of {g.suit_to_str()}')
                    if isinstance(f, Card):
                        if j == 0:
                            print(f'pair values: {f.value} of {f.suit_to_str()}')
                        if j == 1:
                            print(f'straight flushes: {f.value} of {f.suit_to_str()}')
                        if j == 2:
                            print(f'straights: {f.value} of {f.suit_to_str()}')
                        if j == 3:
                            print(f'flushes: {f.value} of {f.suit_to_str()}')


    player = Player()

    #four of a kind
    set_one = [Card(0,1),Card(1,1), Card(2,1), Card(3,1),Card(0,2),Card(1,2),Card(2,2)]
    # # two pair
    # set_two = [Card(0,1),Card(1,1), Card(2,11), Card(3,9),Card(0,7),Card(1,0),Card(2,2)]
    #
    player.set_hand(set_one)
    # if player.strength() != [["0 1", "1 1"],["0 1", "0 2"],player_straights, flushes]

    # [pair_values[[]],player_straight_flushes[],player_straights[[]], flushes[[],[],[],[]]
    print(strength_to_string(player.strength(set_one)))

def test_game_state():
    db = database.init()
    game_state_1 = Game_state(db, 'test_doc')
    if game_state_1.get_players(db) != []:
        print('FAILED PLAYER NAMES')
    else:
        print('PASSED PLAYER NAMES')
    # card functions
    game_state_1.set_community_cards([Card('d', 12), Card('c', 1)], db)
    if game_state_1.get_community_cards(db)[0] == Card('d', 12) and game_state_1.get_community_cards(db)[1] == Card('c', 1):
        print('PASSED COMMUNITY CARDS SETTER')
    else:
        print('FAILED COMMUNITY CARDS SETTER')

    hands = [[Card('h', 1), Card('h',2 )], [Card('h', 3), Card('h', 4)], [Card('h', 5), Card('h', 6)], [Card('h', 7), Card('h', 8)]]
    print(hands[0])
    print(hands[0][0])
    game_state_1.set_player_hands(hands, db)
    if game_state_1.get_player_hands(db) == [[Card('h', 1), Card('h',2 )], [Card('h', 3), Card('h', 4)], [Card('h', 5), Card('h', 6)], [Card('h', 7), Card('h', 8)]]:
       print('PASSED PLAYER HANDS')
    else:
        print('FAILED PLAYER HANDS')
    # community cards 
    if game_state_1.get_total_pot(db) != 0:
        print('FAILED TOTAL POT')
    else:
        print('PASSED TOTAL POT')
    if game_state_1.get_round_pot(db) != 0:
        print('FAILED ROUND POT')
    else:
        print('PASSED ROUND POT')
    expected_player_stacks = [1000, 1000, 1000, 1000]
    if game_state_1.get_player_stacks(db) != expected_player_stacks:
        print('FAILED PLAYER STACKS')
        print(game_state_1.get_player_stacks(db))
    else:
        print('PASSED PLAYER STACKS')
    expected_total_call = 0
    if game_state_1.get_total_call(db) != expected_total_call:
        print('FAILED TOTAL CALL')
        print(game_state_1.get_total_call(db))
    else:
        print('PASSED TOTAL_CALL')
    expected_waiting = False
    if game_state_1.get_waiting(db) != expected_waiting:
        print('FAILED WAITING')
    else:
        print('PASSED WAITING')
    game_state_1.flip_waiting(db)
    if game_state_1.get_waiting(db) != True:
        print('FAILED WAITING FLIP')
    else:
        print('PASSED WAITING FLIP')
    if game_state_1.get_whose_turn(db) != 0:
        print('FAILED WHOSE TURN')
    else:
        print('PASSED WHOSE TURN')
    if game_state_1.get_bet(db) != 0:
        print('FAILED GET BET')
    else:
        print('PASSED GET BET')
    if game_state_1.get_minimum_call(db) != 10:
        print('FAILED MIN CALL')
    else:
        print('PASSED MIN CALL')
    expected_dealer = 3
    game_state_1.set_dealer(expected_dealer, db)
    if game_state_1.get_dealer(db) != expected_dealer:
        print('FAILED DEALER')
    else:
        print('PASSED DEALER')
    if game_state_1.get_actives(db) != [0, 1, 2, 3]:
        print('FAILED ACTIVES')
    else:
        print('PASSED ACTIVES')
    if game_state_1.get_round(db) != 'dealing':
        print('FAILED ROUND')
    else:
        print('PASSED ROUND')
    # player_decision fails! 
    if game_state_1.get_player_decision(db)[0] != 'check' and game_state_1.get_player_decision(db)[1] != 0:
        print('FAILED DECISION')
    else:
        print('PASSED DECISION')

def test_deck():
    deck = Deck()
    #print(deck.deal())
    if len(deck.get_deck()) != 52:
        print('FAILED DECK WRONG SIZE')
        print(len(deck.get_deck()))
    else:
        print('PASSED DECK LENGTH')
    dealt = deck.deal()
    if len(dealt) != 4:
        print('FAILED DEAL')
    if len(dealt[0]) != 2:
        print('FAILED DEAL')
    else:
        print('PASSED DEAL')
    print(dealt)

def main():
    #test_game_state()
    # test_deck()
    test_possible_hands()

main()