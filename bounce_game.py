"""

_  __  ___b o u n c e___  __  _
        a Pong knock off

by Justin Meredith.
project started March 16th, 2018.


"""



#   ~   ~   ~   ~   MODULES & SET UP   ~   ~   ~   ~   ~#

import sys, pygame as game, get_image_size, random

game.init()

graphics_path = "graphics/"
fps_clock = game.time.Clock()



#   ~   ~   ~   ~   CLASSES   ~   ~   ~   ~   ~#

# the Board class is used to create the screen and background images
class Board:
    def __init__(self, image_file):
        self.file_name = image_file
        self.background = game.image.load(graphics_path + self.file_name)
        self.size = width, height = get_image_size.get_image_size(graphics_path + self.file_name)
        self.screen = game.display.set_mode(self.size)

    def display(self):
        self.screen.blit(self.background, (0, 0))


class Score:
    def __init__(self, side_of_screen):
        self.load_numbers()
        self.score_count = 0
        self.change_score()
        if side_of_screen == "left":
            self.rectangle.centerx = 50
            self.rectangle.centery = 50
        elif side_of_screen == "right":
            self.rectangle.centerx = board.size[0] - 50
            self.rectangle.centery = 50

    def load_numbers(self):
        self.zero = game.image.load(graphics_path + "0.png")
        self.one = game.image.load(graphics_path + "1.png")
        self.two = game.image.load(graphics_path + "2.png")
        self.three = game.image.load(graphics_path + "3.png")
        self.four = game.image.load(graphics_path + "4.png")
        self.five = game.image.load(graphics_path + "5.png")
        self.six = game.image.load(graphics_path + "6.png")
        self.seven = game.image.load(graphics_path + "7.png")

    def change_score(self):
        if self.score_count == 0:
            self.current_score = self.zero
        elif self.score_count == 1:
            self.current_score = self.one
        elif self.score_count == 2:
            self.current_score = self.two
        elif self.score_count == 3:
            self.current_score = self.three
        elif self.score_count == 4:
            self.current_score = self.four
        elif self.score_count == 5:
            self.current_score = self.five
        elif self.score_count == 6:
            self.current_score = self.six
        elif self.score_count == 7:
            self.current_score = self.seven

        self.rectangle = self.current_score.get_rect()

    def display(self):
        board.screen.blit(self.current_score, self.rectangle)


# the Paddle class is used to create and control the paddles
class Paddle:
    def __init__(self, image_file, side_of_screen):
        self.file_name = image_file
        self.paddle = game.image.load(graphics_path + self.file_name)
        self.rectangle = self.paddle.get_rect()
        if side_of_screen == "left":
            self.rectangle.centerx = 30
            self.up = game.K_w
            self.down = game.K_s
        elif side_of_screen == "right":
            self.rectangle.centerx = board.size[0] - 30
            self.up = game.K_UP
            self.down = game.K_DOWN
        self.rectangle.centery = board.size[1] / 2
        self.speed = 8

    def display(self):
        board.screen.blit(self.paddle, self.rectangle)

    def move(self, key_input):
        if key_input[self.up] and self.rectangle.top >= 0:
            self.rectangle.centery -= self.speed
        elif key_input[self.down] and self.rectangle.bottom <= board.size[1]:
            self.rectangle.centery += self.speed

    def reset_position(self):
        self.rectangle.centery = board.size[1] / 2


# the Ball class is used to create and control the ball
class Ball:
    def __init__(self, image_file):
        self.file_name = image_file
        self.ball = game.image.load(graphics_path + self.file_name)
        self.rectangle = self.ball.get_rect()
        self.rectangle.centerx = board.size[0] / 2
        self.rectangle.centery = board.size[1] / 2
        self.start_moving = False
        self.speed = [4.5, 4.5]
        self.randomize_speed()

    def display(self):
        board.screen.blit(self.ball, self.rectangle)

    def move(self):
        if self.start_moving == True:
            self.rectangle = self.rectangle.move(self.speed)
            if self.rectangle.right < 0 or self.rectangle.left > board.size[0]:      # going off left or right of screen
                reset_positions(ball, left_paddle, right_paddle)

            if self.rectangle.top < 0 or self.rectangle.bottom > board.size[1]:      # bouncing off top or bottom of screen
                self.speed[1] = -self.speed[1]

            if self.rectangle.colliderect(left_paddle.rectangle) and self.rectangle.left == 32 and self.rectangle.top > left_paddle.rectangle.top and self.rectangle.bottom < left_paddle.rectangle.bottom:      # bouncing off of the left paddle
                self.speed[0] = -self.speed[0]

            if self.rectangle.colliderect(right_paddle.rectangle) and self.rectangle.right == 791 and self.rectangle.top > right_paddle.rectangle.top and self.rectangle.bottom < right_paddle.rectangle.bottom:      # bouncing off of the right paddle
                self.speed[0] = -self.speed[0]

    def reset_position(self):
        self.rectangle.move([0, 0])
        ball.start_moving = False
        self.randomize_speed()
        self.rectangle.centerx = board.size[0] / 2
        self.rectangle.centery = board.size[1] / 2

    def randomize_speed(self):
        randomizer = (-1)**random.randrange(2)      # generates a 1 or -1
        self.speed[0] *= randomizer
        self.speed[1] *= randomizer



#   ~   ~   ~   ~   FUNCTIONS   ~   ~   ~   ~   ~#

def update_display(board, score, ball, left_paddle, right_paddle):
    board.display()
    score.display()
    ball.display()
    left_paddle.display()
    right_paddle.display()

def reset_positions(ball, left_paddle, right_paddle):
    ball.reset_position()
    left_paddle.reset_position()
    right_paddle.reset_position()



#   ~   ~   ~   ~   SETTING THE BOARD   ~   ~   ~   ~   ~#

board = Board("background.png")
score = Score("left")
ball = Ball("ball.png")
left_paddle = Paddle("paddle.png", "left")
right_paddle = Paddle("paddle.png", "right")
update_display(board, score, ball, left_paddle, right_paddle)
game.display.update()


#   ~   ~   ~   ~   RUNNING THE GAME   ~   ~   ~   ~   ~#

while True:

    #//// Check for Specific Events //

    for event in game.event.get():
        if event.type == game.QUIT:      # allows the player to exit the game by clicking the exit 'X' on the window
            game.quit()
            raise SystemExit


    #//// Variables for Running the Game //

    fps_clock.tick(60)      # sets the frame rate at 60fps
    game.event.pump()
    key_input = game.key.get_pressed()
    update_display(board, score, ball, left_paddle, right_paddle)
    game.display.update()


    #//// Moving Objects //

    #// Moving the left paddle /
    if key_input[left_paddle.up] or key_input[left_paddle.down]:
        left_paddle.move(key_input)
        ball.start_moving = True

    #// Moving the right paddle /
    if key_input[right_paddle.up] or key_input[right_paddle.down]:
        right_paddle.move(key_input)
        ball.start_moving = True

    ball.move()
