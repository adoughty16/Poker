
from Game_state import Game_state
import db_connect as database
from cards import Card
from deck import Deck
from Player import Player, HandStrength

# function to test game_state class 

''' current failures
- community cards 
- community cards setter
- get bet
- decision 
- '''

def test_showdown():
    db = database.init()
    game_state_1 = Game_state(db, 'test_doc')

    # test for tiebreaking two similar hands
    hand_one = [[2,HandStrength.TWO_PAIR], [5, HandStrength.TWO_PAIR], [11, HandStrength.HIGH_CARD], [3, HandStrength.ONE_PAIR]]
    result = game_state_1.showdown(hand_one)
    if result != [5, HandStrength.TWO_PAIR]:
        print('RANK TEST FAILED!')
    else:
        print('RANK TEST PASSED!')

    # test for high card
    hand_two = [[2, HandStrength.HIGH_CARD], [5, HandStrength.HIGH_CARD], [11, HandStrength.HIGH_CARD],
                [3, HandStrength.HIGH_CARD]]
    result = game_state_1.showdown(hand_two)
    if result != [11, HandStrength.HIGH_CARD]:
        print('HIGH CARD TEST FAILED!')
    else:
        print('HIGH CARD TEST PASSED!')

    # test for straight flush
    hand_three = [[2, HandStrength.HIGH_CARD], [5, HandStrength.HIGH_CARD], [11, HandStrength.HIGH_CARD],
                [3, HandStrength.STRAIGHT_FLUSH]]
    result = game_state_1.showdown(hand_three)
    if result != [3, HandStrength.STRAIGHT_FLUSH]:
        print('STRAIGHT FLUSH TEST FAILED!')
    else:
        print('STRAIGHT FLUSH TEST PASSED!')

def test_make_decision():
    db = database.init()
    player = Player()

    # 4 straight flush
    community_cards = [Card(0,1),Card(0,2),Card(2,11)]
    player.set_hand([Card(0,3),Card(0,4)])
    decision = player.make_decision(community_cards,db)
    if decision != ["bet", 700]:
        print('FAILED 4-STRAIGHT FLUSH!')
    else:
        print('PASSED 4-STRAIGHT FLUSH!')


def test_possible_hands():

    # [pair_values[[]],player_straight_flushes[[]],player_straights[[]], flushes[[],[],[],[]]
    def possible_hands_to_string(lst):
        # lst[0] is pair_values[ [] ], i is [], a list of cards of the same value
        for j, i in enumerate(lst):
            if not i:
                continue
            for f in i:
                if isinstance(f, list):
                    for g in f:
                        if j == 0:
                            print(f'pair values: {g.value} of {g.suit_to_str()}')
                        if j == 1:
                            print(f'straight flushes: {g.value} of {g.suit_to_str()}')
                        if j == 2:
                            print(f'straights: {g.value} of {g.suit_to_str()}')
                        if j == 3:
                            print(f'flushes: {g.value} of {g.suit_to_str()}')
                if isinstance(f, Card):
                    if j == 0:
                        print(f'pair values: {f.value} of {f.suit_to_str()}')
                    if j == 1:
                        print(f'straight flushes: {f.value} of {f.suit_to_str()}')
                    if j == 2:
                        print(f'straights: {f.value} of {f.suit_to_str()}')
                    if j == 3:
                        print(f'flushes: {f.value} of {f.suit_to_str()}')
                print('---')


    player = Player()

    #four of a kind
    set_one = [Card(0,1),Card(1,1), Card(2,1), Card(3,1),Card(0,2),Card(1,2),Card(2,2)]
    result = (player.evaluate_hand(set_one))
    if result != [1, HandStrength.FOUR_OF_A_KIND]:
        print('FAILED FOUR OF A KIND')
    else:
        print('PASSED FOUR OF A KIND')

    # straight flush
    set_two = [Card(0,1),Card(0,2),Card(0,3), Card(0,4), Card(0,5), Card(0,6), Card(0,7), ]
    result = (player.evaluate_hand(set_two))
    if result != [3, HandStrength.STRAIGHT_FLUSH]:
        print('FAILED STRAIGHT FLUSH')
    else:
        print('PASSED STRAIGHT FLUSH')

    #full house
    set_three= [Card(0,1),Card(1,1), Card(2,11), Card(3,11),Card(0,11),Card(1,0),Card(2,0)]
    result = (player.evaluate_hand(set_three))
    if result != [11, HandStrength.FULL_HOUSE]:
        print('FAILED FULL HOUSE')
    else:
        print('PASSED FULL HOUSE')
    # flush
    set_four = [Card(2, 1), Card(2, 3), Card(2, 11), Card(2, 11), Card(2, 6), Card(2, 0), Card(2, 8)]
    result = (player.evaluate_hand(set_four))
    if result != [11, HandStrength.FLUSH]:
        print('FAILED FLUSH')
    else:
        print('PASSED FLUSH')
    # straight
    set_five = [Card(1, 1), Card(2, 3), Card(0, 4), Card(2, 2), Card(1, 6), Card(3, 5), Card(0, 8)]
    result = (player.evaluate_hand(set_five))
    if result != [2, HandStrength.STRAIGHT]:
        print('FAILED STRAIGHT')
    else:
        print('PASSED STRAIGHT')
    # three of a kind
    set_six = [Card(1, 1), Card(2, 3), Card(0, 4), Card(2, 2), Card(1, 4), Card(3, 5), Card(2, 4)]
    result = (player.evaluate_hand(set_six))
    if result != [4, HandStrength.THREE_OF_A_KIND]:
        print('FAILED THREE OF A KIND')
    else:
        print('PASSED THREE OF A KIND')
    # two pair
    set_seven = [Card(1, 1), Card(2, 1), Card(0, 4), Card(2, 10), Card(1, 4), Card(3, 5), Card(2, 12)]
    result = (player.evaluate_hand(set_seven))
    if result != [4, HandStrength.TWO_PAIR]:
        print('FAILED TWO PAIR')
    else:
        print('PASSED TWO PAIR')
    # high card
    set_seven = [Card(1, 1), Card(2, 11), Card(0, 3), Card(2, 10), Card(1, 4), Card(3, 5), Card(2, 12)]
    result = (player.evaluate_hand(set_seven))
    if result != [12, HandStrength.HIGH_CARD]:
        print('FAILED HIGH CARD')
    else:
        print('PASSED HIGH CARD')
    # 4 cards- pair
    set_eight = [Card(1, 1), Card(2, 1), Card(0, 3), Card(2, 10)]
    result = (player.evaluate_hand(set_eight))
    if result != [1, HandStrength.ONE_PAIR]:
        print('FAILED 4-CARD PAIR')
    else:
        print('PASSED 4-CARD PAIR')
    # 3 cards- high card
    set_nine = [Card(1, 1), Card(2, 12), Card(0, 3)]
    result = (player.evaluate_hand(set_nine))
    if result != [12, HandStrength.HIGH_CARD]:
        print('FAILED 3-CARD HIGH CARD')
    else:
        print('PASSED 3-CARD HIGH CARD')

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
    game_state_1.clear_player_hands(db)
    print(game_state_1.get_player_hands(db))
    # community cards 
    game_state_1.clear_community_cards(db)
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
    for card in deck.get_deck():
        print(card.get_filename())

def main():
    test_game_state()
    # test_deck()
    #test_game_state()
    # test_deck()
    #test_possible_hands()

main()