import random
from statistics import mean, median
from genetic_algorithm.individual import *
import time


def generate_first_gen(classes, population_size, room_number):
    """Generates the first generation of Schedules (individuals) with random classes assigned to them.
    Calls the Schedule class to create a new Schedule object for each individual until the population is filled.
    A generation is regarded as a list of Schedule objects, each representing a potential solution to the scheduling problem.

    :param classes: List of Subject objects representing the classes to be scheduled.
    :param population_size: The number of individuals in the population.
    :param room_number: The number of rooms available for scheduling.

    :return: A list of Schedule objects representing the first generation of individuals."""
    generation_list = []
    for i in range (population_size):
            current_individual = Schedule(len(classes), room_number)
            current_individual.set_random_classes(len(classes), classes)
            generation_list.append(current_individual)
        
    return generation_list


# Implements elitism - only a few schedules from current gen can survive, we fill the new gen with only children
def selection(generation: list[Schedule], selection_percent, population_size):
    """Chooses which Schedules (individuals) survive to the next generation based on elitism.
    Only the best Schedules from the current generation will survive, and the rest will be filled with children from the crossover step.

    :param generation: The current generation of Schedules.
    :param selection_percent: The percentage of the best Schedules that will survive to the next generation - implementation of elitism.
    :param population_size: The total number of Schedules in the population.

    :return: The new generation of Schedules after selection."""
    num_parents= int(selection_percent * population_size)  # How many parents will survive to the next generation
    surviving_schedules = generation[:num_parents]  # Take the best Schedules from the current generation
    children = generation[population_size:]  # The children that were created in the crossover step
    children.sort(reverse=True, key=lambda Schedule: Schedule.get_fitness_score())  # Sort children by fitness score 
    generation = surviving_schedules + children[:population_size - num_parents]  # Fill the new generation with the best children
    generation.sort(reverse=True, key=lambda Schedule: Schedule.get_fitness_score()) # Sort the new generation by fitness score
    
    return generation
    

def roulette_parent_selection(generation: list[Schedule]):
    """Favors the best Schedules in the population, but allows for some randomization to ensure diversity.
    parent1 and parent2 are chosen based on their fitness scores, with a random factor to ensure diversity.

    :param generation: The current generation of Schedules.

    :return: Indices of the two parents chosen for crossover."""

    generation.sort(reverse=True, key=lambda Schedule: Schedule.get_fitness_score()) # sort the generation by fitness score
    schedule_ranking = list(range(len(generation), 0, -1)) # create a ranking
    random_scores = [random() for _ in range(len(schedule_ranking))] # create a list of random scores
    final = [schedule_ranking[i] * random_scores[i] for i in range(len(schedule_ranking))] # now this list is sorted ascendingly, so the biggest nums are on the end
    sorted_scores = sorted(range(len(final)), key=lambda i:final[i]) # sort the list of scores, so the biggest nums are on the end
    return sorted_scores[-1], sorted_scores[-2]  # choose the last two indices, which correspond to the biggest scores

def crossover_all(generation: list[Schedule], population_size: int, mutation_chance: float, classes: list[Subject]):
    """Breeds individuals (Schedules) which passed the selection (previous step in life cycle). 
    Works by selecting two parents (roulette selection) and creating two children from them through crossover function.
    
    :param generation: The current generation of Schedules.
    :param population_size: The total number of Schedules in the population.
    :param mutation_chance: The chance of mutation for each child.
    :param classes: List of Subject objects representing the classes to be scheduled.

    :return: The new generation of Schedules after crossover and mutation."""

    # The generation will be filled with {population_size} parents so we add {population_size} children to select from
    while len(generation) < 2 * population_size:
        parent1, parent2 = roulette_parent_selection(generation=generation)
        child1, child2 = cross_over(parent1=generation[parent1], parent2=generation[parent2], class_list=classes, mutations = mutation_chance)

        generation.append(child1)
        generation.append(child2)

    return generation
     

def life_cycle(max_generations, optimal_fitness, stopping_criteria, classes, population_size, selection_parameter, mutation_chance,rooms, output_file):
    """This is the main function that will do the genetic algorithm on populations, where the algorithm consists of:
        0. Generating the first population (Gen. 1)
        Then, we loop through the following 4 steps until one of the stopping criteria is fulfilled 
        * Loop stop criteria - reached max number of generations or the best Schedule is within an acceptable distance from an optimal one.
        The main loop consists of:
            1. Selection
            2. Crossover (breeding) including possible mutations on children genomes
            3. Recalculating fitness upon the population
        
    :param max_generations: The maximum number of generations to run the algorithm for.
    :param optimal_fitness: The fitness score of the "ideal" Schedule which has not yet been reached with the algorithm.
    :param stopping_criteria: The minimum difference between the best fitness and the current maximum fitness
    :param classes: List of Subject objects representing the classes to be scheduled.
    :param population_size: The total number of Schedules in the population.
    :param selection_parameter: The percentage of the best Schedules that will survive to the next generation.
    :param mutation_chance: A list of three mutation chances for different stages of the algorithm.
    :param rooms: List of rooms available for scheduling.

    :return: The best Schedule from the population, which is regarded as the best schedule.
    """
    # The 0 step - generating the first generation with random individuals
    current_gen = generate_first_gen(classes, population_size,len(rooms))
    generation_index = 1
    max_fitness = 0

    # The main loop of the genetic algorithm
    while not (generation_index == max_generations or (optimal_fitness - max_fitness) < stopping_criteria):
        print_generation(current_gen, generation_index)
        max_fitness = current_gen[0].get_fitness_score()
        # Has variant mutation chance based on generation number
        if generation_index< max_generations/2:
            mutatation = mutation_chance[0]
        elif generation_index < max_generations * 0.75:
            mutatation = mutation_chance[1]
        else:
            mutatation = mutation_chance[2]
        current_gen = crossover_all(current_gen, population_size, mutatation, classes) # Crossover includes mutations of children
        current_gen = selection(current_gen, selection_parameter, population_size)

        generation_index += 1

    current_gen.sort(reverse=True, key=lambda Schedule: Schedule.get_fitness_score())  # Sort the generation by fitness score
    # After sorting, the best Schedule by its fitness score is the first one in the list 
    print("\n\nBEST SCHEDULE:")
    print("Fitness score:", current_gen[0].get_fitness_score())
    # Check if the best schedule has no overlaps
    current_gen[0].no_overlap()

    current_gen[0].write_schedule_to_html(classes, output_file, generation=generation_index, mutation=mutation_chance, keepPercent=selection_parameter)
    return current_gen[0]  # The best schedule



def print_generation(generation: list[Schedule], index: int):
    """For debugging purposes, a function that will show the statistics of fitness scores in a generation

    :param generation: The current generation of Schedules.
    :param index: The index of the generation in the life cycle.
    """

    print("\nGeneration no.", index)
    fitness_list = [ind.get_fitness_score() for ind in generation]
    print("Best fitness:", max(fitness_list))
    print("Mean fitness:", mean(fitness_list))
    print("Median fitness:", median(fitness_list))
    print("Worst fitness:", min(fitness_list))

    print("\n-------------------------------------")
