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

    def __init__(self, size: int, num_snakes: int, player, gui=None, display=False, max_turns=100):
        print("[Game class]: Initializing game...")
        self.size = size
        self.num_snakes = num_snakes
        self.player = player
        self.gui = gui
        self.display = display
        self.max_turns = 100

        self.num_food = 4
        self.turn = 0
        self.snake_size = 3
        print("[Game class]: Generating snakes...")
        self.snake = [(1 * self.size // (2 * self.num_snakes), self.size // 2 + i) for i in
                      range(self.snake_size)]
        print(self.snake)
        print("[Game class] Generating food...")
        self.food = [(self.size // 4, self.size // 4), (3 * self.size // 4, self.size // 4),
                     (self.size // 4, 3 * self.size // 4),
                     (3 * self.size // 4, 3 * self.size // 4)]

        print("[Game class]: Creating board...")

        self.board = np.zeros((self.size, self.size))

        for tup in self.snake:
            self.board[tup[0], tup[1]] = 1
        for tup in self.food:
            self.board[tup[0], tup[1]] = FOOD

        self.food_index = 0
        # THIS IS FOR DEBUGING PURPOSE. CHANGE FOR RANDOM GENERATOR IN test.py
        self.food_xy = [(6, 7), (9, 7), (2, 6), (6, 7), (8, 7), (6, 2), (9, 2), (5, 3), (7, 9), (0, 4), (1, 0), (2, 0),
                        (2, 5), (7, 0), (8, 4), (9, 9), (9, 4), (1, 9), (4, 6), (1, 7), (8, 8), (0, 5), (9, 5), (6, 9),
                        (1, 5), (2, 1), (4, 9), (0, 6), (8, 0), (0, 3), (3, 5), (8, 8), (1, 7), (4, 2), (6, 7), (5, 3),
                        (0, 6), (6, 7), (9, 3), (9, 6), (3, 5), (7, 6), (7, 9), (1, 3), (4, 0), (4, 8), (1, 6), (0, 6),
                        (1, 3), (2, 8), (1, 7), (0, 3), (6, 2), (9, 2), (4, 0), (9, 5), (9, 1), (1, 2), (9, 9), (8, 8),
                        (6, 8), (1, 4), (4, 2), (0, 1), (7, 4), (3, 2), (4, 0), (7, 9), (3, 3), (6, 8), (3, 5), (6, 4),
                        (9, 0), (9, 0), (1, 9), (1, 1), (4, 0), (6, 2), (1, 6), (9, 3), (6, 2), (1, 4), (1, 6), (5, 4),
                        (7, 3), (3, 6), (9, 3), (3, 4), (8, 4), (8, 2), (9, 2), (9, 7), (1, 9), (8, 1), (5, 9), (9, 4),
                        (6, 7), (2, 6), (1, 8), (3, 2), (7, 7), (3, 6), (5, 3), (4, 4), (8, 3), (0, 3), (5, 4), (9, 8),
                        (6, 9), (7, 7), (8, 9), (5, 7), (4, 5), (6, 3), (9, 5), (2, 4), (6, 0), (3, 0), (1, 3), (9, 1),
                        (5, 1), (9, 4), (1, 3), (5, 1), (4, 8), (9, 7), (4, 7), (5, 9), (3, 8), (4, 1), (9, 4), (6, 7),
                        (2, 5), (5, 5), (0, 1), (0, 0), (0, 2), (7, 0), (6, 0), (2, 8), (5, 9), (4, 1), (2, 4), (4, 2),
                        (4, 5), (5, 5), (2, 0), (0, 3), (4, 1), (5, 0), (0, 3), (5, 5), (1, 8), (8, 9), (9, 2), (1, 3),
                        (9, 3), (6, 0), (3, 1), (7, 6), (3, 8), (8, 4), (9, 7), (7, 3), (1, 5), (9, 4), (6, 8), (3, 2),
                        (9, 9), (4, 1), (7, 5), (2, 9), (7, 2), (1, 3), (0, 8), (0, 4), (9, 3), (8, 5), (7, 9), (3, 3),
                        (3, 1), (9, 1), (6, 3), (1, 3), (6, 9), (2, 7), (2, 0), (3, 2), (3, 2), (9, 7), (0, 1), (0, 1),
                        (1, 7), (5, 6), (6, 2), (9, 6), (5, 0), (6, 5), (9, 0), (1, 6)]
        print("All done!")

    def move(self):
        moves = []

        move_i = self.player.get_move(self.board, self.snake)
        moves.append(move_i)
        new_square = (self.snake[-1][0] + move_i[0], self.snake[-1][1] + move_i[1])
        self.snake.append(new_square)
        # update tail
        head_i = self.snake[-1]
        if head_i not in self.food:
            self.board[self.snake[0][0]][self.snake[0][1]] = EMPTY
            self.snake.pop(0)
        else:
            self.player.score += 1
            self.food.remove(head_i)
        # Check out of bounds
        head_i = self.snake[-1]
        if head_i[0] >= self.size or head_i[1] >= self.size or head_i[0] < 0 or head_i[1] < 0:
            print("Out of bounds")
            print(f"Head position: x = {head_i[0]} y = {head_i[1]}")
            return False
        else:
            print("In bounds")
            print(f"Head position: x = {head_i[0]} y = {head_i[1]}")
            self.board[head_i[0], [head_i[1]]] = 1
        # Check for collisions

        head_i = self.snake[-1]
        if head_i in self.snake[:-1]:
            print("The snake ate it self")
            return False
        # Spawn new food
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

        if (len(self.snake[0]) - self.turn / 20) <= 0:
            print("Stopping game because I don't now")
            return -1
        if self.turn >= self.max_turns:
            print("Stopping because max turn reached")
            return 0
        isAlive = self.move()
        if not isAlive:
            print(f"Score: {self.player.score}")
            return True
        self.turn += 1

        self.display_board()
        return False

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
        print(self.ratio)

        pygame.init()

        fps = 1
        fpsClock = pygame.time.Clock()

        width, height = self.size, self.size
        screen = pygame.display.set_mode((width, height))

        self.ga_surfaces = pygame.Surface((self.size, self.size))

        # Game loop.
        while True:
            screen.fill((0, 0, 0))
            for i in range(len(self.game.snake)):

                # HEAD OF SNAKE
                pygame.draw.rect(self.ga_surfaces, (255, 0, 0),
                                 pygame.Rect((self.ratio * (self.game.snake[-1][1]), self.ratio * (self.game.snake[-1][0])),
                                             (self.size // self.game.size, self.size // self.game.size)))
                # TAIL OF SNAKE
                for j in range(len(self.game.snake) - 1):
                    pygame.draw.rect(self.ga_surfaces, (0, 0, 255),
                                     pygame.Rect(((self.game.snake[j][1] + 1), self.ratio * (self.game.snake[j][0] + 1)),
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
            isDead = self.game.play(True)
            if isDead:
                pygame.quit()
                sys.exit()
            # Draw.
            screen.blit(self.ga_surfaces, (0, 0))

            pygame.display.flip()
            fpsClock.tick(fps)


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
                                 pygame.Rect((self.ratio * (self.game.snake[j][1]), self.ratio * (self.game.snake[j][0])),
                                             (self.size // self.game.size, self.size // self.game.size)))
            # FOOD
        for food in self.game.food:
            pygame.draw.rect(self.ga_surfaces, (255, 255, 255),
                             pygame.Rect((self.ratio * (food[1]), self.ratio * (food[0])),
                                         (self.size // self.game.size, self.size // self.game.size)))
