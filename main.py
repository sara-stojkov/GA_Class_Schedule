from reading_data import load_data
from genetic_algorithm.generation import life_cycle
from const import MAX_GENERATIONS, MUTATION_CHANCE, POPULATION_SIZE, KEEP_PERCENT, FILE_PATH, DAYS

def main():
    rooms, events = load_data(FILE_PATH)

    print("Rooms:")
    for room_id, room_name in rooms.items():
        print(f"  {room_id}: {room_name}")

    print("\nEvents:")
    for event in events:
        print(event)

    life_cycle(max_generations=MAX_GENERATIONS, best_fitness=1000000000, stopping_criteria=0.1, classes=events, 
               population_size=POPULATION_SIZE, selection_parameter=KEEP_PERCENT, mutation_chance=MUTATION_CHANCE,rooms=rooms, days=DAYS)


if __name__ == "__main__":
    main()