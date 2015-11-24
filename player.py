# Python Final Project
# Connect Four
#
# Irving Salmeron
# Juan Pablo Meouchi


import random
import os
import time
from minimax import Minimax

class Player(object):
    type = None # possible types are "Human" and "AI"
    name = None
    color = None
    difficulty = None

    def __init__(self, name, color,playertype,difficulty=None):
        self.type = playertype
        self.name = name
        self.color = color
        self.difficulty = difficulty
    
    def move(self, state, rounds):
        if self.type.lower() == 'human':
            print("{0}'s turn.  {0} is {1}".format(self.name, self.color))
            column = None
            while column == None:
                try:
                    choice = int(input("Enter a move (1-7): ")) - 1
                except ValueError:
                    choice = None
                if 0 <= choice <= 6:
                    column = choice
                else:
                    print("Invalid choice, try again")
            return column
        else:
            print("{0}'s turn.  {0} is {1}".format(self.name, self.color))
            #return random.randint(0, 6)
            m = Minimax(state)
            best_alpha, alpha = m.findColumn(self.difficulty, state, self.color, rounds)
            return best_alpha