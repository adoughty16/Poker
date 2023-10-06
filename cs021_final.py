"""
cs021 final project

collin rinaldi and nick lovera

"""

import random


#index 0 is Clubs, 1 is Diamonds, 2 is Hearts, 3 is Spades
# 1 is Ace, 11 is Jack, 12 is Queen, 13 is King
cards = ["c1","c2","c3","c4","c5","c6","c7","c8","c9","c10","c11","c12","c13",
         "d1","d2","d3","d4","d5","d6","d7","d8","d9","d10","d11","d12","d13",
         "h1","h2","h3","h4","h5","h6","h7","h8","h9","h10","h11","h12","h13",
         "s1","s2","s3","s4","s5","s6","s7","s8","s9","s10","s11","s12","s13"]



#community, a list of cards on the table

community = []

#player, a list where the first space is another list of their hand, and the second space is their last bet

player= [[],0]

#deck, a list of all cards in the game, should act as a QUEUE

deck = []

def init_deck():
        deck.clear()
        for i in cards:
                deck.append(i)

#burn, a list of burned cards
burn = []
#pot, an integer starting at 0, that tracks the total amount


#raise, an integer that holds the current amount raised
_raise_ = 10

#game, a dictionary containing players as keys and their hands as values
game = [[[],0]]

#shuffle() should add all the cards from the dictionary to a deck at random
#random.shuffle() deck
def shuffle_deck():
    random.shuffle(deck)
         
#dealer_deal_flop() for each playe twice it deals two cards from a deck
#for player in game
#for i in range(2)
#game{player} = [deck.pop(), deck.pop()]
def dealer_deal():
    player[0] = [deck.pop(),deck.pop()]
    print("Your hand:")
    show(player[0])
                  

#dealer_turn() burns a card and deals one community card
#burn.append(deck.pop())
#community.append(deck.pop())
def burn_and_turn():
    burn.insert(0, deck.pop())
    community.append(deck.pop())
     

#round_betting() for each player, gets their play (bet, fold, or pass)
#if they have not raised, ask if they want to fold or bet
#the bet has to be >=raise
def round_betting():
    
    for p in game:
        player[1] = 0
        
    for q in game:
        play = input("Your turn! What would you like to do? a) Bet b) Fold c) Pass :")
        play = play.lower()

        while (play!='a' and play!='b' and play!='c'):
            print("You must enter one of the choices!")
            play = input("Your turn! What would you like to do? a) Bet b) Fold c) Pass : ")
            play = play.lower()
            
        return play

#bet() takes a bet amount and adds it to the pot and prints the amount added

def bet(pot):
    x = 0
    while True:
        try:
            print(f"Current betting amount: {_raise_}")
            x = int(input("Enter amount to raise: $"))
            
            while ( x < _raise_):
                x = int(input(f"Must be at least ${_raise_}!\nEnter amount to raise: $"))
            player[1] = x
            print(f"Bet ${x}!")
            pot = pot + x
            print(f"Pot amount: ${pot}")
            return pot
        except ValueError:
            print('Bet must be a number!')
            bet(pot)
        
            

#show(player) takes a player and prints their hand
def show(lst):
    for card in lst:
        print_card(card)

#print_card(key) takes a card as a dictionary key and formats it to print as " <color> <num> of <suite> "
#
def print_card(card):
    suite = card[0]
    card = card[1:]
    if card == '1':
            card = 'Ace'
    if card == '11':
            card = 'Jack'
    if card == '12':
            card = 'Queen'
    if card == '13':
            card = 'King'
    if suite == 'c':
        print(f'{card} of Clubs')
        return 0
    if suite == 'd':
        print(f'{card} of Diamonds')
        return 0
    if suite == 'h':
        print(f'{card} of Hearts')
        return 0
    if suite == 's':
        print(f'{card} of Spades')
        return 0
    
#fold(player, show) takes a player and a bool and removes the player from the game and if show is true, prints their hand
def fold(player):
    while True:
        showcard = input('Do you want to show your cards? y or n: ')

        if showcard.lower() == 'y':
            show(player[0])
            player[0].clear()
            player[0] = [deck.pop(), deck.pop()]
            break
        
        elif showcard.lower() == 'n':
            player[0].clear()
            player[0] = [deck.pop(), deck.pop()]
            break

        else:
            print('Please enter yes or no')
        
def playagain():
        while True:
                playagain = input('Do you want to play again? y/n: ')

                if playagain.lower() == 'y':


                        
                        
                        return True

                elif playagain.lower() == 'n':
                        print('Have a nice day')
                        exit()

                else:
                        print('y or n')

