
from random import random

from structures.subject import Subject


class Schedule:
    """
    Represents a schedule for classes in a school. It contains class_list, 
    it is a list of lists (each sublist represents a time slot so there are 12 hours * 4 quarters * 5 days  * room_count),
    so the first list is on Monday at 7:00 in the first room, the second is on Monday at 7:15 also first room, and so on.
    If the class lasts 1 hour, it will occupy 4 consecutive slots.
    It is a list of lists, because in the beginning we allow multiple classes to be scheduled at the same time,
    but this will be corrected later in the algorithm (negative impact on fitness score).
    The mapping is a dictionary that maps class indices to their first positions (start of the class) in the class_list.

    """
    __slots__ = ('class_list', 'mapping', 'fitness_score')
    def __init__(self, class_count: int, room_count: int):
        # Initialize the schedule where the time slots are represented as a list of lists.
        # Each sublist corresponds to a time slot (12 hours * 4 quarters * 5 days * room_count).
        self.class_list = [[] for _ in range(12 * 4 * 5 * room_count)]
        # Initialize the mapping of classes to their indices.
        # The mapping is a dictionary where the key is the class index and the value is -1 (indicating no class scheduled).
        # The mapping will be updated when classes are added to the schedule.
        self.mapping = {i: -1 for i in range(class_count)}
        self.fitness_score = -1

    def get_class_list(self):
        """Returns the list of classes in the schedule."""
        return self.class_list

    def get_mapping(self):
        """Returns the mapping of classes to their indices."""
        return self.mapping

    def get_fitness_score(self):
        """Returns the fitness score of the schedule."""
        return self.fitness_score

    def set_fitness_score(self, score: int):
        """Sets the fitness score of the schedule."""
        self.fitness_score = score

    def set_random_class(self):
        """
        Sets a class at a random time slot and room. Time slots are 15 minutes each.
        Adding a class to the schedule is done by appending it to the class_list and updating the mapping.
        
        """
        pass

    def fitness(self):
        """
        Calculates the fitness score of the schedule.
        The fitness score is a measure of how well the schedule meets the requirements.
        It can be based on various factors such as the number of classes scheduled, 
        conflicts, and other criteria.
        
        """
        pass

    


    def __repr__(self):
        return f"Schedule(class_list={self.class_list}, mapping={self.mapping}, fitness_score={self.fitness_score})"

    def __str__(self):
        return f"Schedule: {self.class_list}, {self.mapping}, {self.fitness_score}"

def cross_over(parent1: Schedule, parent2: Schedule, class_list: list[Subject]) -> Schedule:
    """
    Performs crossover between two schedules.
    This can be done by combining the class lists and mappings of both schedules.

    """
    k = random.randint(0, len(parent1.class_list) - 1)

    class_count = len(parent1.mapping)
    room_count = len(parent1.class_list) // (12 * 4 * 5)
    child = Schedule(class_count, room_count)
    for i in range(k):
        value = parent1.mapping.get(i, -1)
        child.mapping[i] = value
        duration = class_list[i].get_duration()
        for j in range(duration):
            child.class_list[value + j].append(i)
    for i in range(k, class_count):
        value = parent2.mapping.get(i, -1)
        child.mapping[i] = value
        duration = class_list[i].get_duration()
        for j in range(duration):
            child.class_list[value + j].append(i)
    return child
