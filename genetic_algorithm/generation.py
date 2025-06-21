# Here will be the code for generating the initial generation
from math import abs
from individual import Schedule, cross_over
import random


def generate_first_gen(classes, population_size, class_number, room_number):
    generation_list = []
    for i in range (population_size):
            current_individual = Schedule(class_count=class_number, room_count=room_number)
            for j in range(class_number): # iterating through the indexes of all classes
                random_class_index = random.randint(0, 4*12*room_number)
                for k in range(classes[j].duration):
                     current_individual.class_list[random_class_index + k].append(j) 
                current_individual.mapping[j] = random_class_index
            generation_list.append(current_individual)

# Needs to be tested
def selection(generation, selection_percent):
    generation.sort(reverse=True, key=Schedule.fitness())   # This will sort the Schedules in a descending order, meaning the best Schedules will be up front
    kept_individuals = selection_percent * len(generation)
    generation = generation[:int(kept_individuals)] # round that to nearest integer
    return generation

def crossover_all(generation, population_size):
    """Breeds individuals (Schedules) which passed the selection (previous step in life cycle)"""
    passed_selection = len(generation)
    while len(generation) < population_size:
        parent1 = random.randint(0, passed_selection)
        parent2 = random.randint(0, passed_selection)

        generation.append(cross_over(parent1=parent1, parent2=parent2))

    return generation
     
def mutations(generation, mutation_chance):
     pass

def life_cycle(max_generations, best_fitness, stopping_criteria, classes, population_size, selection_parameter):

    current_gen = generate_first_gen(classes, population_size)
    generation_index = 0
    max_fitness = 0

    while not (generation_index == max_generations - 1 and abs(max_fitness - best_fitness) < stopping_criteria):
        current_gen = selection(current_gen, selection_parameter)
        current_gen = crossover_all(current_gen)
        current_gen = mutations()
        generation_index += 1



def print_generation(generation):

    pass