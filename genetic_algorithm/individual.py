
class Schedule:
    """
    Represents a schedule for classes in a school. It contains class_list, 
    it is a list of lists (each sublist represents a time slot so there are 12 hours * 4 quarters * 5 days * class_count * room_count),
    so the first list is on Monday at 7:00 in the first room, the second is on Monday at 7:15 also first room, and so on.
    If the class lasts 1 hour, it will occupy 4 consecutive slots.
    It is a list of lists, because in the beginning we allow multiple classes to be scheduled at the same time,
    but this will be corrected later in the algorithm (negative impact on fitness score).
    The mapping is a dictionary that maps class indices to their first positions (start of the class) in the class_list.

    """
    __slots__ = ('class_list', 'mapping', 'fitness_score')
    def __init__(self, class_count: int, room_count: int):
        self.class_list = [[] for _ in range(12 * 4 * 5 * class_count * room_count)]
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
    
