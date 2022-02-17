import sys

import numpy as np
import pygame
from pygame.constants import QUIT

# Global variables

UP = (-1, 0)
DOWN = (1, 0)
LEFT = (0, -1)
RIGHT = (0, 1)

MOVES = [UP, DOWN, LEFT, RIGHT]

EMPTY = 0
FOOD = 99


class Game:

    def __init__(self, size: int, player, food_xy, gui=None, display=False, max_turns=100):
        self.size = size
        self.player = player
        self.gui = gui
        self.display = display
        self.max_movements = 100

        self.num_food = 4
        self.movements = 0
        self.snake_size = 3
        self.snake = [(1 * self.size // 2, self.size // 2 + i) for i in
                      range(self.snake_size)]

        self.food = [(self.size // 4, self.size // 4), (3 * self.size // 4, self.size // 4),
                     (self.size // 4, 3 * self.size // 4),
                     (3 * self.size // 4, 3 * self.size // 4)]
        self.board = np.zeros((self.size, self.size))

        for tup in self.snake:
            self.board[tup[0], tup[1]] = 1
        for tup in self.food:
            self.board[tup[0], tup[1]] = FOOD

        self.food_index = 0
        # THIS IS FOR DEBUGGING PURPOSE. CHANGE FOR RANDOM GENERATOR IN test.py
        self.food_xy = food_xy

    def move(self):

        try:
            move_i = self.player.get_move(self.board, self.snake)
        except IndexError:
            return False
        new_square = (self.snake[-1][0] + move_i[0], self.snake[-1][1] + move_i[1])

        self.snake.append(new_square)
        # update tail -----------------------------------------------
        head_i = self.snake[-1]
        if head_i not in self.food:
            self.board[self.snake[0][0]][self.snake[0][1]] = EMPTY
            self.snake.pop(0)
        else:
            if self.display:
                print("Eat!")
            self.player.score += 1
            self.food.remove(head_i)

        # Check out of bounds ---------------------------------------
        head_i = self.snake[-1]
        if head_i[0] >= self.size or head_i[1] >= self.size or head_i[0] < 0 or head_i[1] < 0:
            if self.display:
                print("Out of bounds")
            return False
        else:
            self.board[head_i[0], [head_i[1]]] = 1

        # Check for collisions ---------------------------------------
        head_i = self.snake[-1]

        if head_i in self.snake[:-1]:
            if self.display:
                print("Ate it self")
            return False

        # Spawn new food ---------------------------------------------
        while len(self.food) < self.num_food:
            x = self.food_xy[self.food_index][0]
            y = self.food_xy[self.food_index][1]
            while self.board[x][y] != EMPTY:
                self.food_index += 1
                x = self.food_xy[self.food_index][0]
                y = self.food_xy[self.food_index][1]
            self.food.append((x, y))
            self.board[x, y] = FOOD
            self.food_index += 1

        return True

    def play(self, display):
        if display:
            self.display_board()

        isAlive = self.move()
        if not isAlive:
            return True, self.player.score, self.movements
        self.movements += 1

        return False, self.player.score, self.movements

    def display_board(self):
        print("**********************************************")
        for i in range(self.size):
            for j in range(self.size):
                if self.board[i][j] == EMPTY:
                    print("|_", end="")
                elif self.board[i][j] == FOOD:
                    print("|#", end="")
                else:
                    print("|" + str(int(self.board[i][j])), end="")
            print("|")


class Gui:

    def __init__(self, game, size):
        self.game = game
        self.size = size
        self.game.gui = self

        self.ratio = self.size / self.game.size

        pygame.init()

        self.fps = 1
        self.fpsClock = pygame.time.Clock()

        width, height = self.size, self.size
        self.screen = pygame.display.set_mode((width, height))

        self.ga_surfaces = pygame.Surface((self.size, self.size))

        # Game loop.

    def run(self):
        while True:
            self.screen.fill((0, 0, 0))
            for i in range(len(self.game.snake)):

                # HEAD OF SNAKE
                pygame.draw.rect(self.ga_surfaces, (255, 0, 0),
                                 pygame.Rect(
                                     (self.ratio * (self.game.snake[-1][1]), self.ratio * (self.game.snake[-1][0])),
                                     (self.size // self.game.size, self.size // self.game.size)))
                # TAIL OF SNAKE
                for j in range(len(self.game.snake) - 1):
                    pygame.draw.rect(self.ga_surfaces, (0, 0, 255),
                                     pygame.Rect(
                                         ((self.game.snake[j][1] + 1), self.ratio * (self.game.snake[j][0] + 1)),
                                         (self.size // self.game.size, self.size // self.game.size)))
                # FOOD
            for food in self.game.food:
                pygame.draw.rect(self.ga_surfaces, (255, 255, 255),
                                 pygame.Rect((self.ratio * (food[1]), self.ratio * (food[0])),
                                             (self.size // self.game.size, self.size // self.game.size)))
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()

            # Update.
            self.update()
            isDead, score, movements = self.game.play(False)
            if isDead:
                pygame.quit()
                return score, movements
                # sys.exit()
            # Draw.
            self.screen.blit(self.ga_surfaces, (0, 0))

            pygame.display.flip()
            self.fpsClock.tick(self.fps)

    def update(self):
        empty = pygame.Color(0, 0, 0, 0)
        self.ga_surfaces.fill(empty)
        self.ga_surfaces.fill((55, 155, 255))
        for i in range(len(self.game.snake)):

            # HEAD OF SNAKE
            pygame.draw.rect(self.ga_surfaces, (255, 0, 0),
                             pygame.Rect((self.ratio * (self.game.snake[-1][1]), self.ratio * (self.game.snake[-1][0])),
                                         (self.size // self.game.size, self.size // self.game.size)))
            # TAIL OF SNAKE
            for j in range(len(self.game.snake) - 1):
                pygame.draw.rect(self.ga_surfaces, (0, 0, 255),
                                 pygame.Rect(
                                     (self.ratio * (self.game.snake[j][1]), self.ratio * (self.game.snake[j][0])),
                                     (self.size // self.game.size, self.size // self.game.size)))
            # FOOD
        for food in self.game.food:
            pygame.draw.rect(self.ga_surfaces, (255, 255, 255),
                             pygame.Rect((self.ratio * (food[1]), self.ratio * (food[0])),
                                         (self.size // self.game.size, self.size // self.game.size)))
