
from random import random, randint

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

    def set_fitness_score(self, score: int) -> None:
        """Sets the fitness score of the schedule."""
        self.fitness_score = score

    def set_random_classes(self, class_number: int, room_number: int, classes: list[Subject]):
        """
        Used for randomizing an individual Schedule, used in creating the first generation.
        Iterates through all the classes and assignes them to a random timeslot (15 minutes) and classroom, according to Schedule structure. 
        Adding a class to the schedule is done by appending it to the class_list and updating the mapping.
        """
        for i in range(class_number): # iterating through the indexes of all classes
            random_class_index = randint(0, len(self.class_list) - classes[i].duration)
            for j in range(classes[i].duration):
                    self.class_list[random_class_index + j].append(i) 
            self.mapping[i] = random_class_index

        self.fitness(classes)


    def fitness(self, all_class: list[Subject]) -> None:
        """
        Calculates the fitness score of a schedule.
        The fitness score is a measure of how well the schedule meets the requirements.
        There will be two main criteria for the fitness evaluation and the final score will be their multiplication:
        First:
            If a class is scheduled at a time slot that is already occupied, it will not get a point.
            if at the end of a class there is no time for the next class, it will not get a point.
            if before a class there is no time for the previous class, it will not get a point.
            The max score of a class is 3 points, the minimum is 0 points.
            The score of the first part is the sum of the scores of all classes divided 
            by the count of classes * by max point (the class can get).

        Second:
            We record for each classroom and for each day the time elapsed from 7:00 a.m. to the beginning of the first
            lectures. If we have n classrooms and m working days, there will be n m of these values
            these values ​​with pi, where i takes integer values ​​from 1 to n m
            time elapsed from the end of the last lecture to 19:00 for each day and for each classroom. This one
            we mark times with ki. We form the optimality criterion in the following way:
            The sum of pi * ki for all i from 1 to n*m is the second part of the fitness score.

        The final fitness score is the product of the two parts.
        :param all_class: The list of classes.
        """

        first_part_score = 0
        second_part_score = 0
        max_point = 3

        for k, v in self.mapping.items():
            curr = 0
            # if there is no class right before
            duration = all_class[k].get_duration()
            if v == 0:
                curr+=1
            else:
                if self.class_list[v-1] == []:
                    curr+=1
            # if there is no class right after
            if v + duration == len(self.class_list):
                curr+=1
            elif self.class_list[v + duration] == []:
                curr+=1
            # if there is no class in the same time slot
            temp_point = 1
            for i in range(v, v + duration):
                if len(self.class_list[i]) > 1:
                    temp_point = 0
                    break

            first_part_score += curr + temp_point

        first_part_score = first_part_score / (len(self.mapping) * max_point)


        for i in range(0, len(self.class_list),12*4):
            sufix=0
            prefix=0
            # Find the first non-empty slot in the first part of the day, start of the working day
            for j in range(12*4):
                if self.class_list[i+j]:
                    prefix = j
                    break
            # Find the last non-empty slot in the first part of the day, end of the working day
            for j in range(12*4-1, -1, -1):
                if self.class_list[i+j]:
                    sufix = j
                    break
            second_part_score += prefix *sufix*15*15
                
        fitness_score = first_part_score * second_part_score
        self.set_fitness_score(fitness_score)
        return
    
    # In the future possibly change more than 2 classes
    def mutate(self, all_clases: list[Subject]):
        """Funtion that handles the mutation of an individual.
           To improve variability, there will be 3 kinds of mutations:
           1. Moving a random class from scheduled classes to other random time slot.
           2. Switching two classes time slots.
           """
        option = random()
        if option > 0.5:
            class_index = randint(0, len(self.mapping) - 1) # We pick a class out of all classes that are in this Schedule

            old_position = self.mapping[class_index]

            duration = all_clases[class_index].duration
            
            for i in range(old_position, old_position + duration):
                self.class_list[i].remove(class_index)

            new_position = randint(0, len(self.class_list) - duration) # We choose a spot in the Schedule (all days, rooms) to which we move the class

            for j in range(new_position, new_position + duration):
                self.class_list[j].append(class_index)

            self.mapping[class_index] = new_position

        else:
            p = randint(0, len(self.mapping) - 1)
            q = randint(0, len(self.mapping) - 1)

            if p == q:
                if p == len(self.mapping) - 1:
                    p -= 2
                p += 1

            # Old positions for future reference
            p_old = self.mapping[p]
            q_old = self.mapping[q]

            # First retrieve the duration of both classes from all_classes parameter
            duration_p = all_clases[p].duration
            duration_q = all_clases[q].duration

            # Remove class 1, index p, from its' old position and add class 2, index q
            for i in range(p_old, p_old + duration_p):
                self.class_list[i].remove(p)
            
            # Handles the case that one longer class is swapped with a shorter one not to cause index out of range
            if p_old + duration_q > len(self.class_list):
                for slot in range(duration_q):
                    self.class_list[-1-slot].append(q)
                self.mapping[q] = len(self.class_list) - duration_q
            else:
                for j in range(self.mapping[p], self.mapping[p] + duration_q):
                    self.class_list[j].append(q)
                self.mapping[q] = p_old

            # Remove class 2, index q, from its' old position and add class 1, index p
            for k in range(self.mapping[q], self.mapping[q] + duration_q):
                self.class_list[k].remove(q)
            
            # Handles the case that one longer class is swapped with a shorter one not to cause index out of range
            if self.mapping[q] + duration_p > len(self.class_list):
                for slot in range(duration_p):
                    self.class_list[-1-slot].append(p)
                self.mapping[p] = len(self.class_list) - duration_p
            else:
                for j in range(self.mapping[q], self.mapping[q] + duration_p):
                    self.class_list[j].append(p)
                
                self.mapping[p] = q_old

        self.fitness(all_clases)


    def __repr__(self):
        return f"Schedule(class_list={self.class_list}, mapping={self.mapping}, fitness_score={self.fitness_score})"

    def __str__(self):
        return f"Schedule: {self.class_list}, {self.mapping}, {self.fitness_score}"

def cross_over(parent1: Schedule, parent2: Schedule, class_list: list[Subject]) -> Schedule:
    """
    Performs crossover between two schedules.
    This can be done by combining the class lists and mappings of both schedules.

    """
    k = randint(0, len(parent1.mapping) - 1)

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

    child.fitness(class_list)
    return child
