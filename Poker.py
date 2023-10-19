import Game
import Game_state
import Graphics
import threading
import time
import db_connect as database

def main():
	db = database.init()
	lock = threading.Lock()
	# Boots up graphics window in one thread
	# Calls game loop in another
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
	
	game_state = Game_state()
	
	graphicsThread = threading.Thread(Graphics.main(), num_players, host, game_state, lock)
	graphicsThread.start()

	lock.acquire()
	game = Game(num_players, game_state, host, db)
	lock.release()

	gameThread = threading.Thread(game.initial_main(), lock)
	gameThread.start()

	graphicsThread.join()
	gameThread.join()

	db.close()


main()
