
import arcade
import threading
import arcade.gui

# Screen title and size
SCREEN_WIDTH = 1024
SCREEN_HEIGHT = 768
SCREEN_TITLE = "Texas Hold'em Poker"

# Constants for sizing
CARD_SCALE = 0.6

# How big are the cards?
CARD_WIDTH = 140 * CARD_SCALE
CARD_HEIGHT = 190 * CARD_SCALE

# How big is the mat we'll place the card on?
MAT_PERCENT_OVERSIZE = 1.25
MAT_HEIGHT = int(CARD_HEIGHT * MAT_PERCENT_OVERSIZE)
MAT_WIDTH = int(CARD_WIDTH * MAT_PERCENT_OVERSIZE)

# How much space do we leave as a gap between the mats?
# Done as a percent of the mat size.
VERTICAL_MARGIN_PERCENT = 0.10
HORIZONTAL_MARGIN_PERCENT = 0.10

# The Y of the bottom row (2 piles)
BOTTOM_Y = MAT_HEIGHT / 2 + MAT_HEIGHT * VERTICAL_MARGIN_PERCENT

# The X of where to start putting things on bottom
START_X = SCREEN_WIDTH/2


# The Y of the top row
TOP_Y = SCREEN_HEIGHT - MAT_HEIGHT / 2 - MAT_HEIGHT * VERTICAL_MARGIN_PERCENT

# The Y of the middle row
MIDDLE_Y = SCREEN_HEIGHT/2

# the X for player 2, middle row
MIDDLE_X_2 = MAT_WIDTH / 2 + MAT_WIDTH * HORIZONTAL_MARGIN_PERCENT


# the X for player 4, middle row
MIDDLE_X_4 = MAT_WIDTH + MAT_WIDTH * HORIZONTAL_MARGIN_PERCENT


# How far apart each pile goes
X_SPACING = MAT_WIDTH + MAT_WIDTH * HORIZONTAL_MARGIN_PERCENT

# Card constants
CARD_VALUES = ["A", "2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K"]
CARD_SUITS = ["Clubs", "Hearts", "Spades", "Diamonds"]

# Face down image
FACE_DOWN_IMAGE = ":resources:images/cards/cardBack_red2.png"




''' CREATE THE WELCOME SCREEN'''

class WelcomeView(arcade.View):


    def __init__(self):
        super().__init__()

        # --- Required for all code that uses UI element,
        # a UIManager to handle the UI.
        self.manager = arcade.gui.UIManager()
        self.manager.enable()
        # Create a vertical BoxGroup to align buttons
        self.v_box = arcade.gui.UIBoxLayout()


        # creating host button
        host_button = arcade.gui.UIFlatButton(text="Host Game", width=200)
        self.v_box.add(host_button.with_space_around(bottom=20))

    #    self.manager.add(
      #      arcade.gui.UIAnchorWidget(
      #          anchor_x="center_x",
      #          anchor_y="center_y",
      #          child=host_button)
      #  )



        # creating join game button
        join_button = arcade.gui.UIFlatButton(text="Join Game", width=200)
        self.v_box.add(join_button.with_space_around(bottom=20))

        # creating 1 player button
      #  player1_button = arcade.gui.UIFlatButton(text="1 player", width=200)
       # self.v_box.add(player1_button.with_space_around(bottom=20))

        # creating 2 players button
      #  player2_button = arcade.gui.UIFlatButton(text="2 players", width=200)
      #  self.v_box.add(player2_button.with_space_around(bottom=20))


        # creating 3 players button
     #   player3_button = arcade.gui.UIFlatButton(text="3 players", width=200)
     #   self.v_box.add(player3_button.with_space_around(bottom=20))


        # creating 4 players button
      #  player4_button = arcade.gui.UIFlatButton(text="4 players", width=200)
      #  self.v_box.add(player4_button.with_space_around(bottom=20))

        # Create a widget to hold the v_box widget, that will center the buttons
        self.manager.add(
            arcade.gui.UIAnchorWidget(
                anchor_x="center_x",
                anchor_y="center_y",
                child=self.v_box)
        )



    def on_draw(self):
        self.clear()
        self.manager.draw()

    def on_show_view(self):
        """ This is run once when we switch to this view """
        arcade.set_background_color(arcade.csscolor.BROWN)

        # Reset the viewport, necessary if we have a scrolling game and we need
        # to reset the viewport back to the start so we can see what we draw.
        arcade.set_viewport(0, self.window.width, 0, self.window.height)


    def on_draw(self):
        """ Draw this view """
        self.clear()
        self.manager.draw()
        arcade.draw_text("Welcome to Texas Hold'em Poker!", self.window.width / 2, self.window.height - 50,
                         arcade.color.WHITE, font_size=48, anchor_x="center")
        arcade.draw_text("Click to advance", self.window.width / 2, self.window.height - 100,
                         arcade.color.WHITE, font_size=20, anchor_x="center")
        arcade.draw_text("Do you want to HOST or JOIN the game?", self.window.width / 2 , self.window.height /2 + 90,
                         arcade.color.WHITE, font_size=15, anchor_x="center")
        #arcade.draw_text("How many people are playing?", self.window.width - 70 , self.window.height / 2,
                         #arcade.color.WHITE, font_size=15, anchor_x="center")





    def on_mouse_press(self, _x, _y, _button, _modifiers):
        """ If the user presses the mouse button, start the game. """
        game_view = GameView()
        game_view.setup()
        self.window.show_view(game_view)







