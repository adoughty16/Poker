#import Game
import threading
import time
import db_connect as database

def main():
	# Boots up graphics window

	# establish what values might change during the course of the game that must be drawn
	# these values need to be mutable objects so that we can pass them into a thread and then the
	# thread can update them in real time while the graphics loop perdiodically draws them (automatically
	# drawing any values that have been updated in the threads)

	#Calls Game thread and passes it game_state_values to update
	db = database.init()

	
	Game(players, gamestate, host, db)


	#while gaming:
		#ask for permision to check game_state
			#draw
		#wait



db.close()


main()
