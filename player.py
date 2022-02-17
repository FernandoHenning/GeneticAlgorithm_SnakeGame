import random

from game import *


class RandomPlayer:
    def __init__(self, i):
        self.i = i
        self.score = 0

    def get_move(self, board, snake):
        r = random.randint(0, 3)
        return MOVES[r]

class GeneticPlayer():

    def __init__(self, genotype):
        self.genotype = genotype
        self.movements = self.genotype.copy()
        self.phenotype: float
        self.fitness: float
        self.score = 0

    def get_move(self, board, snake):
        index = self.movements.pop(0)
        return MOVES[index]
