from player import *
from game import *
from GeneticAlgorithm import GeneticAlgorithm
import matplotlib.pyplot as plt

from tkinter import messagebox
import tkinter as tk
from tkinter import ttk
import numpy as np



# root window
root = tk.Tk()

root.geometry("600x400")
root.title('Algorítmo Genético - Maximizar y Minimizar')

root.configure(bg="white")

# configure the grid
root.columnconfigure(0, weight=1)
root.columnconfigure(1, weight=7)

title_label = ttk.Label(root, text="Parámetros inciales del algoritmo", background='#fff',
                        font=('Lucida Sands', '12', 'bold'))
title_label.grid(column=1, row=0, )

# GENERACIONS MÁXIMAS --------------------------------------------------------
max_generations_label = ttk.Label(root, text="Generaciones máximas", background='#fff', font=('Lucida Sands', '10'))

max_generations_label.grid(column=1, row=1, sticky=tk.W, padx=5, pady=5)

max_generations_entry = ttk.Entry(root)
max_generations_entry.insert(0, "500")
max_generations_entry.grid(column=1, row=1, sticky=tk.E, padx=5, pady=5)

# POBLACIÓN MÁXCIMA--------------------------------------------------------
max_population_label = ttk.Label(root, text="Población Máxima", background='#fff', font=('Lucida Sands', '10'))

max_population_label.grid(column=1, row=2, sticky=tk.W, padx=5, pady=5)

max_population_entry = ttk.Entry(root)
max_population_entry.insert(0, "100")
max_population_entry.grid(column=1, row=2, sticky=tk.E, padx=5, pady=5)


# POBLACIÓN INICIAL --------------------------------------------------------
initial_population_label = ttk.Label(root, text="¨Población inicial:", background='#fff', font=('Lucida Sands', '10'))

initial_population_label.grid(column=1, row=3, sticky=tk.W, padx=5, pady=5)

initial_population_entry = ttk.Entry(root)
initial_population_entry.insert(0, "10")
initial_population_entry.grid(column=1, row=3, sticky=tk.E, padx=5, pady=5)

# PROBABILIDAD DE MUTACIÓN INDIVIDUO --------------------------------------------------------
mutacion_individuo_label = ttk.Label(root, text="Probabilidad de mutación de individuo:", background='#fff', font=('Lucida Sands', '10'))

mutacion_individuo_label.grid(column=1, row=4, sticky=tk.W, padx=5, pady=5)

mutacion_individuo_entry = ttk.Entry(root)
mutacion_individuo_entry.insert(0, "0.7")
mutacion_individuo_entry.grid(column=1, row=4, sticky=tk.E, padx=5, pady=5)


# PROBABILIDAD DE MUTACIÓN POR GEN --------------------------------------------------------
mutacion_gen_label = ttk.Label(root, text="Probabilidad de mutación de un gen:", background='#fff', font=('Lucida Sands', '10'))

mutacion_gen_label.grid(column=1, row=5, sticky=tk.W, padx=5, pady=5)

mutacion_gen_entry = ttk.Entry(root)
mutacion_gen_entry.insert(0, "0.01")
mutacion_gen_entry.grid(column=1, row=5, sticky=tk.E, padx=5, pady=5)


# Movimiento máximos --------------------------------------------------------
max_movements_label = ttk.Label(root, text="Movimiento máximos permitidos:", background='#fff', font=('Lucida Sands', '10'))

max_movements_label.grid(column=1, row=6, sticky=tk.W, padx=5, pady=5)

max_movements_entry = ttk.Entry(root)
max_movements_entry.insert(0, "50")
max_movements_entry.grid(column=1, row=6, sticky=tk.E, padx=5, pady=5)



def graph(ga):
    plt.plot(np.arange(0, ga.limit_generations), [x[2] for x in ga.best_cases], label="Best cases")
    plt.plot(np.arange(0, ga.limit_generations), [x[2] for x in ga.worst_cases], label="Worst cases")
    plt.plot(np.arange(0, ga.limit_generations), ga.avg_cases, label="Average cases")
    plt.legend()
    plt.title("Evolución de la población")
    plt.xlabel("Generaciones/Iteraciones")
    plt.ylabel("Valor de aptitud")
    plt.show()


def run():
    size = 10
    num_snakes = 1

    gui_size = 600

    food_xy = [(random.randint(0, 9), random.randint(0, 9)) for _ in range(200)]
    ga = GeneticAlgorithm(
        limit_generations=int(max_generations_entry.get()),
        limit_population=int(max_population_entry.get()),
        initial_populatin_size=int(initial_population_entry.get()),
        mutation_individual_prob=float(mutacion_individuo_entry.get()),
        mutation_gene_prob=float(mutacion_gen_entry.get()),
        max_movements=int(max_movements_entry.get()),
        food_xy=food_xy
    )
    best_individual = ga.run(True)
    best_player = GeneticPlayer(best_individual[0])
    graph(ga)
    messagebox.showinfo(
        message=f"Genotipo : {best_individual[0]}, Fenotipo: {best_individual[1]}, Aptitud: {best_individual[2]}",
        title="Mejor individuo")

    game = Game(size, best_player, food_xy, display=True, max_turns=50)
    gui = Gui(game, gui_size)
    gui.run()



login_button = ttk.Button(root, text="Ejecutar", command=lambda: run())
login_button.grid(column=1, row=15, sticky=tk.W, padx=5, pady=5)


root.mainloop()








