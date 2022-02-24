
from operator import itemgetter
from random import choices


from sympy import var
from sympy import sympify
from sympy.utilities.lambdify import lambdify
from statistics import mean
from player import *
from game import *


class GeneticAlgorithm:

    def __init__(self,
                 limit_generations: int,
                 limit_population: int,
                 initial_populatin_size: int,
                 mutation_individual_prob: float,
                 mutation_gene_prob: float,
                 max_movements,
                 food_xy
                 ):
        self.max_movements = max_movements
        self.food_xy = food_xy
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
        individual = GeneticPlayer(genotype)
        game = Game(size, individual,self.food_xy, display=False,max_turns=self.max_movements)

        while True:
            isDead, score, movements = game.play(False)
            if isDead:
                break
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
