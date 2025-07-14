
from random import random, randint, shuffle

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
        # Initialize the schedule where the time slots are represented as a list of lists.
        # Each sublist corresponds to a time slot (12 hours * 4 quarters * 5 days * room_count).
        self.class_list = [[] for _ in range(12 * 4 * 5 * room_count)]
        # Initialize the mapping of classes to their indices.
        # The mapping is a dictionary where the key is the class index and the value is -1 (indicating no class scheduled).
        # The mapping will be updated when classes are added to the schedule.
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

    def set_random_classes(self, class_number: int, room_number: int, classes: list[Subject]):
        """
        Used for randomizing an individual Schedule, used in creating the first generation.
        Iterates through all the classes and assignes them to a random timeslot (15 minutes) and classroom, according to Schedule structure. 
        Adding a class to the schedule is done by appending it to the class_list and updating the mapping.
        """
        for i in range(class_number):
            placed = False
            tries = 0
            while not placed and tries < 100:
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
                    for j in range(classes[i].duration):
                        self.class_list[random_class_index + j].append(i)
                    self.mapping[i] = random_class_index
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

        penalty= 1
        total_classes = len(self.mapping)

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
                    penalty += 100

            

           

        # Second Part: Schedule Spread (Late Starts + Early Finishes)
        second_score_total = 0
        slots_per_day = 12 * 4  # 12 hours * 4 = 48 slots/day
        days = len(self.class_list) // slots_per_day

        for day_start in range(0, len(self.class_list), slots_per_day):
            slots = self.class_list[day_start: day_start + slots_per_day]
            p1=1
            p2=0

            prefix = next((i for i, s in enumerate(slots) if s), slots_per_day)
            suffix = next((i for i, s in enumerate(reversed(slots)) if s), slots_per_day)
            suffix = slots_per_day - suffix - 1  # Convert index from end

            if prefix == slots_per_day or suffix == slots_per_day:
                p1 = 0

            # Penalize if the last class ends in the last eighth of the day
            # or if the first class starts in the first eighth of the day
            # eighth = slots_per_day // 8
            if suffix >= slots_per_day//10:
                p2 -= 10000  # Penalize if the last class ends late or first class starts early
            if prefix < slots_per_day//10:
                p2 -= 10000  # Penalize if the last class ends late or first class starts early
            second_score_total += (prefix * 15) * ((slots_per_day - 1 - suffix) * 15)*p1 +p2  # Convert slots to minutes

        # Normalize second part (optional but improves stability)
        fitness_score = second_score_total/ penalty
        # Or try weighted sum: 0.7 * first_part_score + 0.3 * second_part_score

        self.set_fitness_score(fitness_score)
    
    # In the future possibly change more than 2 classes
    # In future changes should be more heavy to introduce variance
    def mutate(self, mutation_chance: int, all_clases: list[Subject]):
        """Funtion that handles the mutation of an individual.
           To improve variability, there will be 2 kinds of mutations:
           1. Moving a random class from scheduled classes to other random time slot.
           2. Switching two classes time slots. (In the works, causes errors)
           """
        
        mutation_happens = random()
        # The principle is the following: We generate a random number between 0 and 1. Then we compare that number to the parameter
        # mutation_chance - if the random number is smaller than mutation chance then we mutate the individual. Otherwise, we exit this function,
        # which is what is implemented below
        if mutation_happens > mutation_chance:
            self.fitness(all_clases)  # If we do not mutate, we still need to calculate the fitness score
            return
        # weight = random()
        class_num = randint(len(all_clases)//18, len(all_clases)//4)
        # Will mutate 1 -  classes randomly
        for _ in range(class_num):
            class_index = randint(0, len(self.mapping) - 1) # We pick a class out of all classes that are in this Schedule

            old_position = self.mapping[class_index]
            block= old_position // self.block_size

            duration = all_clases[class_index].duration
            
            for i in range(old_position, old_position + duration):
                if class_index in self.class_list[i]:
                    self.class_list[i].remove(class_index)

            placed = False
            tries = 0
            # random_start =random()
            # if random_start < 0.6:
            #     random_s = False
            # else:
            #     random_s = True
            while not placed and tries < 100:
                # if random_s:
                #     block_id = randint(0, self.num_blocks - 1)  # first pick out a block
                # else:
                #     block_id = block
                block_id = block  # first pick out a block
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
                    for j in range(duration):
                        self.class_list[new_position + j].append(class_index)
                    self.mapping[class_index] = new_position
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
        print("\n-------------------------------")
        print("SCHEDULE BY DAYS AND ROOMS:\n")

        slots_per_hour = 4
        hours_per_day = 12
        days_per_week = 5

        slots_per_day_per_room = hours_per_day * slots_per_hour  # 48
        slots_per_day_all_rooms = slots_per_day_per_room * (len(self.class_list) // (slots_per_day_per_room * days_per_week))
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


    def write_schedule_to_html(self, classes: list[Subject], filename: str):
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
        ]

        # For each day, create a table
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

        for list in self.class_list:
            if len(list) > 1:
                print("OVERLAP!!!!!!!! NOT GOOD!!!!")
                return
        
        print("\n YAYYYYYY NO OVERLAP, VALID SCHEDULE!!!! \n   >>>>>>>>>>>>>>>")


def cross_over(parent1: Schedule, parent2: Schedule, class_list: list[Subject], mutations: int) -> Schedule:
    """
    Performs crossover between two schedules.
    This is done by combining the class list of twi schedules.
    2 parents are combined to get 2 child Schedules.

    """
    class_count = len(parent1.mapping)
    room_count = len(parent1.class_list) // (12 * 4 * 5)

    def build_child(preferred, fallback):
        child = Schedule(class_count, room_count)
        indices = list(range(class_count))
        shuffle(indices)  # Shuffle to avoid bias
        for i in indices:
            placed = False
            # Try preferred parent
            for mapping in (preferred.mapping, fallback.mapping):
                pos = mapping.get(i, -1)
                duration = class_list[i].get_duration()
                if pos == -1:
                    continue
                # Check if slots are free
                if all(not child.class_list[pos + j] for j in range(duration)):
                    for j in range(duration):
                        child.class_list[pos + j].append(i)
                    child.mapping[i] = pos
                    placed = True
                    break
            if not placed:
                # Try to find a random valid slot
                tries = 0
                while tries < 100:
                    block_id = randint(0, child.num_blocks - 1)
                    block_start = block_id * child.block_size
                    block_end = block_start + child.block_size - duration
                    rand_pos = randint(block_start, block_end)
                    if all(not child.class_list[rand_pos + j] for j in range(duration)):
                        for j in range(duration):
                            child.class_list[rand_pos + j].append(i)
                        child.mapping[i] = rand_pos
                        placed = True
                        break
                    tries += 1
                if not placed:
                    # As a last resort, place anyway (may overlap, but rare)
                    for j in range(duration):
                        child.class_list[rand_pos + j].append(i)
                    child.mapping[i] = rand_pos
        return child

        # Child 1: prefer parent1, fallback to parent2
    child1 = build_child(parent1, parent2)
        # Child 2: prefer parent2, fallback to parent1
    child2 = build_child(parent2, parent1)

    child1.mutate(mutations, class_list)
    child2.mutate(mutations, class_list)
    return child1, child2