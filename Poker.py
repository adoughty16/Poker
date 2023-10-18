#import Game
import threading
import time
import db_connect as database

#sample class to check DB upload
class Apple():
	def __init__(self, name, color, sweetness):
		self.name = name
		self.color = color
		self.sweetness = sweetness

	def to_dict(self):
		return {
            'name': self.name,
            'color': self.color,
            'sweetness' : self.sweetness
        }


def main():
	# Boots up graphics window

	# establish what values might change during the course of the game that must be drawn
	# these values need to be mutable objects so that we can pass them into a thread and then the
	# thread can update them in real time while the graphics loop perdiodically draws them (automatically
	# drawing any values that have been updated in the threads)

	#Calls Game thread and passes it game_state_values to update


	#while gaming:
		#ask for permision to check game_state
			#draw
		#wait







	#THIS IS JUST A SAMPLE OF HOW TO DO THIS
	db = database.init()
	apple = Apple('granny-smith','green','sour')
	doc_ref = db.collection('apple').document('my_document')
	doc_ref.set(apple.to_dict())
	db.close()

main()
