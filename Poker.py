import Game
import Game_state
import Graphics
import threading
import time
import db_connect as database

def main():
	lock = threading.Lock()
	# Boots up graphics window in one thread
	# Calls game loop in another
	# all shared variables get passed to both
	# NOTE: the classes must expect these variables and they must aqquire the lock any time they are changed

	# say you want to increment shared variable puppies:
	# lock.aquire()
	# puppies += 1
	# lock.release()

	#graphics window needs to prompt and allow input for the following values	
	players = None #the number of non computer players for this game
	host = None #boolean value for wether the user on this machine is the host



	game_state = Game_state()
	db = database.init()

	game = Game(players, game_state, host, db)

	graphThread = threading.Thread(Graphics.main(), players, host)
	gameThread = threading.Thread(game.initial_main(), None)

	graphThread.start()
	gameThread.start()

	graphThread.join()
	gameThread.join()

	db.close()


main()
