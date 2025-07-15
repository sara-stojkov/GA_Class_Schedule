from reading_data import load_data, load_data_from_string
from genetic_algorithm.generation import life_cycle
from const import MAX_GENERATIONS, MUTATION_CHANCE, POPULATION_SIZE, KEEP_PERCENT, FILE_PATH, BEST_FITNESS

def main():
    # Load data from the string instead of a file
    # Uncomment the next line to load from a file and comment the line below

    # rooms, events = load_data(FILE_PATH)
    rooms, events = load_data_from_string()


    life_cycle(max_generations=MAX_GENERATIONS, best_fitness=BEST_FITNESS, stopping_criteria=0.1, classes=events, 
               population_size=POPULATION_SIZE, selection_parameter=KEEP_PERCENT, mutation_chance=MUTATION_CHANCE,rooms=rooms)


if __name__ == "__main__":
    main()