import Game
import arcade
import Game_state
import Graphics
import threading
import time
import db_connect as database

def main():
	db = database.init()
	lock = threading.Lock()
	ready = False
	thread_ready = False
	# all shared variables get passed to both
	# NOTE: the classes must expect these variables and they must aqquire the lock any time they are 
	# interacted with (read/write). So every time a function interacts with the game_state, it must aquire/release

	# say you want to increment puppies:
	# lock.aquire()
	# puppies += 1
	# lock.release()

	#graphics window needs to prompt and allow input for the following 2 values:
	num_players = None #the number of non computer players for this game
	host = None #boolean value for whether the user on this machine is the host
	
	#init game_state
	game_state = Game_state.Game_state(db, 'doc1')

	
	# Boots up graphics window in one thread
	# graphicsThread = threading.Thread(group=None, target=Graphics.main, name=None, args=(num_players, host, game_state, thread_ready, lock,))
	# graphicsThread.start()
					#(group=None, target=None, name=None, args=(), kwargs={}, *, daemon=None)¶
	# while not ready:
	#	lock.acquire()
	#	if thread_ready:
	#		ready = True
	#	lock.release()
	#	time.sleep(2)
	#
	#lock.acquire()
	#game = Game(num_players, game_state, host, db)
	#lock.release()

	# Call game loop thread
	#gameThread = threading.Thread(group=None, target=game.initial_main, name=None, args=(game_state, lock))
	#gameThread.start()

#	graphicsThread.join()
#	gameThread.join()

#	db.close()


main()
