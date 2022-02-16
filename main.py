from player import *
from game import *

size = 10
num_snakes = 1
players = RandomPlayer(0)

gui_size = 600

game = Game(size, num_snakes, players, display=True, max_turns=100)
gui = Gui(game, gui_size)

# GENERAR MOVIMIENTOS ALEATORIOS PARA GENERAR EL GENOTIPO Y AL MISMO TIEMPO IR JUGANDO PARA OBTENER LA APTITUD