def highestHand(lst, community):
        ascendingScore = 0
        matchingScore = 0
        maxAscendingScore = 0
        maxMatchingScore = 0
        maxFlushScore=0
        flushScore=0
        ascending = []
        matching = []
        houses = [0,0,0,0]
        strip = lst + community
        sortCards(strip)
        show(strip)
        rank=0
        flushRank = 0
        ascendingRank = 0
        matchingRank = 0
        
        for i, e in enumerate(strip):
                #check if ascending
                #add current card to ascending list
                ascending.append(e)

                #if the card is the first item in the list and the next number is sequential, increase the score
                if i == 0 and int(e[1:]) == int(strip[i+1][1:])+1:
                        ascendingScore+=1
                #if this card is an ascension of the last card and i is not too big to index to the nex card
                        #and if i is not 0 or if this card matches last card or if this card matches the next card then enter the loop
                elif ((int(e[1:]) == (int(strip[i-1][1:]) + 1)) and (i != len(strip))) and i!=0:
                        #if this card is an ascension of the last card
                        if (int(e[1:]) == (int(strip[i-1][1:]) + 1)):
                                ascendingScore+=1       
                                #if the last card is not in the list of ascending cards
                                if strip[i-1] not in ascending:
                                        #append the last card to the list of ascending cards
                                        ascending.append(strip[i-1])
                                        
                                #ascending.append(e)
                # if the card is not sequential but the next one is sequential
                if i != 0 and i!= 6 and (int(e[1:]) != (int(strip[i-1][1:]) + 1)) and int(e[1:]) == (int(strip[i+1][1:]) - 1):
                        ascendingScore = 0
                #if the card is not sequential
                if i != 0 and (int(e[1:]) != (int(strip[i-1][1:]) + 1)) and int(e[1:]) != (int(strip[i-1][1:])):
                        ascendingScore = 0
                        ascending.remove(e)
                
                        
                #check if matching
                matching.append(e)
                if i == 0 and int(e[1:]) == int(strip[i+1][1:]):
                        matchingScore+=1
                if i!=0 and (int(e[1:]) == (int(strip[i-1][1:]))):
                        if (int(e[1:]) == (int(strip[i-1][1:]))):
                            matchingScore+=1
                        if strip[i-1] not in matching:
                            matching.append(strip[i-1])
                
                if (int(e[1:]) != (int(strip[i-1][1:]))):
                        matchingScore = 0
                        matching.remove(e)


                #add to houses counters
                if e[0] == 'c':
                        houses[0] += 1
                if e[0] == 'd':
                        houses[1] += 1
                if e[0] == 'h':
                        houses[2] += 1
                if e[0] == 's':
                        houses[3] += 1

                if matchingScore > maxMatchingScore:
                        maxMatchingScore = matchingScore
                if ascendingScore > maxAscendingScore:
                        maxAscendingScore = ascendingScore

        for i in houses:
                if i > maxFlushScore:
                        maxFlushScore = i
                if i == maxFlushScore:
                        maxFlushScore =+ i
        for i in strip:
                rank+=int(i[1:])
        for i in ascending:
                ascendingRank=+int(i[1:])
        for i in matching:
                matchingRank=+int(i[1:])
                        

        sortCards(ascending)
        sortCards(matching)


        maxFlushScore +=1
        maxAscendingScore =+1
        maxMatchingScore =+1

        print(f'How good is your hand?\nHand score: {(maxFlushScore/2)*ascendingRank * maxAscendingScore + maxMatchingScore*matchingRank}')

                              

def sortCards(lst):
        n = len(lst)
        #bubbleSort by card number
        for i in range(n):
                for j in range(0, n - i - 1):
                        if int(lst[j][1:]) > int(lst[j+1][1:]):
                                lst[j], lst[j+1] = lst[j+1],lst[j]
        

                
if __name__ == '__main__':  
    while True:
        choice = input("Welcome to poker! Would you like to play? y/n: ")
    
        if choice.lower() == 'y':
            while True:
                print('-----------------------  New Game! -----------------------')
                pot = 0
                community.clear()
                for player in game:
                        player[0].clear()
                init_deck()
                shuffle_deck()
                dealer_deal()
                burn_and_turn()
                burn_and_turn()
                
                print('\nCommunity: ')
                show(community)
                print('-----\n')
                
                choice = round_betting()
                if (choice == 'a'):
                    pot = bet(pot)
                if (choice == 'b'):
                    fold(player)
                if (choice == 'c'):
                    print('Pass')
                    
                burn_and_turn()
                
                print("-----\nYour hand:")
                show(player[0])
                
                print('\nCommunity: ')
                show(community)
                print('-----\n')
                choice = round_betting()
                if (choice == 'a'):
                    pot = bet(pot)
                if (choice == 'b'):
                    fold(player)
                if (choice == 'c'):
                    print('Pass')
                
                burn_and_turn()

                print("-----\nYour hand:")
                show(player[0])
                
                print('\nCommunity: ')
                show(community)
                print('-----\n')
                choice = round_betting()
                if (choice == 'a'):
                    pot = bet(pot)
                if (choice == 'b'):
                    fold(player)
                if (choice == 'c'):
                    print('Pass')

                burn_and_turn()

                print("-----\nYour hand:")
                show(player[0])
                
                print('\nCommunity: ')
                show(community)
                print('-----\n')
                choice = round_betting()
                if (choice == 'a'):
                    pot = bet(pot)
                if (choice == 'b'):
                    fold(player)
                if (choice == 'c'):
                    print('Pass')
                highestHand(player[0],community)

                playagain()
        elif choice.lower() == 'n':
            print('Have a nice day')
            exit()
        else:
            print('Y or N')

            
             
             
