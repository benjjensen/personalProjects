# https://github.com/korolvs/snake_nn/blob/master/snake_game.py

import curses
from random import randint

class SnakeGame:
    def __init__(self, board_width = 20, board_height = 20, gui = False):
        self.score = 0.0
        self.done = False
        self.board = {'width': board_width, 'height': board_height}
        self.gui = gui
    
    def start(self):
        self.snake_init()
        self.generate_food()
        if self.gui: 
            self.render_init()

        return self.generate_observations()

    def snake_init(self):
        '''
            Generates the starting snake, which comprises three connected 
            points starting somewhere in the board (but not near the edges)
        '''
        x = randint(5, self.board["width"] - 5) # Keeps the snake at least 5 spaces from each edge
        y = randint(5, self.board["height"] - 5)
        self.snake = []
        vertical = randint(0,1) == 0 # Determines if the snake will be vertical or not
        for i in range(3):
            point = [x+i, y] if vertical else [x, y + i]
            self.snake.insert(0, point)

    def generate_food(self):
        '''
            Generates a piece of food in a random location not covered by the snake
        '''
        food = []
        while food == []:
            food = [randint(1, self.board["width"]), randint(1, self.board["height"])]
            if food in self.snake: 
                food = []
        self.food = food

    def render_init(self):
        '''
            Generates a screen for the human to see
        '''
        curses.initscr()
        win = curses.newwin(self.board["width"] + 2, self.board["height"] + 2, 0, 0)
        curses.curs_set(0)
        win.nodelay(1)
        win.timeout(200)
        self.win = win
        self.render()

    def step(self, key):
        ''' 
            Takes in an input key and moves the snake accordingly
            0 -> up, 1 -> right, 2 -> down, 3 -> left
        '''
        if self.done == True: 
            self.end_game()
        self.create_new_point(key)
        if self.food_eaten():
            self.score += 1
            self.generate_food()
        

