import Game
import arcade
import Game_state
import Graphics
import time
import db_connect as database
from Graphics import WelcomeView


def main():
	db = database.init()

	#graphics window needs to prompt and allow input for the following 2 values:
	num_players = None #the number of non computer players for this game
	host = None #boolean value for whether the user on this machine is the host

	#init game_state
	game_state = Game_state.Game_state(db, 'doc1')

	game_state.set_selected_host(True)  # Set initial value for selected_host
	game_state.set_selected_players(1)  # Set initial value for selected_players

	# Create an instance of the WelcomeView and pass the game_state object
	Graphics.main(game_state)


#	db.close()


main()
