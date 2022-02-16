import random

from game import *


class RandomPlayer:
    def __init__(self, i):
        self.i = i
        self.score = 0

    def get_move(self, board, snake):
        r = random.randint(0, 3)
        return MOVES[r]
