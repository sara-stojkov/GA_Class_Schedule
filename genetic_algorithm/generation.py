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
def selection(generation: list[Schedule], child_generation: list[Schedule], selection_percent, population_size):
    """Chooses which Schedules (individuals) survive to the next generation.
    Elitism is implemented by selecting 10% of best individuals from the parent generation.
    Then, the rest of the new population is filled with the best individuals from the new generation.
    That way, monotomy is harder to achieve and the generations get a big refresh."""

    num_parents= int(selection_percent * population_size)  # How many parents will survive to the next generation

    generation.sort(reverse=True, key=lambda Schedule: Schedule.get_fitness_score()) 
    surviving_parents = generation[:num_parents]  # Take the best Schedules from the current generation

    num_children = population_size - num_parents

    child_generation.sort(reverse=True, key=lambda Schedule: Schedule.get_fitness_score())  # Sort children by fitness score 
    surviving_children = child_generation[:num_children]
    final_gen = surviving_parents + surviving_children  # Fill the new generation with the best of both batches

    final_gen.sort(reverse=True, key=lambda Schedule: Schedule.get_fitness_score())
    
    return final_gen
    

def roulette_parent_selection(generation: list[Schedule]):
    """Used for selecting a parent pair in crossover. 
    It is based on ranking all individuals and assigning them a rank to stop big differences between their fitness scores.
    Then, for each individual in a generation, a random number is generated between 0 and 1.
    The rank and the random score are multiplied and that is the final score of an individual.
    The two Schedules with best final scores are selected for breeding. 
    This way each individual has a chance to be picked but better individuals are favored."""

    generation.sort(reverse=True, key=lambda Schedule: Schedule.get_fitness_score())
    schedule_ranking = list(range(len(generation), 0, -1))
    random_scores = [random() for _ in range(len(schedule_ranking))]
    final = [schedule_ranking[i] * random_scores[i] for i in range(len(schedule_ranking))] # now this list is sorted ascendingly, so the biggest nums are on the end
    sorted_scores = sorted(range(len(final)), key=lambda i:final[i])
    return sorted_scores[-1], sorted_scores[-2]

def crossover_all(generation: list[Schedule], population_size: int, mutation_chance: int, classes: list[Subject]):
    """Breeds individuals (Schedules) which passed the selection (previous step in life cycle)"""
    child_gen = []
    while len(child_gen) < population_size:
        # Roulette selection of parents
        parent1, parent2 = roulette_parent_selection(generation=generation)
        child1, child2 = cross_over(parent1=generation[parent1], parent2=generation[parent2], class_list=classes, mutations = mutation_chance)

        child_gen.append(child1)
        child_gen.append(child2)

    return child_gen
     
# def mutations(generation: list[Schedule], mutation_chance, classes):
#     """Function that handles calling the mutate function in cases it needs to be called"""
    
#     for individual in generation:
#         chance = random()

#         if chance <= mutation_chance:
#             individual.mutate(classes)

#     return generation

def life_cycle(max_generations, best_fitness, stopping_criteria, classes, population_size, selection_parameter, mutation_chance, rooms, days):
    """This is the main function that will do the genetic algorithm on populations, where the algorithm consists of:
        0. Generating the first population (Gen. 1)
        Then, we loop through the following 4 steps until one of the stopping criteria is fulfilled 
        * Loop stop criteria - reached max number of generations or the best Schedule is within an acceptable distance from an optimal one.
        The main loop consists of:
            1. Crossover (breeding) including possible mutations on children genomes
            2. Selection of best Schedules from the parent generation and the new children
            3. Recalculating fitness upon the population
        
        returns the best species from the population, regarded as the best schedule
    """
    current_gen = generate_first_gen(classes, population_size,len(rooms))
    current_gen.sort(reverse=True, key=lambda Schedule: Schedule.get_fitness_score())
    generation_index = 1
    max_fitness = current_gen[0].get_fitness_score()

    while not (generation_index == max_generations + 1 or abs(max_fitness - best_fitness) < stopping_criteria):
        print_generation(current_gen, generation_index)
        new_gen = crossover_all(current_gen, population_size, mutation_chance, classes) # Crossover includes mutations of children
        current_gen = selection(current_gen, new_gen, selection_parameter, population_size)

        max_fitness = current_gen[0].get_fitness_score()
        generation_index += 1

    current_gen.sort(reverse=True, key=lambda Schedule: Schedule.get_fitness_score()) # called to sort the population by fitness
    print("\n\nBEST BEBA")
    # current_gen[0].nice_print()    
    current_gen[0].no_overlap()

    current_gen[0].write_schedule_to_html(classes, rooms, days, "schedules/novelabele.html")
    return current_gen[0]  # This is the best schedule



def print_generation(generation: list[Schedule], index: int):
    """For debugging purposes, a function that will show the statistics of a generation"""
    print("\nGeneration no.", index)
    fitness_list = [ind.get_fitness_score() for ind in generation]
    print("Best fitness:", max(fitness_list))
    print("Mean fitness:", mean(fitness_list))
    print("Median fitness:", median(fitness_list))
    print("Worst fitness:", min(fitness_list))

    print("\n-------------------------------------")
