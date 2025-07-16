
from random import random, randint

from structures.subject import Subject

class Schedule:
    """
    Represents a schedule for classes in a school. It contains class_list, 
    it is a list of lists (each sublist represents a time slot so there are 12 hours * 4 quarters * 5 days  * room_count),
    so the first list is on Monday at 7:00 in the first room, the second is on Monday at 7:15 also first room, and so on.
    If the class lasts 1 hour, it will occupy 4 consecutive slots.
    Also, blocks are introduced to prevent overlap of one subject across days or different rooms.
    It is a list of lists, because in the beginning we allow multiple classes to be scheduled at the same time,
    but this will be corrected later in the algorithm (negative impact on fitness score).
    The mapping is a dictionary that maps class indices to their first positions (start of the class) in the class_list.

    """
    __slots__ = ('class_list', 'mapping', 'fitness_score', 'num_blocks', 'block_size')
    def __init__(self, class_count: int, room_count: int):
        """
        Initializes a Schedule object with the given number of classes and rooms. The time slots are represented as a list of lists,
        where each sublist corresponds to a time slot (12 hours * 4 quarters * 5 days * room_count).
        Besides the list, each Schedule has a mapping.
        The mapping is a dictionary where the key is the class index and the value is -1 (indicating no class scheduled).
        The mapping will be updated when classes are added to the schedule.
        :param class_count: The number of classes in the schedule.
        :param room_count: The number of rooms in the schedule."""
        
        self.class_list = [[] for _ in range(12 * 4 * 5 * room_count)]
        self.mapping = {i: -1 for i in range(class_count)}
        self.fitness_score = -1
        self.num_blocks = 5 * room_count  # We have 5 work days and n rooms, so each combination of these is one block
        self.block_size = 4 * 12 # Since we work with quarters of an hour, this is 4 quarters per 12 hours (from 7 am to 7 pm)

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

    def set_random_classes(self, class_number: int, classes: list[Subject]):
        """
        Used for randomizing an individual Schedule, used in creating the first generation.
        Iterates through all the classes and assignes them to a random timeslot (15 minutes) and classroom, according to Schedule structure. 
        Adding a class to the schedule is done by appending it to the class_list and updating the mapping
        and checking for overlaps, if any occur the class will be placed in a different slot.

        :param class_number: The number of classes to be scheduled.
        :param room_number: The number of rooms available for scheduling.
        :param classes: The list of classes to be scheduled.
        """
        for i in range(class_number):
            # For each class, we try to place it in a random time slot
            # We will try to place it in a random time slot, if it overlaps with another class, we will try again
            placed = False
            tries = 0
            while not placed and tries < 100:
                # Pick a random block (day and room) and place a random class in it
                block_id = randint(0, self.num_blocks - 1)
                block_start = block_id * self.block_size
                block_end = block_start + self.block_size - classes[i].duration
                random_class_index = randint(block_start, block_end)
               # Check for overlap
                overlap = False
                for j in range(classes[i].duration):
                    if self.class_list[random_class_index + j]:
                        overlap = True
                        break
                if not overlap:
                    placed = True
                tries += 1
            if not placed:
                block_id = randint(0, self.num_blocks - 1)   # first pick out a block
                block_start = block_id * self.block_size
                block_end = block_start + self.block_size - classes[i].duration
                random_class_index = randint(block_start, block_end)

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
        - Schedule Validity: Checks if the classes are scheduled in valid time slots, without overlaps.
          If a class is scheduled in an invalid slot, it will be penalized.
        Second:
        - Schedule Spread: Checks if the classes are spread evenly throughout the day.
          The score is calculated based on the time slots used and the spread of classes.

        :param all_class: The list of classes to calculate the fitness score for.
        """

        penalty= 1

        # First Part: Schedule Validity
        for class_index, start_slot in self.mapping.items():
            duration = all_class[class_index].get_duration()
            

            # Check before
            if start_slot == 0 or not self.class_list[start_slot - 1]:
                continue
            else:
                penalty +=5

            # Check after
            if start_slot + duration >= len(self.class_list) or not self.class_list[start_slot + duration]:
                continue
            else:
                penalty += 5

            # Check slot overlap
            
            for i in range(start_slot, start_slot + duration):
                if len(self.class_list[i]) > 1:
                    penalty += 1000


        # Second Part: Schedule Spread (Late Starts + Early Finishes)
        total_score = 0
        slots_per_day = 12 * 4  # 12 hours * 4 = 48 slots/day

        for day_start in range(0, len(self.class_list), slots_per_day):
            slots = self.class_list[day_start: day_start + slots_per_day]
            p1=1

            prefix = next((i for i, s in enumerate(slots) if s), slots_per_day)
            suffix = next((i for i, s in enumerate(reversed(slots)) if s), slots_per_day)
            
            # If the prefix or suffix is equal to slots_per_day, it means that there are no classes scheduled in that day
            if prefix == slots_per_day or suffix == slots_per_day:
                p1 = 0

            total_score += (prefix * 15) * ((suffix) * 15) * p1  # Convert slots to minutes

        fitness_score = total_score/ penalty

        self.set_fitness_score(fitness_score)
    
    
    def mutate(self, mutation_chance: float, all_clases: list[Subject]):
        """Funtion that handles the mutation of an individual.
        It randomly selects a class and tries to move it to a different time slot,
        in the same block (same day and room), if possible.

        :param mutation_chance: The chance of mutation happening, a number between 0 and 1.
        :param all_clases: The list of classes to be scheduled.
           """
        
        mutation_happens = random()
        # The principle is the following: We generate a random number between 0 and 1. Then we compare that number to the parameter
        # mutation_chance - if the random number is smaller than mutation chance then we mutate the individual. Otherwise, we exit this function,
        # which is what is implemented below
        if mutation_happens > mutation_chance:
            self.fitness(all_clases)  # If we do not mutate, we still need to calculate the fitness score
            return

        class_num = randint(len(all_clases)//16, len(all_clases)//4)
        # Will mutate {class_num} classes randomly, from 1/16 to 1/4 of all classes so it also randomizes the mutation strength
        for _ in range(class_num):
            class_index = randint(0, len(self.mapping) - 1) # We pick a class out of all classes that are in this Schedule

            old_position = self.mapping[class_index]
            block= old_position // self.block_size

            duration = all_clases[class_index].duration
            
            # Remove the class from the old position
            for i in range(old_position, old_position + duration):
                if class_index in self.class_list[i]:
                    self.class_list[i].remove(class_index)

            placed = False
            tries = 0

            while not placed and tries < 100:
                block_id = block  
                block_start = block_id * self.block_size
                block_end = block_start + self.block_size - duration
                new_position = randint(block_start, block_end)
               # Check for overlap
                overlap = False
                for j in range(duration):
                    if self.class_list[new_position + j]:
                        overlap = True
                        break
                if not overlap:
                    placed = True
                tries += 1
            if not placed:
                block_id = randint(0, self.num_blocks - 1)   # first pick out a block
                block_start = block_id * self.block_size
                block_end = block_start + self.block_size - duration
                new_position = randint(block_start, block_end)

            for j in range(duration):
                self.class_list[new_position + j].append(class_index)
            self.mapping[class_index] = new_position

        self.fitness(all_clases)


    def __repr__(self):
        return f"Schedule(class_list={self.class_list}, mapping={self.mapping}, fitness_score={self.fitness_score})"

    def __str__(self):
        return f"Schedule: {self.class_list}, {self.mapping}, {self.fitness_score}"
    
    def nice_print(self):
        """Prints the schedule in a nice format in console, showing the classes scheduled in each time slot.
        Used for debugging and visualization purposes."""
        print("\n-------------------------------")
        print("SCHEDULE BY DAYS AND ROOMS:\n")

        slots_per_hour = 4
        hours_per_day = 12
        days_per_week = 5

        slots_per_day_per_room = hours_per_day * slots_per_hour  # 48
        num_rooms = len(self.class_list) // (slots_per_day_per_room * days_per_week)

        for day in range(days_per_week):
            print(f"\nDAY {day + 1}")
            for room in range(num_rooms):
                print(f"  ROOM {room + 1}")
                start = (day * slots_per_day_per_room * num_rooms) + (room * slots_per_day_per_room)
                end = start + slots_per_day_per_room
                for slot in range(start, end):
                    print(f"    Slot {slot - start:2d}: {self.class_list[slot]}")
                print("  -------------------------")
            print("*****************************")


    def write_schedule_to_html(self, classes: list[Subject], filename: str, generation: int = 0, mutation: list[float] = [0.5, 0.3, 0.2], keepPercent: float = 0.2):
        """
        Write the schedule to an HTML file in a clear table format:
        - Each day has a separate table.
        - Each table shows rows for time slots and columns for rooms.
        - Each cell shows the class name(s) scheduled in that slot.
        """

        slots_per_hour = 4
        hours_per_day = 12
        slots_per_day_per_room = slots_per_hour * hours_per_day  # 48
        days_per_week = 5
        # Calculate the number of rooms based on the class_list length
        num_rooms = len(self.class_list) // (slots_per_day_per_room * days_per_week)

        html = [
            "<!DOCTYPE html>",
            "<html>",
            "<head>",
            "<meta charset='UTF-8'>",
            "<title>Schedule</title>",
            "<style>",
            "table { border-collapse: collapse; margin: 20px; }",
            "th, td { border: 1px solid black; padding: 5px; text-align: center; }",
            "th { background-color: #f2f2f2; }",
            "</style>",
            "</head>",
            "<body>",
            f"<h1>Schedule (Fitness Score: {self.get_fitness_score():.2f})</h1>",
            f"<p>Generation: {generation}, Mutation: {mutation}, Keep Percent: {keepPercent}</p>"

        ]

        # For each day, creates a table
        for day in range(days_per_week):
            html.append(f"<h2>Day {day + 1}</h2>")
            html.append("<table>")
            
            # Table header: time slot | room 1 | room 2 | ...
            header = "<tr><th>Time</th>"
            for room in range(num_rooms):
                header += f"<th>Room {room + 1}</th>"
            header += "</tr>"
            html.append(header)

            # For each time slot in a day
            for slot_in_day in range(slots_per_day_per_room):
                row = f"<tr><td>{7 + slot_in_day // slots_per_hour}:{(slot_in_day % slots_per_hour) * 15:02d}</td>"
                
                for room in range(num_rooms):
                    # Compute the global slot index
                    slot_idx = (day * num_rooms * slots_per_day_per_room) + (room * slots_per_day_per_room) + slot_in_day
                    slot_classes = self.class_list[slot_idx]

                    if slot_classes:
                        names = ", ".join(classes[i].name for i in slot_classes)
                    else:
                        names = "-"
                    row += f"<td>{names}</td>"

                row += "</tr>"
                html.append(row)

            html.append("</table>")

        html.append("</body>")
        html.append("</html>")

        # Write to file
        with open(filename, 'w', encoding='utf-8') as f:
            f.write('\n'.join(html))

        print(f"\n Schedule written to {filename}")


    def no_overlap(self):
        """Check if the schedule has no overlaps and print a message accordingly."""

        for list in self.class_list:
            # Each list should contain at most one class index, if it contains more than one, there is an overlap
            if len(list) > 1:
                print("OVERLAP!!!!!!!! NOT GOOD!!!!")
                return False
        
        print("\n YAYYYYYY NO OVERLAP, VALID SCHEDULE!!!! \n   >>>>>>>>>>>>>>>")
        return True

def cross_over(parent1: Schedule, parent2: Schedule, class_list: list[Subject], mutations: float):
    """
    Performs crossover between two schedules using three-point crossover.
    If preferred parent's position is invalid, FORCE the fallback parent's position.

    :param parent1: The first parent Schedule.
    :param parent2: The second parent Schedule.
    :param class_list: The list of classes to be scheduled.
    :param mutations: The mutation chance for the children schedules.
    """
    class_count = len(parent1.mapping)
    room_count = len(parent1.class_list) // (12 * 4 * 5)
    child1 = Schedule(class_count, room_count)
    child2 = Schedule(class_count, room_count)

    # pick two random crossover points
    k1 = randint(0, class_count // 2)
    k2 = randint(class_count // 2, class_count - 1)

    def place_class(child, class_idx, preferred_parent, fallback_parent):
        """Try preferred parent first, if invalid FORCE fallback parent"""
        duration = class_list[class_idx].get_duration()
        
        # Try preferred parent
        value = preferred_parent.mapping.get(class_idx, -1)
        if value != -1:
            # Check if slots are free (no overlap)
            if all(not child.class_list[value + j] for j in range(duration) if value + j < len(child.class_list)):
                child.mapping[class_idx] = value
                for j in range(duration):
                    child.class_list[value + j].append(class_idx)
                return
        
        # If preferred failed, FORCE fallback parent (no matter what)
        value = fallback_parent.mapping.get(class_idx, -1)
        if value != -1:
            child.mapping[class_idx] = value
            for j in range(duration):
                child.class_list[value + j].append(class_idx)
        else:
            # If both parents don't have this class, leave unplaced
            child.mapping[class_idx] = -1

    # Child 1: parent1 -> parent2 -> parent1
    for i in range(k1):
        place_class(child1, i, parent1, parent2)
    for i in range(k1, k2):
        place_class(child1, i, parent2, parent1)
    for i in range(k2, class_count):
        place_class(child1, i, parent1, parent2)

    # Child 2: parent2 -> parent1 -> parent2
    for i in range(k1):
        place_class(child2, i, parent2, parent1)
    for i in range(k1, k2):
        place_class(child2, i, parent1, parent2)
    for i in range(k2, class_count):
        place_class(child2, i, parent2, parent1)

    # mutate both children
    child1.mutate(mutations, class_list)
    child2.mutate(mutations, class_list)

    return child1, child2