''' CREATE THE MAIN GAME '''

class GameView(arcade.View):
    """ Main application class. """

    def __init__(self):
        super().__init__()
        # Sprite list with all the cards, no matter what pile they are in.
        self.card_list = None

        arcade.set_background_color(arcade.color.AMAZON)

        # List of cards we are dragging with the mouse
        self.held_cards = None

        # Original location of cards we are dragging with the mouse in case
        # they have to go back.
        self.held_cards_original_position = None

        # Don't show the mouse cursor
        #self.window.set_mouse_visible(False)

        # Sprite list with all the mats tha cards lay on.
        self.pile_mat_list = None

    def setup(self):
        """ Set up the game here. Call this function to restart the game. """
        # List of cards we are dragging with the mouse
        self.held_cards = []

        # Original location of cards we are dragging with the mouse in case
        # they have to go back.
        self.held_cards_original_position = []

        # ---  Create the mats the cards go on.

        # Sprite list with all the mats tha cards lay on.
        self.pile_mat_list: arcade.SpriteList = arcade.SpriteList()

        # Create the mats for player 1 (bottom)
        pile = arcade.SpriteSolidColor(MAT_WIDTH, MAT_HEIGHT, arcade.csscolor.DARK_OLIVE_GREEN)
        pile.position = START_X, BOTTOM_Y
        self.pile_mat_list.append(pile)

        pile = arcade.SpriteSolidColor(MAT_WIDTH, MAT_HEIGHT, arcade.csscolor.DARK_OLIVE_GREEN)
        pile.position = START_X + X_SPACING, BOTTOM_Y
        self.pile_mat_list.append(pile)

        # Create player 2 (left)
        for i in range(2):
            pile = arcade.SpriteSolidColor(MAT_WIDTH, MAT_HEIGHT, arcade.csscolor.DARK_OLIVE_GREEN)
            pile.position = MIDDLE_X_2 + i * X_SPACING, MIDDLE_Y
            self.pile_mat_list.append(pile)

        # Create player 3 (top)
        for i in range(2):
            pile = arcade.SpriteSolidColor(MAT_WIDTH, MAT_HEIGHT, arcade.csscolor.DARK_OLIVE_GREEN)
            pile.position = START_X + i * X_SPACING, TOP_Y
            self.pile_mat_list.append(pile)

        # create player 4 (right)
       # for i in range(2):
           # pile = arcade.SpriteSolidColor(MAT_WIDTH, MAT_HEIGHT, arcade.csscolor.DARK_OLIVE_GREEN)
          #  pile.position = MIDDLE_X_4 + i * X_SPACING, MIDDLE_Y
          #  self.pile_mat_list.append(pile)




        # Sprite list with all the cards, no matter what pile they are in.
        self.card_list = arcade.SpriteList()

        # Create every card
        for card_suit in CARD_SUITS:
            for card_value in CARD_VALUES:
                card = Card(card_suit, card_value, CARD_SCALE)
                card.position = START_X, BOTTOM_Y
                self.card_list.append(card)
        pass

    def pull_to_top(self, card: arcade.Sprite):
        """ Pull card to top of rendering order (last to render, looks on-top) """

        # Remove, and append to the end
        self.card_list.remove(card)
        self.card_list.append(card)

    def on_mouse_press(self, x, y, button, key_modifiers):
        """ Called when the user presses a mouse button. """

        # Get list of cards we've clicked on
        cards = arcade.get_sprites_at_point((x, y), self.card_list)

        # Have we clicked on a card?
        if len(cards) > 0:

            # Might be a stack of cards, get the top one
            primary_card = cards[-1]

            # All other cases, grab the face-up card we are clicking on
            self.held_cards = [primary_card]
            # Save the position
            self.held_cards_original_position = [self.held_cards[0].position]
            # Put on top in drawing order
            self.pull_to_top(self.held_cards[0])


    def on_mouse_motion(self, x: float, y: float, dx: float, dy: float):
        """ User moves mouse """

        # If we are holding cards, move them with the mouse
        for card in self.held_cards:
            card.center_x += dx
            card.center_y += dy

    def on_mouse_release(self, x: float, y: float, button: int,
                         modifiers: int):
        """ Called when the user presses a mouse button. """

        # If we don't have any cards, who cares
        if len(self.held_cards) == 0:
            return

        # We are no longer holding cards
        self.held_cards = []



    def on_draw(self):
        """ Render the screen. """
        # Clear the screen
        self.clear()

        # Draw the mats the cards go on to
        self.pile_mat_list.draw()

        # Draw the cards
        self.card_list.draw()

    def on_mouse_press(self, x, y, button, key_modifiers):
        """ Called when the user presses a mouse button. """
        # Get list of cards we've clicked on
        cards = arcade.get_sprites_at_point((x, y), self.card_list)

        # Have we clicked on a card?
        if len(cards) > 0:
            # Might be a stack of cards, get the top one
            primary_card = cards[-1]

            # All other cases, grab the face-up card we are clicking on
            self.held_cards = [primary_card]
            # Save the position
            self.held_cards_original_position = [self.held_cards[0].position]
            # Put on top in drawing order
            self.pull_to_top(self.held_cards[0])

    def on_mouse_release(self, x: float, y: float, button: int,
                         modifiers: int):
        """ Called when the user presses a mouse button. """
        # If we don't have any cards, who cares
        if len(self.held_cards) == 0:
            return

        # We are no longer holding cards
        self.held_cards = []

    def on_mouse_motion(self, x: float, y: float, dx: float, dy: float):
        """ User moves mouse """
        pass

class Card(arcade.Sprite):
    """ Card sprite """

    def __init__(self, suit, value, scale=1):
        """ Card constructor """

        # Attributes for suit and value
        self.suit = suit
        self.value = value

        # Image to use for the sprite when face up
        self.image_file_name = f":resources:images/cards/card{self.suit}{self.value}.png"

        # Call the parent
        super().__init__(self.image_file_name, scale, hit_box_algorithm="None")


def main():
    """ Main function """

    window = arcade.Window(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    start_view = WelcomeView()
    window.show_view(start_view)
    arcade.run()




if __name__ == "__main__":
    main()

