# Here will be the code for generating the initial generation
import random
from statistics import mean, median
from genetic_algorithm.individual import *
import time


def generate_first_gen(classes, population_size, room_number):
    generation_list = []
    for i in range (population_size):
            current_individual = Schedule(len(classes), room_number)
            current_individual.set_random_classes(len(classes), room_number, classes)
            generation_list.append(current_individual)
        
    return generation_list


# Implements elitism - only a few schedules from current gen can survive, we fill the new gen with only children
def selection(generation: list[Schedule], selection_percent, population_size):
    """Chooses which Schedules (individuals) survive to the next generation"""
    # generation.sort(reverse=True, key=lambda Schedule: Schedule.get_fitness_score())   # This will sort the Schedules in a descending order, meaning the best Schedules will be up front
    # kept_individuals = selection_percent * len(generation)
    # generation = generation[:int(kept_individuals)] # round that to nearest integer
    # return generation
    # generation.sort(reverse=True, key= lambda Schedule: Schedule.get_fitness_score())
    # elites = generation[]

    return generation

def roulette_parent_selection(generation: list[Schedule]):
    generation.sort(reverse=True, key=lambda Schedule: Schedule.get_fitness_score())
    schedule_ranking = list(range(len(generation), 0, -1))
    random_scores = [random() for _ in range(len(schedule_ranking))]
    final = [schedule_ranking[i] * random_scores[i] for i in range(len(schedule_ranking))] # now this list is sorted ascendingly, so the biggest nums are on the end
    sorted_scores = sorted(range(len(final)), key=lambda i:final[i])
    return sorted_scores[-1], sorted_scores[-2]

def crossover_all(generation: list[Schedule], population_size: int, mutation_chance: int, classes: list[Subject]):
    """Breeds individuals (Schedules) which passed the selection (previous step in life cycle)"""
    passed_selection = len(generation)
    while len(generation) < population_size:
        # Roulette selection of parents

        # parent1 = randint(0, passed_selection - 1)
        # parent2 = randint(0, passed_selection - 1)
        parent1, parent2 = roulette_parent_selection(generation=generation)
        child1 = cross_over(parent1=generation[parent1], parent2=generation[parent2], class_list=classes, mutations = mutation_chance)

        generation.append(child1)
        # generation.append(child2)

    return generation
     
# def mutations(generation: list[Schedule], mutation_chance, classes):
#     """Function that handles calling the mutate function in cases it needs to be called"""
    
#     for individual in generation:
#         chance = random()

#         if chance <= mutation_chance:
#             individual.mutate(classes)

#     return generation

def life_cycle(max_generations, best_fitness, stopping_criteria, classes, population_size, selection_parameter, mutation_chance,rooms):
    """This is the main function that will do the genetic algorithm on populations, where the algorithm consists of:
        0. Generating the first population (Gen. 1)
        Then, we loop through the following 4 steps until one of the stopping criteria is fulfilled 
        * Loop stop criteria - reached max number of generations or the best Schedule is within an acceptable distance from an optimal one.
        The main loop consists of:
            1. Selection
            2. Crossover (breeding) including possible mutations on children genomes
            3. Recalculating fitness upon the population
        
        returns the best species from the population, regarded as the best schedule
    """
    current_gen = generate_first_gen(classes, population_size,len(rooms))
    generation_index = 1
    max_fitness = 0

    while not (generation_index == max_generations + 1 or abs(max_fitness - best_fitness) < stopping_criteria):
        print_generation(current_gen, generation_index)
        current_gen = selection(current_gen, selection_parameter)
        max_fitness = current_gen[0].get_fitness_score()
        current_gen = crossover_all(current_gen, population_size, mutation_chance, classes) # Crossover includes mutations of children
        # current_gen = mutations(current_gen, mutation_chance, classes)
        generation_index += 1

    current_gen = selection(current_gen, selection_parameter) # called to sort the population by fitness
    print("\n\nBEST BEBA")
    time.sleep(5)
    current_gen[0].nice_print()    
    current_gen[0].no_overlap()

    current_gen[0].write_schedule_to_html(classes, "schedules/probni4.html")
    return current_gen[0]  # This is the best schedule



def print_generation(generation: list[Schedule], index: int):
    """For debugging purposes, a function that will show the statistics of a generation"""
    print("\nGeneration no.", index)
    fitness_list = [ind.get_fitness_score() for ind in generation]
    print("Best fitness:", max(fitness_list))
    print("Mean fitness:", mean(fitness_list))
    print("Median fitness:", median(fitness_list))
    print("Worst fitness:", fitness_list[-1])

    print("\n-------------------------------------")
