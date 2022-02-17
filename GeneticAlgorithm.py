
from operator import itemgetter
from random import choices, choice
from sympy import var
from sympy import sympify
from sympy.utilities.lambdify import lambdify
from statistics import mean
from player import *
from game import *
import sys

class GeneticAlgorithm:

    def __init__(self,
                 limit_generations: int,
                 limit_population: int,
                 initial_populatin_size: int,
                 mutation_individual_prob: float,
                 mutation_gene_prob: float,
                 max_movements
                 ):
        self.max_movements = max_movements
        # --------------
        x = var('x')
        expr = sympify('x')
        self.f = lambdify(x, expr)
        # -----------------
        self.limit_generations = limit_generations
        self.limit_population = limit_population
        self.initial_population_size = initial_populatin_size
        self.population = []
        self.best_cases = []
        self.worst_cases = []
        self.avg_cases = []

        self.mutation_individual_prob = mutation_individual_prob
        self.mutation_gene_prob = mutation_gene_prob

        self.first_generation = []

    def mutate(self, individual):

        p = random.random()
        if p < self.mutation_individual_prob:
            for _ in range(self.max_movements):
                index = random.randrange(self.max_movements)
                individual[0][index] = individual[0][index] if random.random() > self.mutation_gene_prob else \
                    abs(individual[0][index] - 1)

            individual = self.generate_individual(individual[0])
            return individual
        else:
            return individual

    def generate_individual(self, genotype):
        size = 10
        num_snakes = 1
        gui_size = 600

        individual = GeneticPlayer(genotype)
        game = Game(size, individual,
                    food_xy=[(6, 7), (9, 7), (2, 6), (6, 7), (8, 7), (6, 2), (9, 2), (5, 3), (7, 9), (0, 4), (1, 0),
                             (2, 0),
                             (2, 5), (7, 0), (8, 4), (9, 9), (9, 4), (1, 9), (4, 6), (1, 7), (8, 8), (0, 5), (9, 5),
                             (6, 9),
                             (1, 5), (2, 1), (4, 9), (0, 6), (8, 0), (0, 3), (3, 5), (8, 8), (1, 7), (4, 2), (6, 7),
                             (5, 3),
                             (0, 6), (6, 7), (9, 3), (9, 6), (3, 5), (7, 6), (7, 9), (1, 3), (4, 0), (4, 8), (1, 6),
                             (0, 6),
                             (1, 3), (2, 8), (1, 7), (0, 3), (6, 2), (9, 2), (4, 0), (9, 5), (9, 1), (1, 2), (9, 9),
                             (8, 8),
                             (6, 8), (1, 4), (4, 2), (0, 1), (7, 4), (3, 2), (4, 0), (7, 9), (3, 3), (6, 8), (3, 5),
                             (6, 4),
                             (9, 0), (9, 0), (1, 9), (1, 1), (4, 0), (6, 2), (1, 6), (9, 3), (6, 2), (1, 4), (1, 6),
                             (5, 4),
                             (7, 3), (3, 6), (9, 3), (3, 4), (8, 4), (8, 2), (9, 2), (9, 7), (1, 9), (8, 1), (5, 9),
                             (9, 4),
                             (6, 7), (2, 6), (1, 8), (3, 2), (7, 7), (3, 6), (5, 3), (4, 4), (8, 3), (0, 3), (5, 4),
                             (9, 8),
                             (6, 9), (7, 7), (8, 9), (5, 7), (4, 5), (6, 3), (9, 5), (2, 4), (6, 0), (3, 0), (1, 3),
                             (9, 1),
                             (5, 1), (9, 4), (1, 3), (5, 1), (4, 8), (9, 7), (4, 7), (5, 9), (3, 8), (4, 1), (9, 4),
                             (6, 7),
                             (2, 5), (5, 5), (0, 1), (0, 0), (0, 2), (7, 0), (6, 0), (2, 8), (5, 9), (4, 1), (2, 4),
                             (4, 2),
                             (4, 5), (5, 5), (2, 0), (0, 3), (4, 1), (5, 0), (0, 3), (5, 5), (1, 8), (8, 9), (9, 2),
                             (1, 3),
                             (9, 3), (6, 0), (3, 1), (7, 6), (3, 8), (8, 4), (9, 7), (7, 3), (1, 5), (9, 4), (6, 8),
                             (3, 2),
                             (9, 9), (4, 1), (7, 5), (2, 9), (7, 2), (1, 3), (0, 8), (0, 4), (9, 3), (8, 5), (7, 9),
                             (3, 3),
                             (3, 1), (9, 1), (6, 3), (1, 3), (6, 9), (2, 7), (2, 0), (3, 2), (3, 2), (9, 7), (0, 1),
                             (0, 1),
                             (1, 7), (5, 6), (6, 2), (9, 6), (5, 0), (6, 5), (9, 0), (1, 6)], display=False,
                    max_turns=self.max_movements)
        #gui = Gui(game, gui_size)
        while True:
            isDead, score, movements = game.play(False)
            if isDead:
                break
        #score, movements = gui.run()
        phenotype = movements * 2**score
        fitness = self.f(phenotype)
        return [genotype, phenotype, fitness]

    def pruning(self):
        self.population = self.population[:self.limit_population]

    def random_crossover(self, a, b):
        p1 = random.randint(0, self.max_movements)
        p2 = random.randint(p1, self.max_movements)
        p3 = random.randint(p2, self.max_movements)
        genotype_a = a[0][0:p1] + b[0][p1:p2] + a[0][p2:p3] + b[0][p3:]
        genotype_b = a[0][0:p1] + b[0][p1:p2] + a[0][p2:p3] + b[0][p3:]
        offspring_a = self.generate_individual(genotype_a)
        offspring_b = self.generate_individual(genotype_b)
        return offspring_a, offspring_b

    @staticmethod
    def select_parent(population):
        return choices(population, weights=[x[2] for x in population], k=2)

    def generate_initial_population(self):
        for i in range(self.initial_population_size):
            genotype = choices([0, 1, 2, 3], k=self.max_movements)
            individual = self.generate_individual(genotype)
            self.population.append(individual)
            # [[GENOTYPE], PHENOTYPE, fitness]
    def run(self, minimize: bool):
        generation = 0

        self.generate_initial_population()

        self.population = sorted(self.population, key=itemgetter(2), reverse=True)

        self.first_generation = self.population.copy()
        for i in range(self.limit_generations):
            # SORTED BY BETTER FITNESS
            for j in range(int(len(self.population) / 2)):
                parent = self.select_parent(self.population)
                offspring_a, offspring_b = self.random_crossover(parent[0], parent[1])
                offspring_a = self.mutate(offspring_a)
                offspring_b = self.mutate(offspring_b)
                self.population.append(offspring_a)
                self.population.append(offspring_b)

            self.population = sorted(self.population, key=itemgetter(2), reverse=True)
            self.best_cases.append(self.population[0])
            self.avg_cases.append(mean([x[2] for x in self.population]))
            self.worst_cases.append(self.population[-1])

            if len(self.population) > self.limit_population:
                self.pruning()
            generation += 1

        return self.population[0][0], self.population[0][1], self.population[0][2]


"""
            x = []
            y = []
            for individual in self.population:
                x.append(individual[4])
                y.append(individual[5])

            colors = np.random.uniform(15, 80, len(x))
            # plot
            fig, ax = plt.subplots()
            ax.scatter(x, y, c=colors, vmin=0, vmax=100)

            ax.set(xlim=(self.interval_x[0], self.interval_x[1]), xticks=np.arange(0, self.interval_x[1]),
                   ylim=(self.interval_y[0], self.interval_y[1]), yticks=np.arange(0, self.interval_x[1]))
            plt.title(f"Generación {generation}")
            plt.xlabel("x")
            plt.ylabel("y")
            plt.savefig(f"images/generation {generation}.png")
"""